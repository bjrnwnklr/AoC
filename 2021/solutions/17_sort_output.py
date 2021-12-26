with open('testinput/17_2_test_output.txt', 'r') as f:
    bw_output = []
    for line in f.readlines():
        bw_output.append(tuple(map(int, line.strip().split(','))))

with open('testinput/17_2_example.txt', 'r') as f:
    example_output = []
    for line in f.readlines():
        example_output.append(tuple(map(int, line.strip().split(','))))

print('Not in bw output:')
for line in example_output:
    if line not in bw_output:
        print(line)

print('Not in example output:')
for line in bw_output:
    if line not in example_output:
        print(line)

print('Example output, sorted')
for line in sorted(example_output):
    print(line)
