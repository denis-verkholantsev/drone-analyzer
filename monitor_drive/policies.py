

def check_policies(details):
    if details['deliver_from'] == 'navigation' and details['deliver_to'] == 'drive' \
        or details['deliver_from'] == 'drive' and details['delivaer_to'] == 'navigation':
        return True
    return False
        