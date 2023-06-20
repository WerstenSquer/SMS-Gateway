import requests
from receiver import To_Google, To_Yandex
from celery import Celery

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

repeat_time = 60 #время, за которое происходит повторная отправка

class Sender_single():
    @staticmethod
    def send(address, phone_number, message):
        if address == "Google":
            recepient = To_Google()
        elif address == "Yandex":
            recepient = To_Yandex()
        return [recepient.response(phone_number, message).status_code,
                recepient.response(phone_number, message).url]

class Sender_multiplie():
    @celery_app.task(bind=True, default_retry_delay=repeat_time)
    def send(self, address, phone_numbers: list, message):
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
