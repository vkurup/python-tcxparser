"Simple parser for Garmin TCX files."

from lxml import objectify

__version__ = '0.1.0'


class TcxParser:

    def __init__(self, tcx_file):
        tree = objectify.parse(tcx_file)
        self.root = tree.getroot()
        self.activity = self.root.Activities.Activity

    def latitude(self):
        return self.activity.Lap.Track.Trackpoint.Position.LatitudeDegrees

    def longitude(self):
        return self.activity.Lap.Track.Trackpoint.Position.LongitudeDegrees

    def activity_type(self):
        return self.activity.attrib['Sport'].lower()

    def completed_at(self):
        return self.activity.Lap[-1].Track.Trackpoint[-1].Time

    def distance(self):
        return self.activity.Lap[-1].Track.Trackpoint[-2].DistanceMeters

    def distance_units(self):
        return 'meters'

    def duration(self):
        """Returns duration of workout in seconds."""
        return sum(lap.TotalTimeSeconds for lap in self.activity.Lap)

    def calories(self):
        return sum(lap.Calories for lap in self.activity.Lap)
