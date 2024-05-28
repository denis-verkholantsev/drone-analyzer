from multiprocessing import Queue
from uuid import UUID
from consumer import start_consumer
from producer import start_producer
from confluent_kafka.admin import AdminClient, NewTopic
from argparse import ArgumentParser, FileType
from configparser import ConfigParser

def start_scheduler(args=None, config=None):
    parser = ArgumentParser()
    parser.add_argument("config_file", type=FileType("r"))
    parser.add_argument("--reset", action="store_true")
    args = parser.parse_args()
    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md

    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser["default"])
    config.update(config_parser["scheduler"])
    _requests_queue: Queue = Queue(1000)
    _responses_queue: Queue = Queue(1000)
    _responses_dict: dict[UUID, str] = {}
    _requests_dict: dict[UUID, dict] = {}

    admin = AdminClient(config)
    admin.create_topics([NewTopic('scheduler'), NewTopic('central-system')])
    start_consumer(args, config, _responses_queue, _responses_dict)
    start_producer(args, config, _requests_queue, _requests_dict)


if __name__ == "__main__":
    start_scheduler()
