from fastapi import FastAPI
from abc import ABC, abstractmethod
import requests

app = FastAPI(title="SMS Gateway")

@app.post("/sending")
async def post_message(address, phone_number, message):
    return Sender().send(address, phone_number, message)

class Receiver(ABC):
    @staticmethod
    @abstractmethod
    def response():
        pass

class To_Google(Receiver):
    @staticmethod
    def response(phone_number, message):
        path = "https://www.google.com/"
        params = {"q": {"phone number": phone_number, "message": message}}
        response = requests.get(path, params=params)
        return response

class To_Yandex(Receiver):
    @staticmethod
    def response(phone_number, message):
        path = "https://ya.ru/"
        params = {"q": {"phone number": phone_number, "message": message}}
        response = requests.get(path, params=params)
        return response

class Sender():
    @staticmethod
    def send(address, phone_number, message):
        if address == "Google":
            return To_Google().response(phone_number, message).status_code
        elif address == "Yandex":
            return To_Yandex().response(phone_number, message).status_code
        else:
            return "Неверный адрес."