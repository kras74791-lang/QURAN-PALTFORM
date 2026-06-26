from django.contrib import admin
from .models import Qari, QariAudio, AyahTimestamp, ListeningHistory, QariRating


@admin.register(Qari)
class QariAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'style', 'rating', 'total_ratings', 'is_active')
    list_filter = ('style', 'is_active', 'country')
    search_fields = ('name', 'bio')


@admin.register(QariAudio)
class QariAudioAdmin(admin.ModelAdmin):
    list_display = ('qari', 'surah_number', 'duration', 'file_size')
    list_filter = ('qari', 'surah_number')
    search_fields = ('qari__name',)


@admin.register(AyahTimestamp)
class AyahTimestampAdmin(admin.ModelAdmin):
    list_display = ('qari', 'surah_number', 'ayah_number', 'start_time', 'end_time')
    list_filter = ('qari', 'surah_number')
    search_fields = ('qari__name',)


@admin.register(ListeningHistory)
class ListeningHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'qari', 'surah_number', 'duration_seconds', 'listened_at')
    list_filter = ('listened_at', 'qari', 'surah_number')
    search_fields = ('user__email', 'qari__name')


@admin.register(QariRating)
class QariRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'qari', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__email', 'qari__name')
