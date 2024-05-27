

def check_policies(details):
    if details['deliver_from'] == 'navigation' and details['deliver_to'] == ' gps' \
        or details['deliver_from'] == 'gps' and details['delivaer_to'] == 'navigation':
        return True
    return False
        