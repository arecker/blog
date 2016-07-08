from celery.task.schedules import crontab
from celery.decorators import periodic_task
import logging


@periodic_task(run_every=crontab(), name="sanity", ignore_result=True)
def sanity():
    logging.info('Hello from moolah-celery')
