import re

REGEX = re.compile(r'(\"|\\x..|\\[\\\"])', re.UNICODE)


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
    newline = REGEX.sub(_sub_escapes, line)
    return len(newline)


if __name__ == '__main__':

    # f_name = 'ex1.txt'
    f_name = 'input.txt'

    with open(f_name, 'r', encoding="utf-8") as f:
        lines = f.readlines()

    c_code = c_literal = 0
    for line in lines:
        line = line.strip()
        c_code += count_code(line)
        c_literal += count_literal(line)

    print(f'code: {c_code} - literal: {c_literal} = {c_code - c_literal}')

    # Part 1. 1342

    