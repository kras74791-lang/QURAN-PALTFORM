"""
Celery tasks for notifications
"""
from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import EmailLog
from apps.duas.models import Dua
import random

User = get_user_model()


@shared_task
def send_daily_dua_notification():
    """Send daily dua notification to users"""
    # Get random dua
    dua = Dua.objects.filter(is_featured=True).order_by('?').first()
    
    if not dua:
        dua = Dua.objects.order_by('?').first()
    
    if not dua:
        return
    
    users = User.objects.filter(
        profile__notifications_enabled=True,
        profile__email_notifications=True,
        is_email_verified=True
    )
    
    for user in users:
        subject = f"Daily Dua - {dua.category.name}"
        message = f"""
        Peace be upon you,
        
        Today's Dua:
        
        Arabic: {dua.text_arabic}
        English: {dua.text_english}
        Russian: {dua.text_russian}
        
        May your day be blessed!
        """
        
        try:
            send_mail(
                subject,
                message,
                'noreply@quranplatform.com',
                [user.email],
                fail_silently=False,
            )
            EmailLog.objects.create(
                user=user,
                email_type='daily_dua',
                recipient_email=user.email,
                subject=subject,
                status='sent'
            )
        except Exception as e:
            EmailLog.objects.create(
                user=user,
                email_type='daily_dua',
                recipient_email=user.email,
                subject=subject,
                status='failed',
                error_message=str(e)
            )


@shared_task
def send_reading_reminder():
    """Send reading reminder to users"""
    users = User.objects.filter(
        profile__notifications_enabled=True,
        profile__email_notifications=True,
        is_email_verified=True
    )
    
    for user in users:
        subject = "Time to Read the Quran 📖"
        message = """
        Peace be upon you,
        
        This is a gentle reminder to spend some time reading the Quran.
        
        The Quran is a source of guidance, healing, and peace.
        
        Visit our platform to continue your reading: https://quranplatform.com
        """
        
        try:
            send_mail(
                subject,
                message,
                'noreply@quranplatform.com',
                [user.email],
                fail_silently=False,
            )
            EmailLog.objects.create(
                user=user,
                email_type='reading_reminder',
                recipient_email=user.email,
                subject=subject,
                status='sent'
            )
        except Exception as e:
            EmailLog.objects.create(
                user=user,
                email_type='reading_reminder',
                recipient_email=user.email,
                subject=subject,
                status='failed',
                error_message=str(e)
            )


@shared_task
def send_email_async(user_id, subject, message, email_type='other'):
    """Send email asynchronously"""
    try:
        user = User.objects.get(id=user_id)
        send_mail(
            subject,
            message,
            'noreply@quranplatform.com',
            [user.email],
            fail_silently=False,
        )
        EmailLog.objects.create(
            user=user,
            email_type=email_type,
            recipient_email=user.email,
            subject=subject,
            status='sent'
        )
    except User.DoesNotExist:
        pass
    except Exception as e:
        EmailLog.objects.create(
            user=user,
            email_type=email_type,
            recipient_email=user.email,
            subject=subject,
            status='failed',
            error_message=str(e)
        )
