import re
import json


def traverse_json(js):
    if isinstance(js, int):
        return js
    elif isinstance(js, str):
        return 0
    elif isinstance(js, dict):
        if 'red' in js.values():
            return 0
        else:
            return sum(traverse_json(x) for x in js.values())
    else:
        return sum(traverse_json(x) for x in js)


if __name__ == '__main__':

    # f_name = 'ex1.txt'
    f_name = 'input.txt'

    with open(f_name, 'r') as f:
        line = f.readline().strip()

    m = re.findall(r'(-?\d+)', line)
    if m:
        part1 = sum(map(int, m))
        print(part1)

    # part 1: 111754

    js = json.loads(line)
    print(traverse_json(js))

    # part 2: 65402
