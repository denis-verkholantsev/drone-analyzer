

def check_policies(details: dict):
    if details.get('deliver_from') == 'navigation' and details.get('deliver_to') == ' gps' \
        or details.get('deliver_from') == 'gps' and details.get('deliver_to') == 'navigation':
        return True
    return False
        