

f_name = 'input.txt'
# f_name = 'ex2.txt'

def decompress(segment):
    # check if no opening paranthises in the segment, this is the end state
    # so just return the length
    if '(' not in segment:
        return len(segment)
    else:
        opening_paranthesis = segment.index('(')
        closing_paranthesis = segment.index(')')
        # get the length and factor of the chunk defined by the parathensis
        length, factor = map(int, ''.join(segment[opening_paranthesis + 1:closing_paranthesis]).split('x'))
        return (len(segment[:opening_paranthesis]) 
            + factor * decompress(segment[closing_paranthesis + 1:closing_paranthesis + 1 + length])
            + decompress(segment[closing_paranthesis + 1 + length:]))

with open(f_name, 'r') as f:
    line = list(f.readline().strip('\n'))
    result = decompress(line)

print(result)
# print(decompressed_text)

# part 1: 112830
# part 2: 10931789799

