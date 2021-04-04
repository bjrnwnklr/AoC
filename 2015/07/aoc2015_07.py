import re
from collections import defaultdict


class Instruction:
    def __init__(self, line):
        # split by ->
        left, right = line.strip().split(' -> ')
        self.wire = right
        self.predecessors = list(re.findall(r'([a-z]{1,2})', left))
        matches_gate = re.findall(r'([A-Z]+)', left)
        self.gate = matches_gate[0] if matches_gate else None
        matches_val = re.findall(r'(\d+)', left)
        self.val = int(matches_val[0]) if matches_val else None


if __name__ == '__main__':

    # f_name = 'ex1.txt'
    # f_name = 'input.txt'
    f_name = 'input2.txt'

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
    start_wires = [
        r for r in rules if r not in dependents
    ]
    print(start_wires)

    while start_wires:
        current_wire = start_wires.pop(0)

        w_obj = rules[current_wire]
        gate = w_obj.gate
        # evaluate the gate
        if not gate:
            # it's either a single reference to a predecessor or a number (if no predecessors)
            if w_obj.predecessors:
                val = resolved_vals[w_obj.predecessors[0]]
            else:
                val = w_obj.val
            resolved_vals[current_wire] = val
        elif gate == 'AND':
            args = [resolved_vals[w] for w in w_obj.predecessors]
            if w_obj.val:
                args.append(w_obj.val)
            resolved_vals[current_wire] = args[0] & args[1]
        elif gate == 'OR':
            args = [resolved_vals[w] for w in w_obj.predecessors]
            if w_obj.val:
                args.append(w_obj.val)
            resolved_vals[current_wire] = args[0] | args[1]
        elif gate == 'NOT':
            args = [resolved_vals[w] for w in w_obj.predecessors]
            # Python ~ (bitwise complement) works with signed integers, so produces a negative integer
            # Since we know that 16bit numbers are used, we can & with 0xFFFF (highest 16 bit int)
            # to get an unsigned integer value
            # (see https://stackoverflow.com/questions/31151107/how-do-i-do-a-bitwise-not-operation-in-python)
            resolved_vals[current_wire] = ~args[0] & 0xFFFF
        elif gate == 'LSHIFT':
            args = [resolved_vals[w] for w in w_obj.predecessors]
            if w_obj.val:
                args.append(w_obj.val)
            resolved_vals[current_wire] = args[0] << args[1]
        elif gate == 'RSHIFT':
            args = [resolved_vals[w] for w in w_obj.predecessors]
            if w_obj.val:
                args.append(w_obj.val)
            resolved_vals[current_wire] = args[0] >> args[1]

        # remove the wire from all dependencies since we have resolved it to a value
        for d in dependents:
            if current_wire in dependents[d]:
                dependents[d].remove(current_wire)

        # find any wires that have resolved all dependencies
        start_wires = [
            r for r in rules if not dependents[r] and r not in resolved_vals
        ]

    print(resolved_vals)
    print(resolved_vals['a'])

    # Part 1: 46065
    # Part 2: 14134