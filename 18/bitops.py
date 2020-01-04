import logging
from string import ascii_lowercase


def test_bit(bitarray, bit):
    return bitarray & bit

def set_bit(bitarray, bit):
    return bitarray | bit


if __name__ == '__main__':

    keys = {x: 1 << i for i, x in enumerate(ascii_lowercase)}

    for k in keys:
        print('{}: {}'.format(k, bin(keys[k])))


    keystore = 0b0

    # set some random keys
    # set a, b, t, d, u
    for key in ['a', 'b', 't', 'd', 'u']:
        keystore = set_bit(keystore, keys[key])

    print('Keystore: {}, {}'.format(keystore, bin(keystore)))

    print('a in keystore: {}'.format(bool(test_bit(keystore, keys['a']))))
    print('x in keystore: {}'.format(bool(test_bit(keystore, keys['x']))))

    keystore = set_bit(keystore, keys['x'])
    print('x in keystore: {}'.format(bool(test_bit(keystore, keys['x']))))

    print('Keystore: {}, {}'.format(keystore, bin(keystore)))