import os
from celery import Celery
from django.conf import settings


# задаем переменную окружения, содержащую название файла настроек нашего проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'internet_shop.settings')


app = Celery('internet_shop')


# загружаем конфигурацию из настроек прокта
app.config_from_object('django.conf:settings')
# запускаем процесс поиска и загрузки асинхронных задач по проекту
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)