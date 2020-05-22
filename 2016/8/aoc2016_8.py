import re
import numpy as np
import matplotlib.pyplot as plt

f_name = 'input.txt'
# f_name = 'ex1.txt'

# define display
# dimensions of display: 6 rows, 50 columns
dims = (6, 50)
display = np.zeros(dims)


with open(f_name, 'r') as f:
    for line in f.readlines():
        # find two numbers
        a, b = map(int, re.findall('\d+', line))
        if 'rect' in line:
            display[:b, :a] = 1
        else:
            if 'column' in line:
                display[:, a] = np.concatenate([display[-b:, a], display[:-b, a]])
            else:
                display[a] = np.concatenate([display[a, -b:], display[a, :-b]])

# for part 1, calculate how many pixels are lit
part_1 = np.sum(display)
print(part_1)

# part 1: 128

plt.matshow(display)
plt.show()

# part 2: EOARGPHYAO