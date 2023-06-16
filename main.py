from fastapi import FastAPI
from abc import ABC, abstractmethod
import requests

app = FastAPI(title="SMS Gateway")

client_database = [
    {"phone number": "88005553535", "name": "Том"},
    {"phone number": "89004548838", "name": "Боб"},
    {"phone number": "89503737419", "name": "Джон"},
    {"phone number": "88080707834", "name": "Филл"},
    {"phone number": "89357249353", "name": "Сэм"}
]

messages = [
    "Вам пришло сообщение 1",
    "Вам пришло сообщение 2",
    "Вам пришло сообщение 3"
]

@app.get("/clients/{phone_number}")
async def get_client(phone_number):
    return [client for client in client_database if client.get("phone number") == phone_number]

@app.get("/messages/{message_id}")
async def get_message(message_id: int):
    return messages[message_id - 1]

@app.post("/sending")
async def post_message(address, phone_number, message_id: int):
    name = [client.get("name") for client in client_database if client.get("phone number") == phone_number]
    full_message = name[0] + ", " + messages[message_id - 1] + "."
    return Sender().send(address, phone_number, full_message)

class Receiver(ABC):
    @staticmethod
    @abstractmethod
    def path_indicate():
        pass

class To_Google(Receiver):
    @staticmethod
    def path_indicate():
        path = "https://www.google.com/"
        return path

class To_Yandex(Receiver):
    @staticmethod
    def path_indicate():
        path = "https://ya.ru/"
        return path

class Sender():
    @staticmethod
    def send(address, phone_number, message):
        params = {"q": {"phone number": phone_number, "message": message}}
        if address == "Google":
            response = requests.get(To_Google().path_indicate(), params=params)
        elif address == "Yandex":
            response = requests.get(To_Yandex().path_indicate(), params=params)
        return response.status_code
