
def handle_event(details: dict):
    if details['deliver_to'] == 'central-system' and details['deliver_from'] == 'scheduler' and 'response' in details:
        details['deliver_from'] == 'central-system'
        details['deliver_to'] == 'connection'