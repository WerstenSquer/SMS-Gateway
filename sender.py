import requests
from receiver import To_Google, To_Yandex
from celery import Celery

celery = Celery(
    '__name__',
    broker='redis://localhost:6379',
    backend='redis://localhost:6379',
)

celery.conf.task_routes = {
    'tasks.send_single': {'queue': 'sending'},
    'tasks.send_multiple': {'queue': 'sending'},
}

TIME_REPEAT = 5
MAX_RETRIES = 3

class Sender_single():
    @celery.task(bind=True, max_retries=MAX_RETRIES)
    def send_single(self, address, phone_number, message):
        if address == "Google":
            recepient = To_Google()
        elif address == "Yandex":
            recepient = To_Yandex()
        try:
            with recepient.response(phone_number, message) as response:
                result = {'status': response.status_code,
                          'number': phone_number,
                          'URL': response.url}
        except requests.exceptions.ConnectionError:
                self.retry(countdown=TIME_REPEAT)
        return result

class Sender_multiple():
    @celery.task(bind=True, max_retries=MAX_RETRIES)
    def send_multiple(self, address, phone_numbers: list, message):
        result_list = []
        for number in phone_numbers:
            result = Sender_single.send_single(address, number, message)
            result_list.append(result)
        return result_list
