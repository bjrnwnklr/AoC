in_name = 'input.txt'
out_name = 'commented_gc_program.txt'

with open(in_name, 'r') as f:
    with open(out_name, 'w') as f_out:
        for ipcount, line in enumerate(f.readlines()):
            f_out.write(f'{ipcount:03}: {line}')