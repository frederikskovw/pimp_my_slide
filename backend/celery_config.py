import os

CELERY_BROKER_URL = os.environ.get('REDISCLOUD_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('REDISCLOUD_URL', 'redis://localhost:6379/0')
