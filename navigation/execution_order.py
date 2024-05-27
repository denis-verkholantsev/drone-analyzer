from producer import proceed_to_deliver
from uuid import uuid4
import asyncio 

async def wait_response(id, responses_dict):
    loop = asyncio.get_event_loop()
    while True:
        if id in responses_dict:
            return responses_dict.get(id)
        await asyncio.sleep(1)


async def execute_order(id, details: dict, location, responses_dict):
    details_drive = details.copy()
    details_drive['deliver_to'] = 'drive'
    details_drive['deliver_from'] = 'navigation'
    details['latitude'] = location.latitude
    details['longitude'] = location.longitude
    id_drive = uuid4()
    proceed_to_deliver(id_drive, details_drive)
    response_details = await wait_response(id, responses_dict)
    response_details['deilver_from'] = 'navigation'
    response_details['deliver_to'] = 'scheduler'

    proceed_to_deliver(id, response_details)



