from threading import Thread


def async(f):
    """
    enables process to run in background while page is loaded
    """
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper
