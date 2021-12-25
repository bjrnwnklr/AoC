"""Test the examples given in the puzzle to verify the solution is working."""

# load the required functions from the actual solution
from solutions.aoc2021_16 import load_input, part1, part2, hex_to_bitlist, literal_value, parse_packet


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

    # def test_1_3(self):
    #     """Convert a hex input into a decimal number

    #     This is a length type 1 packet containing two sub packets.

    #     This input (EE00D40C823060) is represented as bits:
    #     11101110000000001101010000001100100000100011000001100000
    #     with the literal number encoded being 1, 2 and 3 in the three sub packets.
    #     """
    #     puzzle_input = load_input('testinput/16_1_3.txt')
    #     assert part1(puzzle_input) == 123

    # def test_1_4(self):
    #     """
    #     8A004A801A8002F478 represents an operator packet (version 4) which contains
    #     an operator packet (version 1) which contains an operator packet (version 5)
    #     which contains a literal value (version 6); this packet has a version sum of 16.
    #     """
    #     puzzle_input = load_input('testinput/16_1_4.txt')
    #     assert part1(puzzle_input) == 16

    # def test_1_5(self):
    #     """
    #     620080001611562C8802118E34 represents an operator packet (version 3) which contains
    #     two sub-packets; each sub-packet is an operator packet that contains
    #     two literal values. This packet has a version sum of 12.
    #     """
    #     puzzle_input = load_input('testinput/16_1_5.txt')
    #     assert part1(puzzle_input) == 12

    # def test_1_6(self):
    #     """
    #     C0015000016115A2E0802F182340 has the same structure as the previous example,
    #     but the outermost packet uses a different length type ID.
    #     This packet has a version sum of 23.
    #     """
    #     puzzle_input = load_input('testinput/16_1_6.txt')
    #     assert part1(puzzle_input) == 23

    # def test_1_7(self):
    #     """
    #     A0016C880162017C3686B18A3D4780 is an operator packet that contains an
    #     operator packet that contains an operator packet that contains
    #     five literal values; it has a version sum of 31.
    #     """
    #     puzzle_input = load_input('testinput/16_1_7.txt')
    #     assert part1(puzzle_input) == 31
