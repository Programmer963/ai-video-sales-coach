from celery import Celery
from app.core.config import settings

# Create Celery instance
celery_app = Celery(
    "sales_coach",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=['app.tasks']  # Include task modules
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Optional: Add task routes for different queues
celery_app.conf.task_routes = {
    'app.tasks.process_video': {'queue': 'video_processing'},
    'app.tasks.analyze_emotions': {'queue': 'ai_analysis'},
    'app.tasks.analyze_speech': {'queue': 'ai_analysis'},
}

if __name__ == '__main__':
    celery_app.start() 