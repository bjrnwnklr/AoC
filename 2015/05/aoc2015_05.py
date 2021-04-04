import re


# at least 3 vowels
# at least one letter twice in a row
# does not contain ab, cd, pq or xy
def rule3(line):
    regex = re.compile('(ab)|(cd)|(pq)|(xy)')
    return not regex.search(line)


def rule1(line):
    regex = re.compile('[aeiou]')
    matches = regex.findall(line)
    return len(matches) >= 3


def rule2(line):
    regex = re.compile(r'([a-z])\1')
    return regex.search(line) is not None


def rule4(line):
    """
    It contains a pair of any two letters that appears at least twice in the string without overlapping, like xyxy (xy)
    or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
    :param line:
    :return:
    """
    regex = re.compile(r'([a-z]{2}).*\1')
    return regex.search(line) is not None


def rule5(line):
    """
    It contains at least one letter which repeats with exactly one letter between them,
    like xyx, abcdefeghi (efe), or even aaa.
    :param line:
    :return:
    """
    regex = re.compile(r'([a-z]).\1')
    return regex.search(line) is not None


if __name__ == '__main__':

    # f_name = 'ex1.txt'
    f_name = 'input.txt'

    with open(f_name, 'r') as f:
        lines = f.readlines()

    nice_count = 0
    for line in lines:
        line = line.strip()
        if rule3(line) and rule1(line) and rule2(line):
            nice_count += 1

    print(f'Part 1: {nice_count}')

    # Part 1: 255

    nice_count = 0
    for line in lines:
        line = line.strip()
        if rule4(line) and rule5(line):
            print(f'Nice: {line}')
            nice_count += 1
        else:
            print(f'Naughty: {line}')

    print(f'Part 2: {nice_count}')

    # Part 2: 55
    