from multiprocessing import Queue
from random import choice
from threading import Thread
from confluent_kafka import Producer
from dataclasses import asdict

_requests_queue: Queue = None
_requests_dict: dict = None


def proceed_to_deliver(id, order):
    _requests_queue.put(id)
    _requests_dict[id] = order


def producer_job(config):
    producer = Producer(config)

    def delivery_callback(err):
        if err:
            print(f'[error] Message failed delivery: {err}')

    topic = 'connection'

    while True:
        id = _requests_queue.get()
        order = _requests_dict.get(id)
        if order is None:
            continue
        producer.produce(topic, value=asdict(order), key=id, callback=delivery_callback)
        
        producer.poll(10000)
        producer.flush()


def start_producer(config, requests_queue, requests_dict):
    global _requests_queue, _requests_dict
    _requests_dict = requests_dict
    _requests_queue = requests_queue
    Thread(target=lambda: producer_job(config)).start()
    

if __name__ == '__main__':
    producer_config = {
        'bootstrap.servers': 'localhost:9092',
        'auto.offset.reset': 'earliest'
    }
    start_producer(producer_config)    