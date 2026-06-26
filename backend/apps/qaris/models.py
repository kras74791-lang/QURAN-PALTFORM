from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Qari(models.Model):
    """Quranic Reciter"""
    RECITATION_STYLES = [
        ('tajweed', 'Tajweed'),
        ('muraatil', 'Muraatil'),
        ('muallim', 'Muallim'),
        ('normal', 'Normal'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='qaris/', null=True, blank=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    style = models.CharField(max_length=20, choices=RECITATION_STYLES, default='normal')
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    total_ratings = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'qaris'
        verbose_name = 'Qari'
        verbose_name_plural = 'Qaris'
        ordering = ['-rating']

    def __str__(self):
        return self.name


class QariAudio(models.Model):
    """Audio file for each Qari's Surah"""
    qari = models.ForeignKey(Qari, on_delete=models.CASCADE, related_name='audio_files')
    surah_number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(114)])
    audio_file = models.FileField(upload_to='qari_audio/')
    duration = models.IntegerField(help_text='Duration in seconds')
    file_size = models.BigIntegerField(help_text='File size in bytes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'qari_audios'
        verbose_name = 'Qari Audio'
        verbose_name_plural = 'Qari Audios'
        unique_together = ('qari', 'surah_number')

    def __str__(self):
        return f'{self.qari.name} - Surah {self.surah_number}'


class AyahTimestamp(models.Model):
    """Timestamps for each Ayah in Qari's audio"""
    qari = models.ForeignKey(Qari, on_delete=models.CASCADE, related_name='timestamps')
    surah_number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(114)])
    ayah_number = models.IntegerField()
    start_time = models.FloatField(help_text='Start time in seconds')
    end_time = models.FloatField(help_text='End time in seconds')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ayah_timestamps'
        verbose_name = 'Ayah Timestamp'
        verbose_name_plural = 'Ayah Timestamps'
        unique_together = ('qari', 'surah_number', 'ayah_number')
        indexes = [
            models.Index(fields=['qari', 'surah_number']),
        ]

    def __str__(self):
        return f'{self.qari.name} - {self.surah_number}:{self.ayah_number}'


class ListeningHistory(models.Model):
    """Track user audio listening sessions"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listening_history')
    qari = models.ForeignKey(Qari, on_delete=models.CASCADE)
    surah_number = models.IntegerField()
    duration_seconds = models.IntegerField()
    listened_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'listening_history'
        verbose_name = 'Listening History'
        verbose_name_plural = 'Listening Histories'

    def __str__(self):
        return f'{self.user.email} - {self.qari.name} ({self.listened_at})'


class QariRating(models.Model):
    """User ratings for Qaris"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='qari_ratings')
    qari = models.ForeignKey(Qari, on_delete=models.CASCADE, related_name='user_ratings')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'qari_ratings'
        verbose_name = 'Qari Rating'
        verbose_name_plural = 'Qari Ratings'
        unique_together = ('user', 'qari')

    def __str__(self):
        return f'{self.user.email} rated {self.qari.name} - {self.rating}★'
