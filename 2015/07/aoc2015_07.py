import re
from collections import defaultdict


class Instruction:
    def __init__(self, line):
        # split by ->
        left, right = line.strip().split(' -> ')
        self.wire = right
        self.predecessors = list(re.findall(r'([a-z]{1,2})', left))
        self.gate = re.findall(r'([A-Z]+)', left)
        matches_val = re.findall(r'(\d+)', left)
        self.val = int(matches_val[0]) if matches_val else None


if __name__ == '__main__':

    f_name = 'ex1.txt'
    # f_name = 'input.txt'

    with open(f_name, 'r') as f:
        lines = f.readlines()

    rules = dict()
    dependents = defaultdict(set)
    resolved_vals = dict()

    for line in lines:
        instr = Instruction(line.strip())
        rules[instr.wire] = instr
        for w in instr.predecessors:
            dependents[instr.wire].add(w)

    print(rules)
    print()
    print(dependents)

    # find the elements that don't depend on any others
    start_wires = {
        r for r in rules if r not in dependents
    }
    print(start_wires)

    while start_wires:
        current_wire = start_wires.pop()

        w_obj = rules[current_wire]
        gate = w_obj.gate
        # evaluate the gate
        if not gate:
            # must be a number
            resolved_vals[current_wire] = w_obj.val

        elif gate == 'AND':
            args = [resolved_vals[w] for w in w_obj.predecessors]
            if w_obj.val:
                args.append(w_obj.val)


