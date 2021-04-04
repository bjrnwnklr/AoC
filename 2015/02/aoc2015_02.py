# f_name = 'ex1.txt'
f_name = 'input.txt'

total = 0
ribbon = 0
with open(f_name, 'r') as f:
    for line in f.readlines():
        l, w, h = map(int, line.strip().split('x'))
        sides = [l*w, w*h, l*h]
        total += sum(2 * s for s in sides) + min(sides)

        perimeter = 2 * sorted([l, w, h])[0] + 2 * sorted([l, w, h])[1]
        ribbon += perimeter + l * w * h

print(total)
print(ribbon)

# Part 1: 1598415
# Part 2: 3812909

