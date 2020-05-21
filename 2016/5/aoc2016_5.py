import hashlib

puzzle_input = 'ugkcyxxp'
# puzzle_input = 'abc'

# use a generator to generate hash numbers
def md5_hash_gen_part1(s):
    i = 0
    while True:
        test_string = s + str(i)
        # create md5 hash
        result = hashlib.md5(test_string.encode()).hexdigest()
        # yield if the first 5 chars of the hex output are zeroes (result[:5] is a string)
        if result[:5] == '00000':
            yield result[5]
        i += 1

# use a generator to generate hash numbers
def md5_hash_gen_part2(s):
    i = 0
    seen = set()
    while True:
        test_string = s + str(i)
        # create md5 hash
        result = hashlib.md5(test_string.encode()).hexdigest()
        # yield if the first 5 chars of the hex output are zeroes (result[:5] is a string)
        if result[:5] == '00000' and result[5] in '01234567' and result[5] not in seen:
            seen.add(result[5])
            yield int(result[5]), str(result[6])
        i += 1

# md5_gen = md5_hash_gen_part1(puzzle_input)
# part1 = ''.join(next(md5_gen) for _ in range(8))
# print(part1)

# part 1: d4cd2ee1

part2_gen = md5_hash_gen_part2(puzzle_input)
part_2_result = [0] * 8
for _ in range(8):
    pos, letter = next(part2_gen)
    part_2_result[pos] = letter
    print(part_2_result)

print(''.join(part_2_result))

# part 2: f2c730e5