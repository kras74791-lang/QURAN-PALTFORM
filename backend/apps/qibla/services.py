"""
Qibla direction calculation service using Haversine formula
"""
import math
from decimal import Decimal


class QiblaCalculator:
    """Calculate Qibla direction from given coordinates"""
    
    # Kaaba coordinates
    MECCA_LATITUDE = Decimal('21.4225')
    MECCA_LONGITUDE = Decimal('39.8262')
    EARTH_RADIUS_KM = 6371  # Earth radius in kilometers
    
    @classmethod
    def calculate_bearing(cls, lat1, lon1, lat2, lon2):
        """
        Calculate bearing between two coordinates using Haversine formula
        
        Args:
            lat1, lon1: User's latitude and longitude (float or Decimal)
            lat2, lon2: Destination latitude and longitude (float or Decimal)
            
        Returns:
            Bearing in degrees (0-360)
        """
        lat1 = float(lat1)
        lon1 = float(lon1)
        lat2 = float(lat2)
        lon2 = float(lon2)
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        dlon = math.radians(lon2 - lon1)
        
        x = math.sin(dlon) * math.cos(lat2_rad)
        y = math.cos(lat1_rad) * math.sin(lat2_rad) - \
            math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon)
        
        bearing = math.atan2(x, y)
        bearing = math.degrees(bearing)
        bearing = (bearing + 360) % 360
        
        return bearing
    
    @classmethod
    def calculate_distance(cls, lat1, lon1, lat2, lon2):
        """
        Calculate distance between two coordinates using Haversine formula
        
        Args:
            lat1, lon1: User's latitude and longitude
            lat2, lon2: Destination latitude and longitude
            
        Returns:
            Distance in kilometers
        """
        lat1 = float(lat1)
        lon1 = float(lon1)
        lat2 = float(lat2)
        lon2 = float(lon2)
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = math.sin(dlat / 2) ** 2 + \
            math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        distance = cls.EARTH_RADIUS_KM * c
        
        return distance
    
    @classmethod
    def calculate_qibla(cls, latitude, longitude):
        """
        Calculate Qibla direction and distance to Mecca
        
        Args:
            latitude: User's latitude
            longitude: User's longitude
            
        Returns:
            dict with bearing and distance
        """
        bearing = cls.calculate_bearing(latitude, longitude, cls.MECCA_LATITUDE, cls.MECCA_LONGITUDE)
        distance = cls.calculate_distance(latitude, longitude, cls.MECCA_LATITUDE, cls.MECCA_LONGITUDE)
        
        # Convert bearing to compass direction
        compass_direction = cls.bearing_to_compass(bearing)
        
        return {
            'bearing': round(bearing, 2),
            'compass_direction': compass_direction,
            'distance_km': round(distance, 2),
        }
    
    @staticmethod
    def bearing_to_compass(bearing):
        """Convert bearing in degrees to compass direction"""
        compass_points = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                         'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        
        # Each point is 22.5 degrees
        index = round(bearing / 22.5) % 16
        return compass_points[index]
