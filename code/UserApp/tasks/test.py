from time import sleep

from config.celery_base import app


@app.task(queue='tasks')
def test_task():
    sleep(2)
    print('test task')
