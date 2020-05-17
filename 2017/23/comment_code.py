with open('input.txt') as f_in:
    with open('input_commented.txt', 'w') as f_out:
        for i, line in enumerate(f_in.readlines()):
            f_out.write(f'[{i:03}]\t{line}')