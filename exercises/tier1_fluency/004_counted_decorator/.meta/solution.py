from functools import wraps


def counted(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        wrapper.call_count += 1
        return fn(*args, **kwargs)
    wrapper.call_count = 0
    return wrapper
