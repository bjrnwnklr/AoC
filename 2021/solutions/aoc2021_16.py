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
        bitlist.extend(list(map(int, list(h_bin))))
    return bitlist


def bitlist_to_int(bitlist: list[int]) -> int:
    """Convert a list of bits (0 and 1 values) into an integer. Most significant bit comes first."""
    b = ''.join(str(x) for x in bitlist)
    return int(b, base=2)


class Packet:
    """Defines a BITS packet"""

    def __init__(self, bitlist: list[int]) -> None:
        self.bitlist = bitlist
        self.version = self.packet_version()
        self.ptype = self.packet_type()

    def __repr__(self) -> str:
        return f'[v{self.version} / t{self.ptype}]'

    def packet_version(self) -> int:
        """Parse the header of a packet and return the packet version (bits 0-2) as an int."""
        return bitlist_to_int(self.bitlist[:3])

    def packet_type(self) -> int:
        """Parse the header of a packet and return the packet type (bits 3-5) as an int."""
        return bitlist_to_int(self.bitlist[3:6])

    def packet_length_type(self) -> int:
        """For operator type packets, return the length type ID (bit 7)."""
        assert self.ptype != 4
        return self.bitlist[7]

    def packet_length(self) -> int:
        """Determine the length in bits, comprised of the header (6 bits), operator mode
        length type bit (1 bit) and any payload (literal values, total length, number of
        sub packets immediately contained).
        """
        if self.ptype == 4:
            # literal value - lenght determined by counting bits in groups of five
            # until the first bit is a 0
            i = 6
            while self.bitlist[i] == 1:
                i += 5
            return i + 5
        else:
            # operator packages
            match self.packet_length_type():
                case 0:
                    # next 15 bits are a number that represents the total length
                    # in bits of the sub-packets contained by this packet
                    # so total length is 7 (header plus length bit) plus 15 plus
                    # the length of the subpackets
                    return 7 + 15 + bitlist_to_int(self.bitlist[8:24])
                case 1:
                    # next 11 bits are a number that represents the number of
                    # sub-packets immediately contained by this packet
                    pass

    def literal_value(self) -> int:
        """Decode the value of a literal value type packet (packet_type == 4)."""
        assert self.ptype == 4
        group_length = 5
        i = 6
        lit_val_bitlist = []
        while True:
            lit_val_bitlist.extend(self.bitlist[i + 1: i + group_length])
            if self.bitlist[i] == 0:
                break
            i += 5

        return bitlist_to_int(lit_val_bitlist)


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
