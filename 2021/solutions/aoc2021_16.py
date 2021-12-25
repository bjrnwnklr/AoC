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


def packet_version(bitlist: list[int]) -> int:
    """Parse the header of a packet and return the packet version (bits 0-2) as an int."""
    return bitlist_to_int(bitlist[:3])


def packet_type(bitlist: list[int]) -> int:
    """Parse the header of a packet and return the packet type (bits 3-5) as an int."""
    return bitlist_to_int(bitlist[3:6])


def packet_length_type(bitlist: list[int]) -> int:
    """For operator type packets, return the length type ID (bit 7)."""
    assert packet_type(bitlist) != 4
    return bitlist[7]


def literal_value(bitlist: list[int]) -> int:
    """Decode the value of a literal value type packet (packet_type == 4)."""
    assert packet_type(bitlist) == 4
    group_length = 5
    i = 6
    lit_val_bitlist = []
    while True:
        lit_val_bitlist.extend(bitlist[i + 1: i + group_length])
        if bitlist[i] == 0:
            break
        i += 5

    return bitlist_to_int(lit_val_bitlist)


def parse_packet(packet: list[int]):
    """Parse a packet and return the sum of the packet versions contained 
    in all subpackets within.

    Returns sum of versions of contained packets and length consumed by the processed packets.
    """
    v_sum = 0
    used_length = 0

    if len(packet) == 0:
        # if there is nothing left to process, return 0
        return 0, 0
    if sum(packet) == 0:
        # elemental case - if remaining packet is all 0s, we can return a 0
        return 0, len(packet)
    if packet_type(packet) == 4:
        # literal value - length determined by counting bits in groups of five
        # until the first bit is a 0
        #
        # a literal type packet does not contain any sub-packets, so we can just
        # return the packet version (this is the leaf case)

        # calculate used length
        print(f'Literal packet {packet}')
        i = 6
        last = False
        while not last:
            if packet[i] == 0:
                last = True
            i += 5
        used_length += i

        return packet_version(packet), used_length
    else:
        # operator packages
        # these contribute their own version number and then the version numbers
        # of any packages contained within
        v_sum += packet_version(packet)
        match packet_length_type(packet):
            case 0:
                # next 15 bits are a number that represents the total length
                # in bits of the sub-packets contained by this packet
                # so total length is 7 (header plus length bit) plus 15 plus
                # the length of the subpackets

                # process full length, which processes the first packet, then process
                # remaining length until nothing is left
                l = bitlist_to_int(packet[7:22])
                used_length = 0
                while used_length < l:
                    v_sum_inc, used_length_inc = parse_packet(
                        packet[22 + used_length:22 + l])
                    v_sum += v_sum_inc
                    used_length += used_length_inc
                return v_sum, 22 + l
            case 1:
                # next 11 bits are a number that represents the number of
                # sub-packets immediately contained by this packet
                pass

    return v_sum, 0


# @aoc_timer


def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    bitlist = hex_to_bitlist(puzzle_input)
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
