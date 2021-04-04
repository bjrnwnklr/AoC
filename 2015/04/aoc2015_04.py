import hashlib



def md5_hash_gen_part1(s, n):
    i = 0
    while True:
        test_string = s + str(i)
        # create md5 hash
        result = hashlib.md5(test_string.encode()).hexdigest()
        # yield if the first 5 chars of the hex output are zeroes (result[:5] is a string)
        if result[:n] == '0' * n:
            yield i
        i += 1


if __name__ == '__main__':
    puzzle_input = 'bgvyzdsv'
    part1 = md5_hash_gen_part1(puzzle_input, 6)
    print(next(part1))

# Part 1: 254575
# Part 2: 1038736


