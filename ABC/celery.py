from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Установите значение переменной окружения DJANGO_SETTINGS_MODULE по умолчанию.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ABC.settings')

app = Celery('ABC')

# Используйте строку подключения к брокеру сообщений из настроек Django.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Загрузите задачи из всех зарегистрированных приложений Django.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
