from multiprocessing import Queue
from uuid import UUID
from consumer import start_consumer
from producer import start_producer
from confluent_kafka.admin import AdminClient, NewTopic
from contracts import OrderInfo

def start_connection(args=None, config=None):

    _requests_queue: Queue = Queue(1000)
    _responses_queue: Queue = Queue(1000)
    _responses_dict: dict[UUID, str] = {}
    _requests_dict: dict[UUID, OrderInfo] = {}

    admin = AdminClient(config)
    admin.create_topics([NewTopic('connection'),
                         NewTopic('central-system'),
                        NewTopic("monitor-drive"),
                        NewTopic("monitor-battery"),
                        NewTopic("monitor-computer-vision"),
                        NewTopic("monitor-lidar"),
                        NewTopic("monitor-gps"),
                        NewTopic("scheduler"),
                        NewTopic("navigation"),
                        NewTopic("emergency-landing"),
                        NewTopic("gps"),
                        NewTopic('drive')])
    start_producer(args, config, _requests_queue, _requests_dict)
    start_consumer(args, config, _responses_queue, _responses_dict)

if __name__ == "__main__":
    start_connection()
