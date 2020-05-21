

f_name = 'input.txt'
# f_name = 'ex1.txt'

def find_abba(s):
    if s[0] == s[3] and s[1] == s[2] and s[0] != s[1]:
        return True
    else:
        return False

valid_addresses = 0
with open(f_name, 'r') as f:
    for line in f.readlines():
        brackets = False
        valid_address = False
        line = line.strip('\n')
        for i in range(len(line) - 3):
            c = line[i]
            if c == '[':
                brackets = True
            elif c == ']':
                brackets = False
            else:
                snippet = line[i:i+4]
                if find_abba(snippet) and brackets:
                    # print(f'Invalid ABBA: {snippet}. Line: {line}')
                    valid_address = False
                    break
                elif find_abba(snippet) and not brackets:
                    valid_address = True
                    # print(f'Valid ABBA: {snippet}')

        if valid_address:
            valid_addresses += 1
            # print(f'Valid: {valid_addresses}. Line: {line}')

print(valid_addresses)

# part 1: 110

