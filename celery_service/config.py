import os

class MailServiceConfig:
    DEBUG = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


class CeleryConfig:
    CELERY_APP_NAME = 'tasks'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
