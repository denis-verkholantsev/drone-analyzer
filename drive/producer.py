from multiprocessing import Queue
from random import choice
from threading import Thread
from confluent_kafka import Producer
from dataclasses import asdict
import json


_requests_queue: Queue = None
_requests_dict: dict = None


def proceed_to_deliver(id, details):
    _requests_queue.put(id)
    _requests_dict[id] = details


def producer_job(_,config):
    producer = Producer(config)

    def delivery_callback(err, msg):
        if err:
            print(f'[error] Message failed delivery: {err}')
    
    while True:
        id = _requests_queue.get()
        details = _requests_dict.get(id)
        if details is None:
            continue
        details['deliver_from'] = 'drive'
        details['deliver_to'] = 'navigation'
        details['response'] == 'OK'
        producer.produce('monitor-drive', value=details, key=id, callback=delivery_callback)
        producer.poll(10)
        producer.flush()


def start_producer(args, config = None, requests_queue=None, requests_dict=None):
    global _requests_queue, _requests_dict
    _requests_dict = requests_dict
    _requests_queue = requests_queue
    Thread(target=lambda: producer_job(args, config)).start()
    

if __name__ == '__main__':
    start_producer()    