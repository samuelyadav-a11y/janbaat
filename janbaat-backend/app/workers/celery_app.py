from celery import Celery
from celery.schedules import crontab

from app.config import settings

celery = Celery(
    "janbaat",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=[
        "app.workers.ai_tasks",
        "app.workers.notification_tasks",
        "app.workers.feed_tasks",
    ],
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
    task_track_started=True,
    worker_prefetch_multiplier=1,
)

# ─── Scheduled Tasks (Celery Beat) ───────────────────────────────────────────
celery.conf.beat_schedule = {
    # Every 5 min: update district dashboards
    "update-dashboards": {
        "task": "app.workers.feed_tasks.compute_dashboards",
        "schedule": crontab(minute="*/5"),
    },
    # Daily at 2am IST: full re-cluster + AI summaries
    "daily-recluster": {
        "task": "app.workers.ai_tasks.run_daily_recluster",
        "schedule": crontab(hour=2, minute=0),
    },
    # Daily at 3am IST: warm feed caches
    "warm-feed-caches": {
        "task": "app.workers.feed_tasks.warm_feed_caches",
        "schedule": crontab(hour=3, minute=0),
    },
}
