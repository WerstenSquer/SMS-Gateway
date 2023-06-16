from fastapi import FastAPI
from sender import Sender

app = FastAPI(title="SMS Gateway")

@app.post("/sending")
async def post_message(address, phone_number, message):
    return Sender().send(address, phone_number, message)