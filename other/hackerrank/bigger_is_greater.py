# https://www.hackerrank.com/challenges/bigger-is-greater/problem

#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'biggerIsGreater' function below.
#
# The function is expected to return a STRING.
# The function accepts STRING w as parameter.
#


def biggerIsGreater(w):
    letters = list(w)
    if len(letters) == 1:
        return "no answer"

    i = -1
    while abs(i) < len(letters):
        right = sorted(letters[i:])
        print(f"{right=}")
        j = 0
        while j < len(right):
            current = letters[i - 1]
            print(f"{i=} {j=} {current=}")
            if right[j] > letters[i - 1]:
                # found a letter that is greater than the current letter
                # swap them, then break
                letters[i - 1] = right[j]
                right[j] = current
                print(f"Found. {letters=} {right=}")
                return "".join(letters[:i] + right)
            else:
                # right was not bigger than current, check next letter
                j += 1
        i -= 1

    # if we get here, no solution was found
    return "no answer"


if __name__ == "__main__":
    with open("bigger_expected.txt", "r") as f:
        expected = [line.strip() for line in f.readlines()]

    with open("bigger.txt", "r") as f:
        T = int(f.readline().strip())

        for T_itr in range(T):
            w = f.readline().strip()

            result = biggerIsGreater(w)
            print(w, result)
            assert result == expected[T_itr]
