from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

from app.core.config import settings

load_dotenv()

app = Celery("tasks", broker=settings.REDIS_URI)
app.autodiscover_tasks(["app.celery_loans.tasks", "kafka_core.handlers"])

app.conf.beat_schedule = {
    "my_task": {"task": "my_task", "schedule": crontab(minute="*/1")},
}
