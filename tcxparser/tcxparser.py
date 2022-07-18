"Simple parser for Garmin TCX files."
import time
from datetime import timedelta

from dateutil.parser import isoparse
from lxml import objectify

from .exceptions import NoHeartRateDataError

namespace = "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"
namespace2 = "http://www.garmin.com/xmlschemas/ActivityExtension/v2"


class TCXParser:
    def __init__(self, tcx_file):
        tree = objectify.parse(tcx_file)
        self.root = tree.getroot()
        self.activity = self.root.Activities.Activity

    def hr_values(self):
        return [
            int(x.text)
            for x in self.root.xpath(
                "//ns:HeartRateBpm/ns:Value", namespaces={"ns": namespace}
            )
        ]

    def altitude_points(self):
        return [
            float(x.text)
            for x in self.root.xpath(
                "//ns:AltitudeMeters", namespaces={"ns": namespace}
            )
        ]

    def position_values(self):
        return [
            (float(pos.LatitudeDegrees.text), float(pos.LongitudeDegrees.text))
            for pos in self.root.xpath(
                "//ns:Trackpoint/ns:Position", namespaces={"ns": namespace}
            )
        ]

    def distance_values(self):
        return self.root.findall(
            ".//ns:Trackpoint/ns:DistanceMeters", namespaces={"ns": namespace}
        )

    def time_values(self):
        return [
            x.text for x in self.root.xpath("//ns:Time", namespaces={"ns": namespace})
        ]

    def time_objects(self):
        """Return a list of timezone-aware datetime objects for each string in time_values()."""
        return [isoparse(x) for x in self.time_values()]

    def time_durations(self):
        """Return a list of timedelta objects for each string in time_values().

        This can be used to calculate the total time in each HR zone, as opposed to the
        total amount of trackpoints in each HR zone.
        """
        time_objects = self.time_objects()
        last_index = len(time_objects) - 1

        durations = []
        for idx, dt in enumerate(time_objects):
            if idx > 0:
                # Add half the time elapsed since previous trackpoint
                duration = (dt - time_objects[idx - 1]) / 2
            else:
                duration = timedelta(0)
            if idx < last_index:
                # Add half the time to next trackpoint
                duration += (time_objects[idx + 1] - dt) / 2
            durations.append(duration)
        return durations

    def cadence_values(self):
        return [
            int(x.text)
            for x in self.root.xpath("//ns:Cadence", namespaces={"ns": namespace})
        ]

    def power_values(self):
        return [
            int(x.text)
            for x in self.root.xpath("//ns:TPX/ns:Watts", namespaces={"ns": namespace2})
        ]

    def steps_values(self):
        return [
            int(x.text)
            for x in self.root.xpath("//ns:Steps", namespaces={"ns": namespace2})
        ]

    @property
    def latitude(self):
        if hasattr(self.activity.Lap.Track.Trackpoint, "Position"):
            return self.activity.Lap.Track.Trackpoint.Position.LatitudeDegrees.pyval

    @property
    def longitude(self):
        if hasattr(self.activity.Lap.Track.Trackpoint, "Position"):
            return self.activity.Lap.Track.Trackpoint.Position.LongitudeDegrees.pyval

    @property
    def activity_type(self):
        return self.activity.attrib["Sport"].lower()

    @property
    def started_at(self):
        return self.activity.Lap[0].attrib["StartTime"]

    @property
    def completed_at(self):
        return self.activity.Lap[-1].Track.Trackpoint[-1].Time.pyval

    @property
    def cadence_avg(self):
        return (
            self.activity.Lap[-1].Cadence
            if hasattr(self.activity.Lap[-1], "Cadence")
            else None
        )

    @property
    def distance(self):
        distance_values = self.distance_values()
        return distance_values[-1] if distance_values else 0

    @property
    def distance_units(self):
        return "meters"

    @property
    def duration(self):
        """Returns duration of workout in seconds."""
        return sum(lap.TotalTimeSeconds for lap in self.activity.Lap)

    @property
    def calories(self):
        return sum(lap.Calories for lap in self.activity.Lap)

    @property
    def hr_avg(self):
        """Average heart rate of the workout"""
        hr_data = self.hr_values()
        return int(sum(hr_data) / len(hr_data)) if hr_data else None

    @property
    def hr_max(self):
        """Maximum heart rate of the workout"""
        return max(self.hr_values()) if self.hr_values() else None

    @property
    def hr_min(self):
        """Minimum heart rate of the workout"""
        return min(self.hr_values()) if self.hr_values() else None

    def hr_percent_in_zones(self, zones):
        """Percentage of workout spent in each heart rate zone.

        Given these user's heart rate zones:
        zones = {
            "Z0": (0, 119),
            "Z1": (120, 199),
            "Z2": (200, 240),
        }

        Then `self.hr_percent_in_zones(zones)` would return something like:
        {
            "Z0": 5,
            "Z1": 95,
            "Z2": 0,
        }

        Correct calculation relies on evenly spaced measurement times.
        """
        hr_values = self.hr_values()
        if not hr_values:
            raise NoHeartRateDataError

        # Initialize a dictionary with one item for each zone
        per_zone = dict.fromkeys(zones.keys(), 0)

        # count number of HR measurements per zone
        for hr in hr_values:
            for zone_name, zone_boundaries in zones.items():
                if hr >= zone_boundaries[0] and hr <= zone_boundaries[1]:
                    per_zone[zone_name] += 1

        # convert counts to percentages
        nr_hr_values = len(hr_values)
        for name, count in per_zone.items():
            per_zone[name] = round(100 * count / nr_hr_values)
        return per_zone

    def hr_time_in_zones(self, zones):
        """Time spent in each heart rate zone.

        Given these user's heart rate zones:
        zones = {
            "Z0": (0, 119),
            "Z1": (120, 199),
            "Z2": (200, 240),
        }

        Then `self.hr_time_in_zones(zones)` would return something like:
        {
            "Z0": timedelta(seconds=3600),
            "Z1": timedelta(seconds=1800),
            "Z2": timedelta(seconds=300),
        }
        """
        hr_values = self.hr_values()
        if not hr_values:
            raise NoHeartRateDataError

        # Initialize a dictionary with time=0 for each zone
        per_zone = dict.fromkeys(zones.keys(), timedelta(0))

        # count number of HR measurements per zone
        for hr, td in zip(hr_values, self.time_durations()):
            for zone_name, zone_boundaries in zones.items():
                if hr >= zone_boundaries[0] and hr <= zone_boundaries[1]:
                    per_zone[zone_name] += td

        return per_zone

    @property
    def pace(self):
        """Average pace (mm:ss/km for the workout"""
        secs_per_km = self.duration / (self.distance / 1000)
        return time.strftime("%M:%S", time.gmtime(secs_per_km))

    @property
    def altitude_avg(self):
        """Average altitude for the workout"""
        altitude_data = self.altitude_points()
        return sum(altitude_data) / len(altitude_data)

    @property
    def altitude_max(self):
        """Max altitude for the workout"""
        altitude_data = self.altitude_points()
        return max(altitude_data)

    @property
    def altitude_min(self):
        """Min altitude for the workout"""
        altitude_data = self.altitude_points()
        return min(altitude_data)

    @property
    def ascent(self):
        """Returns ascent of workout in meters"""
        total_ascent = 0.0
        altitude_data = self.altitude_points()
        for i in range(len(altitude_data) - 1):
            diff = altitude_data[i + 1] - altitude_data[i]
            if diff > 0.0:
                total_ascent += diff
        return total_ascent

    @property
    def descent(self):
        """Returns descent of workout in meters"""
        total_descent = 0.0
        altitude_data = self.altitude_points()
        for i in range(len(altitude_data) - 1):
            diff = altitude_data[i + 1] - altitude_data[i]
            if diff < 0.0:
                total_descent += abs(diff)
        return total_descent

    @property
    def cadence_max(self):
        """Returns max cadence of workout"""
        cadence_data = self.cadence_values()
        return max(cadence_data) if cadence_data else None

    @property
    def activity_notes(self):
        """Return contents of Activity/Notes field if it exists."""
        return getattr(self.activity, "Notes", "")

    @property
    def power_max(self):
        """Returns max power (in watts) of workout"""
        power_data = self.power_values()
        return max(power_data) if power_data else None

    @property
    def power_avg(self):
        """Returns avg power (in watts) of workout"""
        power_data = self.power_values()
        return int((sum(power_data) / len(power_data))) if power_data else None

    @property
    def total_steps(self):
        """Returns total steps (strokes) of workout"""
        step_data = self.steps_values()
        return sum(step_data)
