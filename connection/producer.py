from multiprocessing import Queue
from random import choice
from threading import Thread
from confluent_kafka import Producer
import json
from checks import check

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

    topic = 'central-system'

    while True:
        id = _requests_queue.get()
        details = _requests_dict.pop(id, None)
        if details is None:
            continue
        
        details_dict = details.__dict__
        details_dict['deliver_from'] = 'connection'
        details_dict['deliver_to'] = 'scheduler'

        if not check(details):
            details_dict['response'] = 'bad task'
            producer.produce('connection', value=json.dumps(details_dict), key=id, callback=delivery_callback)
            continue
        
        producer.produce(topic, value=json.dumps(details_dict), key=id, callback=delivery_callback)
        # print(f'---------from connection to {details_dict['deliver_to']}----------')
        producer.poll(10000)
        producer.flush()


def start_producer(args, config = None, requests_queue=None, requests_dict=None):
    global _requests_queue, _requests_dict
    _requests_dict = requests_dict
    _requests_queue = requests_queue
    Thread(target=lambda: producer_job(args, config)).start()
    

if __name__ == '__main__':
    start_producer()    