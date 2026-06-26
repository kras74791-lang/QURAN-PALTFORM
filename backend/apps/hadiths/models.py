from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class HadithCollection(models.Model):
    """Hadith Collection Sources"""
    COLLECTIONS = [
        ('bukhari', 'Sahih Bukhari'),
        ('muslim', 'Sahih Muslim'),
        ('abu_dawood', 'Abu Dawood'),
        ('tirmidhi', 'Tirmidhi'),
        ('nasai', 'An-Nasai'),
        ('ibn_majah', 'Ibn Majah'),
    ]
    
    name = models.CharField(max_length=100, unique=True, choices=COLLECTIONS)
    description = models.TextField(blank=True, null=True)
    total_hadiths = models.IntegerField(default=0)
    compiler_name = models.CharField(max_length=100, blank=True, null=True)
    compiler_bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hadith_collections'
        verbose_name = 'Hadith Collection'
        verbose_name_plural = 'Hadith Collections'

    def __str__(self):
        return self.get_name_display()


class HadithCategory(models.Model):
    """Categories/Topics for Hadiths"""
    CATEGORIES = [
        ('aqida', 'Aqida (Belief)'),
        ('ibadah', 'Ibadah (Worship)'),
        ('salah', 'Salah (Prayer)'),
        ('sawm', 'Sawm (Fasting)'),
        ('hajj', 'Hajj (Pilgrimage)'),
        ('zakat', 'Zakat (Charity)'),
        ('manners', 'Manners & Etiquette'),
        ('family', 'Family & Relations'),
        ('business', 'Business & Commerce'),
        ('medicine', 'Medicine & Health'),
        ('knowledge', 'Knowledge & Learning'),
        ('jihad', 'Jihad & Military'),
    ]
    
    name = models.CharField(max_length=100, unique=True, choices=CATEGORIES)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hadith_categories'
        verbose_name = 'Hadith Category'
        verbose_name_plural = 'Hadith Categories'

    def __str__(self):
        return self.get_name_display()


class Hadith(models.Model):
    """Individual Hadith"""
    AUTHENTICITY_CHOICES = [
        ('sahih', 'Sahih (Authentic)'),
        ('hasan', 'Hasan (Good)'),
        ('daif', 'Daif (Weak)'),
        ('maudu', 'Maudu (Fabricated)'),
    ]
    
    collection = models.ForeignKey(HadithCollection, on_delete=models.CASCADE, related_name='hadiths')
    category = models.ForeignKey(HadithCategory, on_delete=models.CASCADE, related_name='hadiths')
    number = models.CharField(max_length=50)  # e.g., "1234"
    text_arabic = models.TextField()
    text_english = models.TextField()
    text_russian = models.TextField()
    authenticity = models.CharField(max_length=20, choices=AUTHENTICITY_CHOICES)
    narrator_chain = models.TextField(blank=True, null=True)  # Isnad
    commentary = models.TextField(blank=True, null=True)
    chapter_name = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hadiths'
        verbose_name = 'Hadith'
        verbose_name_plural = 'Hadiths'
        unique_together = ('collection', 'number')
        indexes = [
            models.Index(fields=['collection', 'category']),
        ]

    def __str__(self):
        return f'{self.collection.get_name_display()} - {self.number}'


class HadithNarrator(models.Model):
    """Narrators in the chain of transmission"""
    hadith = models.ForeignKey(Hadith, on_delete=models.CASCADE, related_name='narrators')
    narrator_name = models.CharField(max_length=200)
    order = models.IntegerField()  # Position in chain
    biography = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'hadith_narrators'
        verbose_name = 'Hadith Narrator'
        verbose_name_plural = 'Hadith Narrators'

    def __str__(self):
        return self.narrator_name


class UserHadithBookmark(models.Model):
    """User bookmarked hadiths"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hadith_bookmarks')
    hadith = models.ForeignKey(Hadith, on_delete=models.CASCADE, related_name='bookmarks')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_hadith_bookmarks'
        verbose_name = 'User Hadith Bookmark'
        verbose_name_plural = 'User Hadith Bookmarks'
        unique_together = ('user', 'hadith')

    def __str__(self):
        return f'{self.user.email} - {self.hadith}'


class HadithRating(models.Model):
    """User ratings for hadiths"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hadith_ratings')
    hadith = models.ForeignKey(Hadith, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(
        choices=[
            (1, '1 Star'),
            (2, '2 Stars'),
            (3, '3 Stars'),
            (4, '4 Stars'),
            (5, '5 Stars'),
        ]
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hadith_ratings'
        verbose_name = 'Hadith Rating'
        verbose_name_plural = 'Hadith Ratings'
        unique_together = ('user', 'hadith')

    def __str__(self):
        return f'{self.user.email} - {self.hadith}'
