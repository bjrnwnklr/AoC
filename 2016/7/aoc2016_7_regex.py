import re

f_name = 'input.txt'
# f_name = 'ex1.txt'


re_abba_all = r'(?P<first>[a-z])(?P<second>[a-z])(?P=second)(?P=first)'
re_abba_invalid = r'\[[a-z]*?(?P<first>[a-z])(?P<second>[a-z])(?P=second)(?P=first)[a-z]*?\]'

valid_addresses = 0
with open(f_name, 'r') as f:
    for line in f.readlines():
        m_invalids = re.findall(re_abba_invalid, line, )
        if m_invalids:
            # check if letters are the same...
            m = m_invalids[0]
            if m[0] != m[1]:
                print(f'Found invalid: {m_invalids[0]}')
                break
        m_all = re.findall(re_abba_all, line)
        if m_all:
            m = m_all[0]
            if m[0] != m[1]:
                print(f'Found valid: {m_all[0]}')
                valid_addresses += 1

print(valid_addresses)

# part 1: 110

