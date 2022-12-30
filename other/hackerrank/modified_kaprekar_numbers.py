# https://www.hackerrank.com/challenges/kaprekar-numbers/problem?h_r=next-challenge&h_v=zen&isFullScreen=true

#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'kaprekarNumbers' function below.
#
# The function accepts following parameters:
#  1. INTEGER p
#  2. INTEGER q
#


def kaprekarNumbers(p, q):
    results = []
    for i in range(p, q + 1):
        # square the number
        sq_i = i**2

        # split sq_i into two equal parts
        s = str(sq_i)
        # get number of digits of original number
        d = len(str(i))

        # split into two parts
        right = s[-d:]
        left = s[:-d]

        if left == "":
            left = "0"
        # convert back to int and check if sum of left and right is equal to i
        if int(left) + int(right) == i:
            results.append(i)

    print(" ".join(str(i) for i in results))


if __name__ == "__main__":
    p = 1
    q = 100
    result = kaprekarNumbers(p, q)
    print(p, q, result)
