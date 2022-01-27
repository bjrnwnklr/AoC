

if __name__ == '__main__':
    f_in_name = 'input/24.txt'
    f_out_name = 'solutions/24_segments_sorted.txt'

    with open(f_in_name, 'r') as f_in:
        lines = f_in.readlines()

    with open(f_out_name, 'w') as f_out:
        for i in range(18):
            f_out.write(f'LINE {i}:\n')
            for segment in range(14):
                f_out.write(f'[{segment:02}] {lines[i + segment * 18]}')
            f_out.write('\n')
