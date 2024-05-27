from threading import Thread
from confluent_kafka import Consumer, KafkaError
import asyncio
from multiprocessing import Queue
from producer import proceed_to_deliver
import json

_responses_dict: dict = None
_responses_queue: Queue = None


async def wait_response(id):
    loop = asyncio.get_event_loop()
    while True:
        if id in _responses_dict:
            return _responses_dict.get(id)
        await asyncio.sleep(1)


def consumer_job(_, config):
    topics = ['central-system']
    consumer = Consumer(config)
    consumer.subscribe(topics)

    try:
        while True:
            msg = consumer.poll(1.0)
            if not msg:
                continue
            elif msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Error: {msg.error()}")
                    break
            else:
                try:
                    id = msg.key().decode('utf-8')
                    details = json.loads(msg.value().decode('utf-8'))
                    proceed_to_deliver(id, details)
                except Exception as e:
                    print(f"[error] malformed event received from topic {topics[0]}: {msg.value()}. {e}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


def start_consumer(args, config = None, responses_queue = None, responses_dict = None):
    global _responses_queue, _responses_dict
    _responses_dict = responses_dict
    _responses_queue = responses_queue
    Thread(target=lambda: consumer_job(args, config)).start()


if __name__ == "__main__":
    start_consumer()


