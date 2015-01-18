__author__ = 'mic4ael'

import time
from functools import wraps


def profile(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        time_of_execution = time.time()
        f(*args, **kwargs)
        time_of_execution = float(time.time() - time_of_execution)
        print('Executed in: %.4f' % time_of_execution)

    return wrapper