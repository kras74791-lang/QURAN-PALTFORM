from django.contrib import admin
from .models import Surah, Ayah, Bookmark, AyahNote, ReadingHistory


@admin.register(Surah)
class SurahAdmin(admin.ModelAdmin):
    list_display = ('number', 'name_english', 'name_arabic', 'ayah_count', 'revelation_place')
    list_filter = ('revelation_place', 'revelation_order')
    search_fields = ('name_english', 'name_arabic', 'name_transliteration')
    ordering = ('number',)


@admin.register(Ayah)
class AyahAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'surah', 'number', 'sajdah_type')
    list_filter = ('surah', 'sajdah_type')
    search_fields = ('text_arabic', 'text_english', 'text_russian')


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'ayah', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email',)


@admin.register(AyahNote)
class AyahNoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'ayah', 'created_at', 'updated_at')
    list_filter = ('created_at', 'color')
    search_fields = ('user__email', 'note_text')


@admin.register(ReadingHistory)
class ReadingHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'surah', 'ayah_from', 'ayah_to', 'read_at')
    list_filter = ('read_at', 'surah')
    search_fields = ('user__email',)
