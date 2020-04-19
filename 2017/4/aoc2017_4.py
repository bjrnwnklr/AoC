# read in passphrases


def passphrase_valid(l):
    phrase_set = set()
    for phrase in l:
        if phrase in phrase_set:
            # phrase already exists
            return False
        else:
            phrase_set.add(phrase)
    return True


f_name = 'input.txt'
phrase_count = 0
valid_phrase_count = 0

with open(f_name, 'r') as f:
    for line in f.readlines():
        passphrase = line.strip().split(' ')
        phrase_count += 1
        if passphrase_valid(passphrase):
            valid_phrase_count += 1


print(f'Part 1. Total phrases: {phrase_count}. Valid phrases: {valid_phrase_count}.')

# Part 1: 466 out of 512

phrase_count = 0
valid_phrase_count = 0

with open(f_name, 'r') as f:
    for line in f.readlines():
        passphrase = line.strip().split(' ')
        passphrase = [str(sorted(w)) for w in passphrase]
        phrase_count += 1
        if passphrase_valid(passphrase):
            valid_phrase_count += 1

print(f'Part 2. Total phrases: {phrase_count}. Valid phrases: {valid_phrase_count}.')

# Part 2. Total phrases: 512. Valid phrases: 251