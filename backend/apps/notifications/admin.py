from django.contrib import admin
from .models import Notification, EmailLog, PushNotificationSubscription


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__email', 'title', 'message')


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_type', 'recipient_email', 'status', 'sent_at')
    list_filter = ('email_type', 'status', 'created_at')
    search_fields = ('user__email', 'recipient_email', 'subject')


@admin.register(PushNotificationSubscription)
class PushNotificationSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'device_type', 'browser', 'is_active', 'created_at')
    list_filter = ('device_type', 'is_active', 'created_at')
    search_fields = ('user__email',)
