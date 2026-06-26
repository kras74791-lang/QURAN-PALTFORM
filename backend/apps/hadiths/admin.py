from django.contrib import admin
from .models import (
    HadithCollection, HadithCategory, Hadith, 
    HadithNarrator, UserHadithBookmark, HadithRating
)


@admin.register(HadithCollection)
class HadithCollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_hadiths', 'compiler_name', 'created_at')
    search_fields = ('name', 'compiler_name')


@admin.register(HadithCategory)
class HadithCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Hadith)
class HadithAdmin(admin.ModelAdmin):
    list_display = ('number', 'collection', 'category', 'authenticity', 'created_at')
    list_filter = ('collection', 'category', 'authenticity', 'created_at')
    search_fields = ('text_arabic', 'text_english', 'text_russian', 'number')


class HadithNarratorInline(admin.TabularInline):
    model = HadithNarrator
    extra = 1


@admin.register(UserHadithBookmark)
class UserHadithBookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'hadith', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'hadith__number')


@admin.register(HadithRating)
class HadithRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'hadith', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__email', 'hadith__number')
