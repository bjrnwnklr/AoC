def is_valid(i):
    # check if the number at index i is valid, i.e. the sum of two numbers in the previous 25 numbers
    test_range = xmas_data[i - preamble:i]
    test_value = xmas_data[i]
    for a in test_range:
        if (b := test_value - a) in test_range and a != b:
            return True

    return False


f_name = 'input.txt'

with open(f_name, 'r') as f:
    xmas_data = [int(x.strip('\n')) for x in f.readlines()]

preamble = 25
max_i = len(xmas_data)

for i in range(preamble, max_i):
    if not is_valid(i):
        invalid_number = xmas_data[i]
        print(f'Number {invalid_number} at index {i} is not valid')

        break


# Part 1: Number 373803594 at index 622 is not valid

# Part 2

def find_part2():
    for i in range(0, max_i):
        for j in range(i + 1, max_i):
            temp_sum = sum(xmas_data[i:j + 1])
            if temp_sum == invalid_number:
                print(f'Found range of numbers {i}:{j}.')
                return max(xmas_data[i:j + 1]) + min(xmas_data[i:j + i])

    return 0


print(find_part2())

# Part 2: 51152360 (507:523)
