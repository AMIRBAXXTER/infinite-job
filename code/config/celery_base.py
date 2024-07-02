from celery import Celery

app = Celery('infinite-job')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
