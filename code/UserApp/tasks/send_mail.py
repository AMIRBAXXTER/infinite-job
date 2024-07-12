from config.celery_base import app
from django.core.mail import send_mail
from django.conf import settings


@app.task(queue='mail', autoretry_for=(Exception,),default_retry_delay=5, retry_kwargs={'max_retries': 10})
def send_mail_task(subject, message, to):
    send_mail(subject, message, settings.EMAIL_HOST_USER, to)
