

f_name = 'input.txt'
# f_name = 'ex1.txt'


def valid_triangle(sides):
    return all(sides[i] < sides[(i+1) % 3] + sides[(i+2) % 3] for i in range(3))

valid_count = 0
with open(f_name, 'r') as f:
    for line in f.readlines():
        sides = list(map(int, line.strip('\n').split()))
        if valid_triangle(sides):
            valid_count += 1


print(valid_count)

# part 1: 869


valid_count = 0
with open(f_name, 'r') as f:
    sides = [list(map(int, line.strip('\n').split())) for line in f.readlines()]

    for r in range(0, len(sides), 3):
        for c in range(3):
            triangle = [sides[r+i][c] for i in range(3)]
            if valid_triangle(triangle):
                valid_count += 1

print(valid_count)

# part 2: 1544