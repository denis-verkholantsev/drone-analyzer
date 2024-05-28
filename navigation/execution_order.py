from producer import proceed_to_deliver
from uuid import uuid4
import asyncio 
import sys

def wait_response(id, responses_dict):
    while True:
        if id in responses_dict:
            return responses_dict.get(id)


def execute_order(id, details: dict, location, responses_dict):
    # print('------we are in execution---------')
    details['deliver_to'] = 'drive'
    details['deliver_from'] = 'navigation'
    # print('---------------')
    details['latitude'] = location.latitude
    details['longitude'] = location.longitude
    id_drive = str(uuid4())
    proceed_to_deliver(id_drive, details)
    details['deliver_from'] = 'navigation'
    details['deliver_to'] = 'scheduler'
    details['response'] = 'OK'
    return 'OK'



