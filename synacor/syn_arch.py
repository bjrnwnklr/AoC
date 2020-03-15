# Synacor challenge

# first attempt at creating the virtual machine

from collections import defaultdict
import logging


class Synacor():

    def __init__(self, mem=[], ip=0):

        # instruction pointer
        self.ip = 0

        # halt parameter
        self.done = False

        # defaultdict of the program
        self.mem = defaultdict(int, enumerate(mem))



