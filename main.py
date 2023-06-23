from fastapi import FastAPI
from sender import Sender_multiplie, Sender_single
from fastapi.responses import JSONResponse
import time

app = FastAPI(title="SMS Gateway")

TIME_COUNTDOWN = 5
TIME_SLEEP = TIME_COUNTDOWN + 3

@app.post("/sending")
def post_message(address, phone_number, message):
    task = Sender_single().send_single.apply_async((address, phone_number, message), countdown=TIME_COUNTDOWN, queue='sending')
    time.sleep(TIME_SLEEP)
    return JSONResponse({"task_id": task.id,
                         "task_status": task.status,
                         "task_result": task.result
                         })

@app.post("/mailing")
def post_mailing(address, phone_numbers: list, message):
    task = Sender_multiplie().send_multiple.apply_async((address, phone_numbers, message), countdown=TIME_COUNTDOWN, queue='mailing')
    time.sleep(TIME_SLEEP * len(phone_numbers))
    return JSONResponse({"task_id": task.id,
                         "task_status": task.status,
                         "task_result": task.result
                         })