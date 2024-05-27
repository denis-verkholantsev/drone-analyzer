
tasks = {'deliver', 'kill', 'walk'}

def check(details):
    if details.task in tasks:
        return True
    return False