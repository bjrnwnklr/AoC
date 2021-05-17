
def calc_presents(n):
    result = n * 10
    for i in range(1, (n // 2) + 1):
        if n % i == 0:
            # print(i)
            result += i * 10

    return result


if __name__ == '__main__':

    # f_name = 'ex1.txt'
    f_name = 'input.txt'

    with open(f_name, 'r') as f:
        req_presents = int(f.readline().strip())

    presents = dict()

    n = 20_000_000
    j = 370_000
    result = 0
    while result < n:
        j += 1
        result = calc_presents(j)

    print(j, result)

    # print(calc_presents(815_500))

    # for j in range(1, 100):
    #     presents[j] = calc_presents(j)

    # for k in sorted(presents, key=lambda x: presents[x], reverse=True):
    #     print(k, presents[k])


