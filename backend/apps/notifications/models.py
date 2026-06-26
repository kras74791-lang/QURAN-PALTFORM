from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Notification(models.Model):
    """In-app notifications"""
    NOTIFICATION_TYPES = [
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    action_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.email} - {self.title}'


class EmailLog(models.Model):
    """Log sent emails"""
    EMAIL_TYPES = [
        ('verification', 'Email Verification'),
        ('password_reset', 'Password Reset'),
        ('daily_dua', 'Daily Dua'),
        ('reading_reminder', 'Reading Reminder'),
        ('newsletter', 'Newsletter'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_logs')
    email_type = models.CharField(max_length=50, choices=EMAIL_TYPES)
    recipient_email = models.EmailField()
    subject = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('sent', 'Sent'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    error_message = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'email_logs'
        verbose_name = 'Email Log'
        verbose_name_plural = 'Email Logs'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.email_type} - {self.recipient_email}'


class PushNotificationSubscription(models.Model):
    """Store push notification subscriptions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='push_subscriptions')
    endpoint = models.URLField()
    auth_key = models.CharField(max_length=255)
    p256dh = models.CharField(max_length=255)
    browser = models.CharField(max_length=50, blank=True, null=True)
    device_type = models.CharField(
        max_length=20,
        choices=[
            ('desktop', 'Desktop'),
            ('mobile', 'Mobile'),
            ('tablet', 'Tablet'),
        ],
        blank=True, null=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'push_notification_subscriptions'
        verbose_name = 'Push Notification Subscription'
        verbose_name_plural = 'Push Notification Subscriptions'
        unique_together = ('user', 'endpoint')

    def __str__(self):
        return f'{self.user.email} - {self.device_type}'
