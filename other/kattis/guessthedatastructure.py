import sys

if __name__ == '__main__':
    queue = []
    stack = []
    prio = []
    structs = {'q', 's', 'p'}
    m = 0
    n = 0
    c = 0
    for line in sys.stdin:
        ab = line.strip().split()
        if len(ab) == 1:
            n = int(ab[0])
            queue = []
            stack = []
            prio = []
            structs = {'q', 's', 'p'}
            m = 0
            c = 0
        else:
            m += 1
            op = ab[0]
            x = int(ab[1])
            if op == '1':
                # throw x into each data structure
                queue.append(x)
                stack.append(x)
                prio.append(x)
                c += 1
            else:
                # remove from each structure only if there is an element to be taken out of
                if c < 1:
                    structs = set()
                else:
                    c -= 1
                    if 'q' in structs:
                        q_e = queue.pop(0)
                        if x != q_e:
                            structs.remove('q')
                    if 's' in structs:
                        s_e = stack.pop()
                        if x != s_e:
                            structs.remove('s')
                    if 'p' in structs:
                        prio.sort()
                        p_e = prio.pop()
                        if x != p_e:
                            structs.remove('p')

            # determine what type of data structure we have after the last operation of this sequence
            if n == m:
                l = len(structs)
                if l == 0:
                    result = 'impossible'
                elif l > 1:
                    result = 'not sure'
                else:
                    ds = structs.pop()
                    if ds == 'q':
                        result = 'queue'
                    elif ds == 's':
                        result = 'stack'
                    else:
                        result = 'priority queue'

                print(result)