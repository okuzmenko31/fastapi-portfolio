from celery import Celery

app = Celery('src.settings', broker='amqp://guest:guest@rabbitmq//')
app.autodiscover_tasks()
