import logging
from functools import wraps


def log(*, filename=None):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            name_func = func.__name__
            if filename is None:
                try:
                    result = func(*args, **kwargs)
                    print(f"{name_func} ok")
                    return result
                except Exception as e:
                    error_type = type(e).__name__
                    print(f"{name_func} error: {error_type}. Inputs: {args} {kwargs}")
            else:
                logging.basicConfig(level=logging.INFO, filename=filename, filemode="a")
                try:
                    result = func(*args, **kwargs)
                    logging.info(f"{name_func} ok")
                    return result
                except Exception as e:
                    error_type = type(e).__name__
                    logging.info(f"{name_func} error: {error_type}. Inputs: {args} {kwargs}")
                    raise

        return inner

    return wrapper


@log()
def my_function(x, y):
    return x / y


my_function(2, 0)
