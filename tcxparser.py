"Simple parser for Garmin TCX files."

from lxml import objectify


class TCXParser:

    def __init__(self, tcx_file):
        tree = objectify.parse(tcx_file)
        self.root = tree.getroot()
        self.activity = self.root.Activities.Activity

    def hr_values(self):
        hr = []
        for lap in self.activity.Lap:
            for trackpoint in lap.Track.Trackpoint:
                if hasattr(trackpoint, 'HeartRateBpm'):
                    hr.append(trackpoint.HeartRateBpm.Value.pyval)
        return hr

    @property
    def latitude(self):
        return self.activity.Lap.Track.Trackpoint.Position.LatitudeDegrees.pyval

    @property
    def longitude(self):
        return self.activity.Lap.Track.Trackpoint.Position.LongitudeDegrees.pyval

    @property
    def activity_type(self):
        return self.activity.attrib['Sport'].lower()

    @property
    def completed_at(self):
        return self.activity.Lap[-1].Track.Trackpoint[-1].Time.pyval

    @property
    def distance(self):
        return self.activity.Lap[-1].Track.Trackpoint[-2].DistanceMeters.pyval

    @property
    def distance_units(self):
        return 'meters'

    @property
    def duration(self):
        """Returns duration of workout in seconds."""
        return sum(lap.TotalTimeSeconds for lap in self.activity.Lap)

    @property
    def calories(self):
        return sum(lap.Calories for lap in self.activity.Lap)
        
    @property
    def lap_count(self):
        return len(self.activity.Lap)

    @property
    def hr_avg(self):
        hr_data = self.hr_values()
        return sum(hr_data)/len(hr_data)
        
    @property
    def hr_max(self):
        return max(self.hr_values())
        
    @property
    def hr_min(self):
        return min(self.hr_values())
        