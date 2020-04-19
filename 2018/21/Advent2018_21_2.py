
# initial configuration - instr 0-7
r0, r1, r2, r3, r5 = 0, 0, 65536, 10736359, 0
end = False

###### assign start value for r0
r0 = 0

def print_r(msg, r0, r1, r2, r3, r5):
    print('%s:\t\tr0 = %d, r1 = %d, r2 = %d, r3 = %d, r5 = %d' % (msg, r0, r1, r2, r3, r5))

# instr 8-12
def proc8_12(r1, r2, r3):
    r1 = r2 & 255
    #print('r1:', r1)
    r3 += r1
    #print('r3:', r3)
    r3 &= 16777215
    #print('r3:', r3)
    r3 *= 65899
    #print('r3:', r3)
    r3 &= 16777215
    #print('r3', r3)
    #print_r('proc8_12', r0, r1, r2, r3, r5)
    return r1, r2, r3
    

# instr 18-25
def test_18(r1, r2, r5):
    # find factor i so that (256 * i) > r2
    r1 = r2 // 256
    r5 = 1
    r2 = r1
    #print_r('Factor r2', r0, r1, r2, r3, r5)
    return r1, r2, r5

r3s = []
repeats = []

#print_r('Start', r0, r1, r2, r3, r5)
while not end:
    r1, r2, r3 = proc8_12(r1, r2, r3)
    if 256 > r2:
        # step 13 - 256 > r2
        #print_r('13, 256>r2', r0, r1, r2, r3, r5)
        r1 = 1
        # end program if r3 == r0
        # step 28
        if r3 == r0:
            r1 = 1
            end = True

        else:
            # go back to step 6 and start again
            # step 30
            if r3 in r3s:
                print('r3 found before: %d' % r3)
                if r3 in repeats:
                    print('cycle reached!')
                    print(repeats)
                    print('Part 2: %d' % repeats[-1])
                    end = True
                else:
                    repeats.append(r3)
            else:
                r3s.append(r3)
            #print(r3)
            #print_r('30, r3 != r0', r0, r1, r2, r3, r5)
            r2 = r3 | 65536
            r3 = 10736359

    else:
        # step 17, 18-25
        r1 = 0
        r1, r2, r5 = test_18(r1, r2, r5)
        # go back to processing 8-12


print_r('END', r0, r1, r2, r3, r5)