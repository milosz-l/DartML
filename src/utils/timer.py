from functools import wraps
import time


def add_timer_note(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        time_note = f"{func.__name__} took {round(end - start, 4)}s to run"
        return result, time_note

    return wrapper
