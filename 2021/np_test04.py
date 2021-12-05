import numpy as np


def diagonal(x1, y1, x2, y2, a):
    # sort pairs by minimum y coordinate (start with upper row)
    pos1 = min([(x1, y1), (x2, y2)], key=lambda x: x[1])
    pos2 = max([(x1, y1), (x2, y2)], key=lambda x: x[1])

    # if x1 > x2, we need to walk backwards on the x axis
    direction = -1 if pos1[0] > pos2[0] else 1

    coords = []
    for i in range(pos2[1] + 1 - pos1[1]):
        coords.append((pos1[1] + i, pos1[0] + (direction * i)))

    for pos in coords:
        a[pos] += 1


if __name__ == '__main__':
    z = np.zeros((10, 10))

    a = z.copy()
    print(a)

    # TODO: generate the indices by +1 each x and y value

    x1 = 6
    y1 = 4

    x2 = 2
    y2 = 0

    diagonal(x1, y1, x2, y2, a)
    print(a)

    x1 = 8
    y1 = 0

    x2 = 0
    y2 = 8

    diagonal(x1, y1, x2, y2, a)
    print(a)

    x1 = 0
    y1 = 9
    x2 = 5
    y2 = 9

    diagonal(x1, y1, x2, y2, a)
    print(a)
