import requests
from receiver import To_Google, To_Yandex
from celery import Celery

celery = Celery(
    '__name__',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

celery.conf.task_routes = {
    'tasks.send_single': {'queue': 'sending'},
    'tasks.send_multiple': {'queue': 'mailing'},
}

repeat_time = 60 #время, за которое происходит повторная отправка

class Sender_single():
    @staticmethod
    @celery.task
    def send_single(address, phone_number, message):
        if address == "Google":
            recepient = To_Google()
        elif address == "Yandex":
            recepient = To_Yandex()
        return [recepient.response(phone_number, message).status_code,
                recepient.response(phone_number, message).url]

class Sender_multiplie():
    @celery.task(bind=True, default_retry_delay=repeat_time)
    def send_multiple(self, address, phone_numbers: list, message):
        result_list = []
        for number in phone_numbers:
            if address == "Google":
                recepient = To_Google()
            elif address == "Yandex":
                recepient = To_Yandex()
            try:
                result = [recepient.response(number, message).status_code, number]
                result_list.append(result)
            except requests.exceptions.ConnectionError as ex:
                self.retry(exc=ex)
        return result_list
