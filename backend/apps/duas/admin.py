from django.contrib import admin
from .models import DuaCategory, Dua, UserDuaCollection


@admin.register(DuaCategory)
class DuaCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')


@admin.register(Dua)
class DuaAdmin(admin.ModelAdmin):
    list_display = ('category', 'is_featured', 'reference', 'order', 'created_at')
    list_filter = ('category', 'is_featured', 'created_at')
    search_fields = ('text_arabic', 'text_english', 'text_russian', 'reference')


@admin.register(UserDuaCollection)
class UserDuaCollectionAdmin(admin.ModelAdmin):
    list_display = ('user', 'dua', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__email', 'dua__text_arabic')
