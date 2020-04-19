# Day 1 AoC 2019

# Part 1:
# - Load file (individual numbers per line)
# - Calculate the fuel required:
# -- divide by 3
# -- round down to int
# -- subtract 2
# - Add all together

# Load data
with open('input.txt', 'r') as f:
    masses = [int(line) for line in f]

fuel = [(m // 3) - 2 for m in masses]

print(f'Part 1: {sum(fuel)}')


# Part 2:
# - Write a function to calculate fuel requirements until 0 is reached

# Example data: 
# 100756 and its fuel is: 33583 + 11192 + 3728 + 1240 + 411 + 135 + 43 + 12 + 2 = 50346

ex_mass = [100756]

def fuel(mass):
    return (mass // 3) - 2

def fuel_sum(mass):
    f_sum = 0
    f = fuel(mass)
    while f > 0:
        f_sum += f
        f = fuel(f)

    return f_sum

fuel_2 = [fuel_sum(m) for m in masses]

print(f'Part 2: {sum(fuel_2)}')


# Part 2 recursive:

def fuel_recursive(mass):
    f = fuel(mass)
    if f > 0:
        return f + fuel_recursive(f)
    else: 
        return 0

fuel_3 = sum(fuel_recursive(m) for m in masses)

print(f'Recursive: {fuel_3}')
