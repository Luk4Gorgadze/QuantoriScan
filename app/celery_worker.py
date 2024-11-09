from celery import Celery  # tpye: ignore

celery = Celery(
    'app.celery_worker',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

celery.conf.update(task_track_started=True)
celery.autodiscover_tasks(['app.tasks'])
