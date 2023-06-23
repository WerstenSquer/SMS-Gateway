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
    'tasks.send_multiple': {'queue': 'mailing'},
}

TIME_REPEAT = 60 #время, за которое происходит повторная отправка

class Sender_single():
    @celery.task(bind=True, default_retry_delay=TIME_REPEAT)
    def send_single(self, address, phone_number, message):
        if address == "Google":
            recepient = To_Google()
        elif address == "Yandex":
            recepient = To_Yandex()
        try: recepient.response(phone_number, message).url
        except requests.exceptions.ConnectionError as ex:
                self.retry(exc=ex)
        return recepient.response(phone_number, message).url

class Sender_multiplie():
    @celery.task(bind=True, default_retry_delay=TIME_REPEAT)
    def send_multiple(self, address, phone_numbers: list, message):
        result_list = []
        for number in phone_numbers:
            if address == "Google":
                recepient = To_Google()
            elif address == "Yandex":
                recepient = To_Yandex()
            try:
                result = {'status_code': recepient.response(number, message).status_code,
                          'URL': recepient.response(number, message).url}
                result_list.append(result)
            except requests.exceptions.ConnectionError as ex:
                self.retry(exc=ex)
            result_list.append(result)
        return result_list

