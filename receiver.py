from abc import ABC, abstractmethod
import requests

class Receiver(ABC):
    @staticmethod
    @abstractmethod
    def response():
        pass

class To_Google(Receiver):
    @staticmethod
    def response(phone_number, message):
        #path = "https://www.perevodchikl.com"
        path = "https://www.google.com/"
        params = {"q": {phone_number, message}}
        response = requests.get(path, params=params)
        return response

class To_Yandex(Receiver):
    @staticmethod
    def response(phone_number, message):
        path = "https://ya.ru/"
        params = {"q": {phone_number, message}}
        response = requests.get(path, params=params)
        return response