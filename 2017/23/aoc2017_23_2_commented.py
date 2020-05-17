
def print_regs():
    for k, v in zip(list('abcdefgh'), [a, b, c, d, e, f, g, h]):
        print(f'[{k}] = {v}')



a = 1
b = c = d = e = f = g = h = 0


b = 99
c = b

if a > 0:
    b *= 100
    b -= -100_000
    c = b
    c -= -17_000

    # at this point: 
    # b = 109_900
    # c = 126_900

print_regs()

# line 8
while True:
    f = 1
    d = 2


    # while True:
    #     e = 2
    #     while True:
    #         g = d       ## line 11
    #         g *= e
    #         g -= b

    #         # g = (d * e) - b

                        ## if b == d * e
                        ## with d = 2, this means e = b/2 = 54950

    #         if g == 0:
    #             f = 0

    #         e += 1
    #         g = e
    #         g -= b

                        ## if  b == e

    #         # g = (e + 1) - b

    #         # print(f'Loop 3 end')
    #         # print_regs()
    #         # jump back to 11
    #         if g == 0:
    #             break

        
    #     d += 1     ## increase d by 1, so factor for f = 0 changes
    #     g = d
    #     g -= b

    #     print(f'Loop 2 end')
    #     print_regs()

    #     if g == 0:    ## if d == b, exit loop. 
    #                   ##   F is only set if b % d == 0
    #         break
    f = 0

    if f == 0:
        h += 1
    g = b
    g -= c

    print(f'Loop 1 end.')
    print_regs()

    if g == 0:
        break

    b += 17


print(f'Program finished. h={h}')


# the program steps from 109_900 to 126_900 (17000) by increases of 17
# - so 1000 steps

# it then counts how many of the numbers are not prime!

# every time a divisor is found, it increases h