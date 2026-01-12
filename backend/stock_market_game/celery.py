import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_market_game.settings')

app = Celery('stock_market_game')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
