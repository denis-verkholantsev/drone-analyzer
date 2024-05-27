from execution_order import execute_order
from producer import proceed_to_deliver


async def handle_event(id, details, location, responses_dict):
    if details['deliver_from'] == 'scheduler':
        response = await execute_order(id, details, location, responses_dict)
        if response == 'OK':
            details['deliver_to'] == 'scheduler'
            details['deliver_from'] == 'navigation'
            proceed_to_deliver(id, details)
    elif details['deliver_from'] == 'gps':
        if 'response' not in details:
            return
        if details['response'] == 'OK':
            location.latitude = details['response']['latitude']
            location.longtitude = details['response']['longtitude']
        if details['response'] == 'bad response':
            return
    elif details['deliver_from'] == 'drive':
        responses_dict[id] = details

    