import re


def rule_1(password):
    pw = [ord(c) for c in password]
    straight = False
    i = 1
    s_count = 1
    while not straight and i < len(pw):
        if pw[i] - pw[i-1] == 1:
            s_count += 1
            if s_count >= 3:
                straight = True
        else:
            s_count = 1
        i += 1
    return straight


def rule_2(password):
    r = re.search(r'[iol]', password)
    if r:
        pw = list(password)
        pos = r.start()
        pw[pos] = chr(ord(pw[pos]) + 1)
        pw[pos + 1:] = 'a' * len(pw[pos + 1:])
        password = ''.join(pw)
    return password


def rule_3(password):
    regex = r'([a-z])\1.*([a-z])\2'
    r = re.search(regex, password)
    return r and r.group(1) != r.group(2)


def incr_pw(password):
    """
    Unicode integer representation of a letter can be returned with `ord()`, the reverse function is
    `chr()`. 'a' = 97, 'z' = 122.
    :param password:
    :return:
    """
    pw = list(password)
    wrapped = True
    i = 0
    while wrapped:
        n = -1 - i
        c = ord(pw[n]) + 1
        if c > 122:
            c = c - 26
        else:
            wrapped = False
        pw[n] = chr(c)
        i += 1

    return rule_2(''.join(pw))


def is_valid_pw(password):
    result = rule_1(password) and rule_3(password)
    return result


def pw_generator(password):
    pw = incr_pw(password)
    while not is_valid_pw(pw):
        pw = incr_pw(pw)
    return pw


if __name__ == '__main__':

    # f_name = 'ex1.txt'
    f_name = 'input.txt'

    with open(f_name, 'r') as f:
        lines = f.readlines()
        for line in lines:
            pw = line.strip()
            print(f'{pw}: {pw_generator(pw)}')

    # part 1: hepxxyzz
    
