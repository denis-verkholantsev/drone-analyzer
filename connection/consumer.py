from threading import Thread
from confluent_kafka import Consumer, KafkaError
import asyncio
from multiprocessing import Queue

_responses_dict: dict = None
_responses_queue: Queue = None


async def wait_response(id):
    loop = asyncio.get_event_loop()
    while True:
        if id in _responses_dict:
            return _responses_dict.get(id)
        await asyncio.sleep(1)


def consumer_job(config):
    consumer = Consumer(config)
    topics = ['connection']
    consumer.subcribe(topics)

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Error: {msg.error()}")
                    break
            else:
                try:
                    id = msg.key().decode('utf-8')
                    details = msg.value().decode('utf-8')
                    _responses_dict[id] = details
                    _responses_queue.put(id)
                except Exception as e:
                    print(f"[error] malformed event received from topic {topics[0]}: {msg.value()}. {e}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


def start_consumer(config, responses_queue = None, responses_dict = None):
    global _responses_queue, _responses_dict
    _responses_dict = responses_dict
    _responses_queue = responses_queue
    Thread(target=lambda: consumer_job(config)).start()


if __name__ == "__main__":

    consumer_config = {
        'bootstrap.servers': 'localhost:9092',
        'auto.offset.reset': 'earliest'
    }    
    start_consumer(consumer_config)


