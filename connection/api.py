from fastapi import FastAPI
from contracts import PostOrderRequestBody, OrderInfo
from multiprocessing import Queue
from threading import Thread
from uuid import uuid4, UUID
from dataclasses import asdict
from producer import proceed_to_deliver
from consumer import wait_response
import uvicorn
import json

app = FastAPI()
host = "0.0.0.0"
port = 5001

@app.post('/update')        
async def post_order(body: PostOrderRequestBody, ):
    order: OrderInfo = body.to_order_info()
    id = str(uuid4())
    proceed_to_deliver(id, order)
    response = wait_response(id)

    return json.dumps({'r': response})


def start_rest():
    Thread(target=lambda: uvicorn.run(app, host=host, port=port, log_level='info')).start()
    

if __name__ == "__main__":
    start_rest()
    

