from fastapi import FastAPI
from sender import Sender_multiple, Sender_single
from fastapi.responses import JSONResponse
import time

app = FastAPI(title="SMS Gateway")

TIME_SLEEP = 3

@app.post("/sending")
def post_message(address: str, phone_number: int, message: str):
    task = Sender_single().send_single.apply_async((address, phone_number, message), queue='sending')
    time.sleep(TIME_SLEEP)
    return JSONResponse({"task_id": task.id,
                         "task_status": task.status,
                         "task_result": task.result
                         })

@app.post("/mailing")
def post_mailing(address: str, phone_numbers: list, message: str):
    task = Sender_multiple().send_multiple.apply_async((address, phone_numbers, message), queue='sending')
    time.sleep(TIME_SLEEP)
    return JSONResponse({"task_id": task.id,
                         "task_status": task.status,
                         "task_result": task.result
                         })