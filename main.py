from fastapi import FastAPI
from sender import Sender_multiplie, Sender_single
from fastapi.responses import JSONResponse
import time

app = FastAPI(title="SMS Gateway")

@app.post("/sending")
def post_message(address, phone_number, message):
    task = Sender_single().send_single.apply_async((address, phone_number, message), queue='sending')
    #time.sleep(3)
    return JSONResponse({"task_id": task.id,
                         "task_status": task.status,
                         "task_result": task.result
                         })

@app.post("/mailing")
def post_mailing(address, phone_numbers: list, message):
    task = Sender_multiplie().send_multiple.apply_async((address, phone_numbers, message), queue='sending')
    #time.sleep(3)
    return JSONResponse({"task_id": task.id,
                         "task_status": task.status,
                         "task_result": task.result
                         })