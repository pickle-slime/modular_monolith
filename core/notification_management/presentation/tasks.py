from celery import shared_task
from core.notification_management.application.services.external.notification_management import MailchipService 
from .notification_management.models import CommonMailingList

@shared_task
def send_email_monthly_task(subject, from_name, reply_to, audience_id, html_content):
    subscribers = CommonMailingList.objects.iterator()
    service = MailchipService()
    # Iterate through subscribers and send email
    for subscriber in subscribers:
        reply_to = subscriber.email
        # Send email to each subscriber using the email sending function
        service.send_email_to_audience(subject, from_name, reply_to, audience_id, html_content)
    
    return f"Emails sent to {subscribers.count()} subscribers."




