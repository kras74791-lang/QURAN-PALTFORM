from django.contrib import admin
from .models import QiblaLocation, QiblaCalculationHistory


@admin.register(QiblaLocation)
class QiblaLocationAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'country', 'location_source', 'updated_at')
    list_filter = ('location_source', 'updated_at')
    search_fields = ('user__email', 'city', 'country')


@admin.register(QiblaCalculationHistory)
class QiblaCalculationHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'qibla_bearing', 'distance_to_mecca', 'calculated_at')
    list_filter = ('calculated_at',)
    search_fields = ('user__email',)
