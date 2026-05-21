from celery import Celery
from pipeline.config import settings

celery_app = Celery(
    "vn30_pipeline",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Ho_Chi_Minh",
    enable_utc=False,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)

celery_app.conf.beat_schedule = {
    "daily-close-pipeline": {
        "task": "pipeline.tasks.daily_close.daily_close_pipeline",
        "schedule": {"hour": settings.daily_close_hour, "minute": settings.daily_close_minute},
    },
    "daily-tcbs-pipeline": {
        "task": "pipeline.tasks.daily_tcbs.daily_tcbs_pipeline",
        "schedule": {"hour": settings.daily_close_hour, "minute": settings.daily_close_minute + 2},
    },
    "daily-scoring-pipeline": {
        "task": "pipeline.tasks.daily_score.daily_scoring_pipeline",
        "schedule": {"hour": settings.daily_close_hour, "minute": settings.daily_close_minute + 5},
    },
    "daily-open-pipeline": {
        "task": "pipeline.tasks.daily_open.daily_open_pipeline",
        "schedule": {"hour": settings.daily_open_hour, "minute": settings.daily_open_minute},
    },
}
