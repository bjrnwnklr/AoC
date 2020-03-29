def f_6027():
    global r0
    global r1
    print(f'Top, r0: {r0}, r1: {r1}')
    if not r0:
        # print(f'2nd-a, r0: {r0}, r1: {r1}')
        r0 = r1 + 1
        # print(f'2nd-b, r0: {r0}, r1: {r1}')
        return # return what?
    if not r1:
        # print(f'3rd-a, r0: {r0}, r1: {r1}')
        r0 -= 1
        r1 = r7
        f_6027()
        # print(f'3rd-b, r0: {r0}, r1: {r1}')
        return # return what?
    r0_tmp = r0 # push r0
    r1 -= 1
    f_6027()
    r1 = r0
    r0 = r0_tmp
    r0 -= 1
    f_6027()
    return

r0 = 4
r1 = 1
r7 = 6

print('starting')

f_6027()