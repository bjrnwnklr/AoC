
def look_and_say(line):
    result = []
    count = 0
    last_num = line[0]
    for n in line:
        if n == last_num:
            count += 1
        else:
            result.append(count)
            result.append(last_num)
            count = 1
            last_num = n
    result.append(count)
    result.append(last_num)
    return result


if __name__ == '__main__':

    # f_name = 'ex1.txt'
    f_name = 'input.txt'

    with open(f_name, 'r') as f:
        line = f.readline().strip()

    r = list(map(int, list(line)))
    for _ in range(50):
        r = look_and_say(r)
    print(len(r))

    # Part 1: 360154
    # Part 2: 5103798

