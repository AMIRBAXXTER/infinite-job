from time import sleep

from code.config.celery_base import app


@app.task
def test_task():
    sleep(2)
    print('test task')
