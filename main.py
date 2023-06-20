from fastapi import FastAPI
from sender import Sender_multiplie, Sender_single

app = FastAPI(title="SMS Gateway")

@app.post("/sending")
async def post_message(address, phone_number, message):
    return Sender_single().send(address, phone_number, message)

@app.post("/mailing")
async def post_mailing(address, phone_numbers: list, message):
    return Sender_multiplie().send.apply_async((address, phone_numbers, message), countdown=10)
