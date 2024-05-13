from fastapi import FastAPI
from connection.contracts import PostOrderRequestBody, OrderInfo
from multiprocessing import Queue
from threading import Thread
from uuid import uuid4, UUID
from dataclasses import asdict
from connection.producer import proceed_to_deliver
from connection.consumer import wait_response

app = FastAPI()
host = "0.0.0.0"
port = 5001

@app.post('/update')        
async def post_order(body: PostOrderRequestBody, ):
    order: OrderInfo = body.to_order_info()
    id = str(uuid4())
    proceed_to_deliver(id, order)
    response = await wait_response(id)

    return response


def start_rest():
    Thread(target=lambda: app.run(host=host, port=port, debug=True)).start()
    

if __name__ == "__main__":
    start_rest()
    

