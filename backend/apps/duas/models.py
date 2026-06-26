from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class DuaCategory(models.Model):
    """Categories for Duas"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.ImageField(upload_to='dua_icons/', null=True, blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dua_categories'
        verbose_name = 'Dua Category'
        verbose_name_plural = 'Dua Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Dua(models.Model):
    """Duas (Supplications)"""
    category = models.ForeignKey(DuaCategory, on_delete=models.CASCADE, related_name='duas')
    text_arabic = models.TextField()
    text_english = models.TextField()
    text_russian = models.TextField()
    transliteration = models.TextField()
    audio_file = models.FileField(upload_to='duas_audio/', null=True, blank=True)
    reference = models.CharField(max_length=255, blank=True, null=True)  # e.g., "Quran 2:201"
    benefits = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'duas'
        verbose_name = 'Dua'
        verbose_name_plural = 'Duas'
        ordering = ['-is_featured', 'category', 'order']

    def __str__(self):
        return f'{self.category.name} - {self.text_arabic[:50]}'


class UserDuaCollection(models.Model):
    """User saved duas"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dua_collections')
    dua = models.ForeignKey(Dua, on_delete=models.CASCADE, related_name='user_collections')
    added_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'user_dua_collections'
        verbose_name = 'User Dua Collection'
        verbose_name_plural = 'User Dua Collections'
        unique_together = ('user', 'dua')

    def __str__(self):
        return f'{self.user.email} - {self.dua}'
