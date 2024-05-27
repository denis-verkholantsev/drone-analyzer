from multiprocessing import Queue
from uuid import UUID
from consumer import start_consumer
from producer import start_producer
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka.admin import AdminClient, NewTopic


def start_central_system(args=None, config=None):
    parser = ArgumentParser()
    parser.add_argument("config_file", type=FileType("r"))
    parser.add_argument("--reset", action="store_true")
    args = parser.parse_args()
    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md

    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser["default"])
    config.update(config_parser["central-system"])

    admin = AdminClient(config)
    admin.create_topics(
        [
            NewTopic("connection"),
            NewTopic("central-system"),
            NewTopic("monitor-drive"),
            NewTopic("monitor-battery"),
            NewTopic("monitor-computer-vision"),
            NewTopic("monitor-lidar"),
            NewTopic("monitor-gps"),
            NewTopic("scheduler"),
            NewTopic("navigation"),
            NewTopic("emergency-landing"),
        ]
    )

    _requests_queue: Queue = Queue(1000)
    _responses_queue: Queue = Queue(1000)
    _responses_dict: dict = {}
    _requests_dict: dict = {}

    # start_rest()
    start_consumer(args, config, _responses_queue, _responses_dict)
    start_producer(args, config, _requests_queue, _requests_dict)


if __name__ == "__main__":
    start_central_system()
