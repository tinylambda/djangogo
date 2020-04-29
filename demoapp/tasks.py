import time
from celery import shared_task


@shared_task(bind=True)
def demoapp_task(self, *args, **kwargs):
    num = kwargs.get('num', 10)
    count = 0
    while count < num:
        print('Busy....')
        time.sleep(1)
        count += 1
    print('Done')

