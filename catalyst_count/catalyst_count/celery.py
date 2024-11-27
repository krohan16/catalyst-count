from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
project_name="catalyst_count"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{project_name}.settings")
app = Celery(project_name)
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')