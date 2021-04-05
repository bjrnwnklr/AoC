import re

REGEX_LITERAL = re.compile(r'(\"|\\x..|\\[\\\"])', re.UNICODE)
REGEX_ENCODED = re.compile(r'(\"|\\)', re.UNICODE)

def count_code(line):
    return len(line)


def count_literal(line):
    def _sub_escapes(matchobj):
        m = matchobj.group(0)
        if m == '"':
            return ''
        elif m == '\\"':
            return 'X'
        else:
            return 'X'
    newline = REGEX_LITERAL.sub(_sub_escapes, line)
    return len(newline)

def count_encoded(line):
    def _sub_encoded(matchobj):
        return 'XX'
    newline = REGEX_ENCODED.sub(_sub_encoded, line)
    return len(newline) + 2  # add 2 for surrounding quotes


if __name__ == '__main__':

    # f_name = 'ex1.txt'
    f_name = 'input.txt'

    with open(f_name, 'r', encoding="utf-8") as f:
        lines = f.readlines()

    c_code = c_literal = c_encoded = 0
    for line in lines:
        line = line.strip()
        c_code += count_code(line)
        c_literal += count_literal(line)
        c_encoded += count_encoded(line)

    print(f'code: {c_code} - literal: {c_literal} = {c_code - c_literal}')
    print(f'encoded: {c_encoded} - code: {c_code} = {c_encoded - c_code}')

    # Part 1. 1342
    # Part 2: 2074
