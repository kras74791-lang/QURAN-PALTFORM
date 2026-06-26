from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class QiblaLocation(models.Model):
    """Store user location data for Qibla calculation"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='qibla_location')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    location_source = models.CharField(
        max_length=20,
        choices=[
            ('gps', 'GPS'),
            ('ip', 'IP Address'),
            ('manual', 'Manual Entry'),
        ],
        default='manual'
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'qibla_locations'
        verbose_name = 'Qibla Location'
        verbose_name_plural = 'Qibla Locations'

    def __str__(self):
        return f'{self.user.email} - {self.city}, {self.country}'


class QiblaCalculationHistory(models.Model):
    """Track Qibla calculations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='qibla_calculations')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    qibla_bearing = models.FloatField()  # Bearing in degrees
    distance_to_mecca = models.FloatField(help_text='Distance in kilometers')
    accuracy = models.IntegerField(null=True, blank=True, help_text='GPS accuracy in meters')
    calculated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'qibla_calculation_history'
        verbose_name = 'Qibla Calculation'
        verbose_name_plural = 'Qibla Calculations'

    def __str__(self):
        return f'{self.user.email} - {self.qibla_bearing}°'
