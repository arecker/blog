from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from celery.decorators import periodic_task


logger = get_task_logger(__name__)

@periodic_task(run_every=crontab(), name="sanity", ignore_result=True)
def sanity():
    logger.info('Hello from blog-celery')
    print('Hello from blog-celery stdout')
