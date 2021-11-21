import re

f_name = 'input.txt'
# f_name = 'ex1.txt'
# f_name = 'ex2.txt'

with open(f_name, 'r') as f:
    passports = [p for p in f.read().split('\n\n')]

mand_fields = [
    'byr',
    'iyr',
    'eyr',
    'hgt',
    'hcl',
    'ecl',
    'pid'
]

opt_fields = [
    'cid'
]

# add all valid passports to this list, we can then just use this for part 2
# and ignore any invalid passports
valid_passports = []

for p in passports:
    if all(f in p for f in mand_fields):
        valid_passports.append(p)

print(f'Part 1: counted {len(valid_passports)} valid passports.')

# Part 1: 230

# functions that evaluate each attribute
byr = lambda x: 1920 <= x <= 2002
iyr = lambda x: 2010 <= x <= 2020
eyr = lambda x: 2020 <= x <= 2030


def hgt(a):
    hgt_match = re.match(r'((\d+)(cm|in))', a)
    if hgt_match:
        if hgt_match.group(3) == 'cm':
            if 150 <= int(hgt_match.group(2)) <= 193:
                return True
        else:
            if 59 <= int(hgt_match.group(2)) <= 76:
                return True
    return False


def hcl(a):
    hcl_match = re.match(r'^\#[0-9a-f]{6}$', a)
    return True if hcl_match else False


ecl = lambda x: x in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']


def pid(a):
    pid_match = re.match(r'^\d{9}$', a)
    return True if pid_match else False


field_pattern = r'(([a-z]*):(\S*))'

valid_count_pt2 = 0

for p in valid_passports:
    attribs = dict()
    matches = re.findall(field_pattern, p)

    if matches:
        for m in matches:
            attribs[m[1]] = m[2]

    # now check the rules for each attribute
    if all([
        byr(int(attribs['byr'])),
        iyr(int(attribs['iyr'])),
        eyr(int(attribs['eyr'])),
        hgt(attribs['hgt']),
        hcl(attribs['hcl']),
        ecl(attribs['ecl']),
        pid(attribs['pid'])
    ]
    ):
        valid_count_pt2 += 1

print(f'Part 2: counted {valid_count_pt2} valid passports.')

# Part 2: 156