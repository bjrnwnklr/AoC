# Load any required modules. Most commonly used:

# import re
# from collections import defaultdict
from utils.aoctools import aoc_timer


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
    """For operator type packets, return the length type ID (bit 6)."""
    assert packet_type(bitlist) != 4
    return bitlist[6]


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

    if packet_type(packet) == 4:
        # literal value - length determined by counting bits in groups of five
        # until the first bit is a 0
        #
        # a literal type packet does not contain any sub-packets, so we can just
        # return the packet version (this is the leaf case)

        # calculate used length
        used_length = 6
        last = False
        while not last:
            if packet[used_length] == 0:
                last = True
            used_length += 5

        return packet_version(packet), used_length
    else:
        # operator packages
        # these contribute their own version number and then the version numbers
        # of any packages contained within
        v_sum = packet_version(packet)
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

                # identify the number of packages contained within
                n = bitlist_to_int(packet[7:18])
                used_length = 0
                processed_packages = 0
                while processed_packages < n:
                    v_sum_inc, used_length_inc = parse_packet(
                        packet[18 + used_length:])
                    v_sum += v_sum_inc
                    used_length += used_length_inc
                    processed_packages += 1

                return v_sum, 18 + used_length


def parse_packet_2(packet: list[int]):
    """Parse a packet and return the sum of the packet versions contained 
    in all subpackets within.

    Returns sum of versions of contained packets and length consumed by the processed packets.
    """
    used_length = 0

    if packet_type(packet) == 4:
        # literal value - length determined by counting bits in groups of five
        # until the first bit is a 0
        #
        # a literal type packet does not contain any sub-packets, so we can just
        # return the packet version (this is the leaf case)

        # calculate used length
        used_length = 6
        last = False
        while not last:
            if packet[used_length] == 0:
                last = True
            used_length += 5

        return literal_value(packet), used_length
    else:
        # operator packages
        # the value of this packet is derived from the operator type and values
        # of any packages contained within
        vals = []
        length = 0
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
                    val, used_length_inc = parse_packet_2(
                        packet[22 + used_length:22 + l])
                    used_length += used_length_inc
                    vals.append(val)
                length = 22 + l

            case 1:
                # next 11 bits are a number that represents the number of
                # sub-packets immediately contained by this packet

                # identify the number of packages contained within
                n = bitlist_to_int(packet[7:18])
                used_length = 0
                processed_packages = 0
                while processed_packages < n:
                    val, used_length_inc = parse_packet_2(
                        packet[18 + used_length:])
                    used_length += used_length_inc
                    processed_packages += 1
                    vals.append(val)

                length = 18 + used_length

        # now process the values returned based on the operator type
        match packet_type(packet):
            case 0:
                # sum
                result = sum(vals)
            case 1:
                # product
                result = 1
                for v in vals:
                    result *= v
            case 2:
                # minimum
                result = min(vals)
            case 3:
                # maximum
                result = max(vals)
            case 5:
                # greater than
                result = 1 if vals[0] > vals[1] else 0
            case 6:
                # less than
                result = 1 if vals[0] < vals[1] else 0
            case 7:
                # equal to
                result = 1 if vals[0] == vals[1] else 0

        return result, length


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""

    bitlist = hex_to_bitlist(puzzle_input)
    return parse_packet(bitlist)[0]


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""

    bitlist = hex_to_bitlist(puzzle_input)
    return parse_packet_2(bitlist)[0]


if __name__ == '__main__':
    # read the puzzle input
    puzzle_input = load_input('input/16.txt')

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f'Part 1: {p1}')

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f'Part 2: {p2}')

# Part 1: Start: 11:41 End: 17:42 (Reading the text and creating 7 test cases took until 11:59!)
# Part 2: Start: 17:44 End: 18:16

# Elapsed time to run part1: 0.00736 seconds.
# Part 1: 875
# Elapsed time to run part2: 0.00710 seconds.
# Part 2: 1264857437203

# After removing some unnecessary calculations (i in literal vals, v_sum):
# Elapsed time to run part1: 0.00360 seconds.
# Part 1: 875
# Elapsed time to run part2: 0.00415 seconds.
# Part 2: 1264857437203
