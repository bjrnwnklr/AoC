

f_name = 'input.txt'
# f_name = 'ex1.txt'

decompressed_text = ''

with open(f_name, 'r') as f:
    line = list(f.readline().strip('\n'))
    while line:
        c = line.pop(0)
        if c == '(':
            closing_parantheses = line.index(')')
            num_chars, times = map(int, ''.join(line[:closing_parantheses]).split('x'))
            # chop off the stuff in brackets incl bracket. we don't need it anymore
            line = line[closing_parantheses+1:]
            # get the segment with length of "num_chars" and repeat it
            segment = line[:num_chars] * times
            # add the repeated segment to our decompressed text
            decompressed_text += ''.join(segment)
            # chop off the segment from line, we don't need it anymore
            line = line[num_chars:]
        else:
            decompressed_text += c

print(len(decompressed_text))
# print(decompressed_text)

# part 1: 112830

