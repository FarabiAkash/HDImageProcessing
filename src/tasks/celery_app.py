"""
celery_app.py
Configures the Celery application.
"""

import os
from celery import Celery

# Example broker and backend (using Redis); adapt to your environment
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

celery = Celery(
    'image_processing_tasks',
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)

# Optional: Load custom config from a file or environment
celery.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
    # Additional config as needed
)

# Example usage:
# from src.tasks.async_tasks import heavy_pca
# heavy_pca.delay(image_id, n_components)
