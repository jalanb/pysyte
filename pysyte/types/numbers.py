

def inty(thing):
    """Try to make an int from thing"""
    if not thing:
        return 0
    try:
        return int(thing)
    except TypeError:
        return thing

