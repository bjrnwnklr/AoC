with open('input.txt', 'r') as f_in:
    with open('input_annotated.txt', 'w') as f_out:
        for i, line in enumerate(f_in.readlines()):
            f_out.write(f'[{i:02}]: {line}')