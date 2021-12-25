# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
# from utils.aoctools import aoc_timer


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    with open(f_name, 'r') as f:
        return f.readline().strip()


def hex_to_bitlist(hex_inp: str) -> list[int]:
    """
    Convert a hex string e.g. D2FE28 into a list of bits (0 and 1 values).
    Each hexadecimal character corresponds to four bits.
    """
    bitlist = []
    for h in hex_inp:
        h_int = int(h, base=16)
        h_bin = f'{h_int:0>4b}'
        bitlist.extend(list(h_bin))
    return bitlist


def bitlist_to_int(bitlist: list[int]) -> int:
    """Convert a list of bits (0 and 1 values) into an integer. Most significant bit comes first."""
    b = ''.join(x for x in bitlist)
    return int(b, base=2)


class Packet:
    """Defines a BITS packet"""

    def __init__(self, bitlist: list[int]) -> None:
        self.bitlist = bitlist

    def packet_version(self) -> int:
        """Parse the header of a packet and return the packet version (bits 0-2) as an int."""
        return bitlist_to_int(self.bitlist[:3])

    def packet_type(self) -> int:
        """Parse the header of a packet and return the packet type (bits 3-5) as an int."""
        return bitlist_to_int(self.bitlist[3:6])

    def literal_value(self) -> int:
        """Decode the value of a literal value type packet (packet_type == 4)."""
        assert self.packet_type() == 4
        group_length = 5
        payload = self.bitlist[6:]
        num_groups = len(payload) // group_length
        bitlist = []
        for i in range(num_groups):
            b = payload[i * group_length: (i * group_length) + group_length]
            bitlist.extend(b[1:])

        return bitlist_to_int(bitlist)


def parse_packet(packet: list[int]):
    """Parse a packet recursively and return the sum of the packet versions contained 
    in all subpackets within."""
    pass

# @aoc_timer


def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    bitlist = hex_to_bitlist(puzzle_input)
    p = Packet(bitlist)
    return 1


# @aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    return 1


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input/16.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')

# Part 1: Start: 11:41 End:  (Reading the text and creating 7 test cases took until 11:59!)
# Part 2: Start:  End:
