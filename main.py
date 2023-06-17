from fastapi import FastAPI
from sender import Sender

app = FastAPI(title="SMS Gateway")

@app.post("/mailing")
async def post_mailing(address, phone_numbers: list, message):
    return Sender().send(address, phone_numbers, message)