import math
from time import time
from datetime import datetime

seed = 4_000_000_007

def fmt_time(t):
    return datetime.strftime(datetime.fromtimestamp(t), '%a %b %d %H:%M:%S %Y')


def get_ts(t_remainder):
    """
    This takes O(sqrt(n)) time.
    :param t_remainder:
    :return:
    """
    n = 0
    found = False
    while not found:
        full_time = n * seed + t_remainder
        root = int(math.sqrt(full_time))
        if root ** 2 == full_time:
            found = True
        n += 1
        if n % 1_000_000 == 0:
            print(n, fmt_time(root))

    print(f'Found! {n=}, {full_time=}, {root=}')
    return root

ex1 = 1749870067

if __name__ == '__main__':
    # Should be solved with the Tonelli-Shanks algorithm to calculate the quadratic residue.
    # Assuming that the seed value used for the modulo is a prime number, the algorithm should
    # calculate this efficiently.

    t = time()
    print(fmt_time(t))
    res = get_ts(16)
    print(fmt_time(res))
    res = get_ts(ex1)
    print(fmt_time(res))