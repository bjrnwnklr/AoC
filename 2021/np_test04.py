import numpy as np


def bingo(a):
    rows = a.all(axis=1)
    row_bingo = rows.any()
    print('Rows:')
    print(rows)
    print(row_bingo)

    cols = a.all(axis=0)
    col_bingo = cols.any()
    print('Columns:')
    print(cols)
    print(col_bingo)

    return col_bingo or row_bingo


if __name__ == '__main__':
    z = np.zeros((5, 5), dtype=bool)

    # set element [2, 4] to True
    a = z.copy()
    a[2, 4] = True

    print('One element marked:')
    print(a)
    print(bingo(a))
    print('\n\n')

    # create a full row
    a = z.copy()
    a[2] = True

    print('One row marked.')
    print(a)
    print(bingo(a))
    print('\n\n')

    # create a full column
    a = z.copy()
    a[:, 2] = True

    print('One column marked.')
    print(a)
    print(bingo(a))
    print('\n\n')
