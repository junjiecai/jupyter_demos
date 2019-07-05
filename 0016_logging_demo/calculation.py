from functools import wraps

from loguru import logger


# 用装饰器读
def debug_logging(func):
    @wraps(func)
    def inner(*args, **kwargs):
        logger.debug('Calling {} with args:{}, kwargs:{}', func.__name__, str(args), str(kwargs))
        return func(*args, **kwargs)

    return inner


@debug_logging
def add(x, y):
    z = x + y
    logger.info('Add two number')

    return z


@debug_logging
def square(x):
    return x ** 2
