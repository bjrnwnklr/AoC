from functools import wraps
import timeit


def aoc_timer(func):
    """Times an AOC function"""

    @wraps(func)
    def _wrapper(*args, **kwargs):
        # do some timing
        start_time = timeit.default_timer()
        value = func(*args, **kwargs)
        # do some more timing and print
        duration = timeit.default_timer() - start_time
        print(f'Elapsed time to run {func.__name__}: {duration:.5f} seconds.')
        return value

    return _wrapper
