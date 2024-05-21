from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from api import start_rest
from connection import start_connection


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    parser.add_argument('--reset', action='store_true')
    args = parser.parse_args()
    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md

    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])
    config.update(config_parser['connection-consumer'])

    start_rest()
    start_connection(args, config)