import re

f_name = 'input.txt'
# f_name = 'ex2.txt'

def find_aba(s):
    if s[0] == s[2] and s[0] != s[1] and '[' not in s and ']' not in s:
        return True
    else:
        return False


valid_addresses = 0
with open(f_name, 'r') as f:
    for line in f.readlines():
        valid_address = False
        line = line.strip('\n')

        # first split by opening brackets, the first part will be outer segment, the rest will be inner]outer segments
        first_outer, *rest = line.split('[')
        outer, inner = [first_outer], []
        for seg in rest:
            left, right = seg.split(']')
            inner.append(left)
            outer.append(right)

        for out_seg in outer:
#         # now we have all outer segments in 'outer' and all inner elements in 'inner'
            for i in range(len(out_seg) - 2):
                snippet = out_seg[i:i+3]
                if find_aba(snippet):
                    bab_snippet = f'{snippet[1]}{snippet[0]}{snippet[1]}'
                    for in_seg in inner:
                        if bab_snippet in in_seg:
                            print(f'ABA and BAB found: {snippet}')
                            print(line)
                            valid_address = True

        if valid_address:
            valid_addresses += 1

print(valid_addresses)

# part 1: 110
# part 2: 242
