# read in the spreadsheet and split the inputs (could use numpy or pandas!)
with open('input.txt', 'r') as f:
    table = [list(map(int, l.split('\t'))) for l in f.readlines()]

# part 1 (checksum of max-min)
checksum = sum(max(row) - min(row) for row in table)

print('Part 1: ', checksum)

# part 2 (result of evenly divisible numbers summed up)

def even_div(a, b):
    if a % b == 0:
        return a // b
    else:
        return 0

part2 = sum(even_div(a, b) for row in table for a in row for b in row if a != b)

print('Part 2: ', part2)
