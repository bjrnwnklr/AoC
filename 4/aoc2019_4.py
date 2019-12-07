import re

inp_low = 264360
inp_hi = 746325

#### part 1

# generate passwords within range
# write two test functions that check for rules
# 1) two adjacent digits are the same (use a regex)
# 2) digits never decrease
# Correct answer: 945

def check_adj(pw):
    regex = r'(\d)\1+'
    return True if re.search(regex, pw) else False
        
def check_digits(pw):
    inc = lambda x: x[0] <= x[1]

    return all(map(inc, [(pw[i], pw[i+1]) for i in range(len(pw) - 1)]))

print('Part 1: ', sum((check_adj(str(pw)) and check_digits(str(pw))) for pw in range(inp_low, inp_hi + 1)))
    
#### part 2
# 3) matching adjacent digits can not be part of a larger group (must be exactly 2 digits; 
# but can have groups with more adjacent matching digits)


def check_adj_exact(pw):
    pwl = list(pw)
    counter = 1
    counts = []
    curr = pwl.pop()
    while pwl:
        e = pwl.pop()
        if curr == e:
            counter += 1
        else:
            counts.append(counter)
            counter = 1
            curr = e
    else:
        counts.append(counter)

    return True if 2 in counts else False


print('Part 2: ', sum((check_adj_exact(str(pw)) and check_digits(str(pw))) for pw in range(inp_low, inp_hi + 1)))

ex = [112233, 123444, 111122]

#print(sum((check_adj_exact(str(pw)) and check_digits(str(pw))) for pw in ex))

for e in ex:
    print(e)
    print('Adjacent: ', check_adj_exact(str(e)))
    print('Not decreasing: ', check_digits(str(e)))

