"""Test the examples given in the puzzle to verify the solution is working."""

# load the required functions from the actual solution
from solutions.aoc2021_16 import load_input, part1, part2, hex_to_bitlist, literal_value, parse_packet, parse_packet_2


class Test_AOC2021_16:
    """Specifies the tests for parts 1 and 2.

    Create test_n_n functions for each example given in the puzzle definition, put the example in a 
    `test_n_n.txt` file in the `test` directory, and replace the expected value in the `assert` statement.

    Tests can then be run in the day's directory with `pytest`.
    """

    def test_1_1(self):
        """Convert a hex input into a decimal number

        This is a type 4 (literal) packet.

        This input (D2FE28) is represented as bits: 110100101111111000101000
        with the literal number encoded being 2021.
        """
        puzzle_input = load_input('testinput/16_1_1.txt')
        bitlist = hex_to_bitlist(puzzle_input)
        assert literal_value(bitlist) == 2021

    def test_1_1_version(self):
        """Return the version number of the simplest use case (one literal package)

        This is a type 4 (literal) packet.

        This input (D2FE28) is represented as bits: 110100101111111000101000
        with the literal number encoded being 2021.

        The version number is 6 and length processed is 21
        """
        puzzle_input = load_input('testinput/16_1_1.txt')
        bitlist = hex_to_bitlist(puzzle_input)
        assert parse_packet(bitlist) == (6, 21)

    def test_1_2(self):
        """Convert a hex input into a decimal number

        This is a length type 0 packet containing two sub packets.

        This input (38006F45291200) is represented as bits:
        00111000000000000110111101000101001010010001001000000000

        The sum of versions is 1 + 6 + 2 = 9, length is 49.
        """
        puzzle_input = load_input('testinput/16_1_2.txt')
        bitlist = hex_to_bitlist(puzzle_input)
        assert parse_packet(bitlist) == (9, 49)

    def test_1_3(self):
        """Convert a hex input into a decimal number

        This is a length type 1 packet containing three sub packets.

        This input (EE00D40C823060) is represented as bits:
        11101110000000001101010000001100100000100011000001100000

        The sum of versions is 7 + 2 + 4 + 1 = 14, length is 51.
        """
        puzzle_input = load_input('testinput/16_1_3.txt')
        bitlist = hex_to_bitlist(puzzle_input)
        assert parse_packet(bitlist) == (14, 51)

    def test_1_4(self):
        """
        8A004A801A8002F478 represents an operator packet (version 4) which contains
        an operator packet (version 1) which contains an operator packet (version 5)
        which contains a literal value (version 6); this packet has a version sum of 16.
        """
        puzzle_input = load_input('testinput/16_1_4.txt')
        bitlist = hex_to_bitlist(puzzle_input)
        assert parse_packet(bitlist)[0] == 16

    def test_1_5(self):
        """
        620080001611562C8802118E34 represents an operator packet (version 3) which contains
        two sub-packets; each sub-packet is an operator packet that contains
        two literal values. This packet has a version sum of 12.
        """
        puzzle_input = load_input('testinput/16_1_5.txt')
        bitlist = hex_to_bitlist(puzzle_input)
        assert parse_packet(bitlist)[0] == 12

    def test_1_6(self):
        """
        C0015000016115A2E0802F182340 has the same structure as the previous example,
        but the outermost packet uses a different length type ID.
        This packet has a version sum of 23.
        """
        puzzle_input = load_input('testinput/16_1_6.txt')
        bitlist = hex_to_bitlist(puzzle_input)
        assert parse_packet(bitlist)[0] == 23

    def test_1_7(self):
        """
        A0016C880162017C3686B18A3D4780 is an operator packet that contains an
        operator packet that contains an operator packet that contains
        five literal values; it has a version sum of 31.
        """
        puzzle_input = load_input('testinput/16_1_7.txt')
        bitlist = hex_to_bitlist(puzzle_input)
        assert parse_packet(bitlist)[0] == 31

    def test_2_1(self):
        """
        C200B40A82 finds the sum of 1 and 2, resulting in the value 3.
        """
        puzzle_input = 'C200B40A82'
        bitlist = hex_to_bitlist(puzzle_input)
        assert parse_packet_2(bitlist)[0] == 3

    def test_2_2(self):
        """
        04005AC33890 finds the product of 6 and 9, resulting in the value 54.
        """
        puzzle_input = '04005AC33890'
        bitlist = hex_to_bitlist(puzzle_input)
        assert parse_packet_2(bitlist)[0] == 54

    def test_2_3(self):
        """
        880086C3E88112 finds the minimum of 7, 8, and 9, resulting in the value 7.
        """
        puzzle_input = '880086C3E88112'
        bitlist = hex_to_bitlist(puzzle_input)
        assert parse_packet_2(bitlist)[0] == 7

    def test_2_4(self):
        """
        CE00C43D881120 finds the maximum of 7, 8, and 9, resulting in the value 9.
        """
        puzzle_input = 'CE00C43D881120'
        bitlist = hex_to_bitlist(puzzle_input)
        assert parse_packet_2(bitlist)[0] == 9

    def test_2_5(self):
        """
        D8005AC2A8F0 produces 1, because 5 is less than 15.
        """
        puzzle_input = 'D8005AC2A8F0'
        bitlist = hex_to_bitlist(puzzle_input)
        assert parse_packet_2(bitlist)[0] == 1

    def test_2_6(self):
        """
        F600BC2D8F produces 0, because 5 is not greater than 15.
        """
        puzzle_input = 'F600BC2D8F'
        bitlist = hex_to_bitlist(puzzle_input)
        assert parse_packet_2(bitlist)[0] == 0

    def test_2_7(self):
        """
        9C005AC2F8F0 produces 0, because 5 is not equal to 15.
        """
        puzzle_input = '9C005AC2F8F0'
        bitlist = hex_to_bitlist(puzzle_input)
        assert parse_packet_2(bitlist)[0] == 0

    def test_2_8(self):
        """
        9C0141080250320F1802104A08 produces 1, because 1 + 3 = 2 * 2.
        """
        puzzle_input = '9C0141080250320F1802104A08'
        bitlist = hex_to_bitlist(puzzle_input)
        assert parse_packet_2(bitlist)[0] == 1
