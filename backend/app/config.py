import os

class Config:
    DEBUG = False

    CELERY_BROKER_URL = os.getenv('REDISCLOUD_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('REDISCLOUD_URL', 'redis://localhost:6379/0')
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
