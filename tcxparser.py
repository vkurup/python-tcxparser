"Simple parser for Garmin TCX files."

import time
from lxml import objectify

namespace = 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'

class TCXParser:

    def __init__(self, tcx_file):
        tree = objectify.parse(tcx_file)
        self.root = tree.getroot()
        self.activity = self.root.Activities.Activity
        
    def hr_values(self):
        return [int(x.text) for x in self.root.xpath('//ns:HeartRateBpm/ns:Value', namespaces={'ns': namespace})]

    def altitude_points(self):
        return [float(x.text) for x in self.root.xpath('//ns:AltitudeMeters', namespaces={'ns': namespace})]
      
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
    def hr_avg(self):
        """Average heart rate of the workout"""
        hr_data = self.hr_values()
        try:
	  hr = sum(hr_data)/len(hr_data)    
	except Exception as e:
	  hr = e
	return hr
        
    @property
    def hr_max(self):
        """Minimum heart rate of the workout"""
        return max(self.hr_values())
        
    @property
    def hr_min(self):
        """Minimum heart rate of the workout"""
        return min(self.hr_values())
        
    @property
    def pace(self):
        """Average pace (mm:ss/km for the workout"""
        secs_per_km = self.duration/(self.distance/1000)
        return time.strftime('%M:%S', time.gmtime(secs_per_km))
    
    @property
    def altitude_avg(self):
        """Average altitude for the workout"""
        altitude_data = self.altitude_points()
        return sum(altitude_data)/len(altitude_data)
    
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
	  diff = altitude_data[i+1] - altitude_data[i] 
	  if diff > 0.0:
	    total_ascent += diff
        return total_ascent
    
    @property 
    def descent(self):
        """Returns descent of workout in meters"""
	total_descent = 0.0
        altitude_data = self.altitude_points()
        for i in range(len(altitude_data) - 1):
	  diff = altitude_data[i+1] - altitude_data[i] 
	  if diff < 0.0:
	    total_descent += abs(diff)
        return total_descent   