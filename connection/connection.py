from multiprocessing import Queue
from uuid import UUID
from consumer import start_consumer
from producer import start_producer
from api import start_rest


if __name__ == "__main__":
    _requests_queue: Queue = Queue(1000)
    _responses_queue: Queue = Queue(1000)
    _responses_dict: dict[UUID, str] = {}
    _requests_dict: dict[UUID, str] = {}

    start_rest(_requests_queue, _responses_queue, _requests_dict, _responses_dict)
    start_consumer(_responses_queue, _responses_dict)
    start_producer(_requests_queue, _requests_dict)

