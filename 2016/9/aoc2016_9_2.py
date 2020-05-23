

f_name = 'input.txt'
# f_name = 'ex2.txt'


def chunker(segment):
    # create chunks of segments that can be processed
    # chunks are separated by (axb)
    # find the first opening '('
    chunks = []
    i = 0
    len_seg = len(segment)
    while segment:
        if '(' in segment:
            opening_paranthesis = segment.index('(')
            if opening_paranthesis != 0:
                # found a chunk before the opening '(', so chop that off and add to chunks
                chunks.append((1, i, opening_paranthesis))
            # cut off from segment and only process the rest
            # update how much we have already processed
            i += opening_paranthesis + 1
            segment = segment[opening_paranthesis + 1:]
            closing_paranthesis = segment.index(')')
            # get the length and factor of the chunk defined by the parathensis
            length, factor = map(int, ''.join(segment[:closing_paranthesis]).split('x'))
            i += closing_paranthesis + 1
            chunks.append((factor, i, length))
            # chop of the processed chunk
            i += length 
            segment = segment[closing_paranthesis + length + 1:]
        else:
            # process the case where no more paranthesises in segment
            chunks.append((1, i, len(segment)))
            segment = []

    return chunks

def decompress(segment):
    # check if no opening paranthises in the segment, this is the end state
    # so just return the length
    if '(' not in segment:
        return len(segment)
    else:
        # otherwise, chunk up the segment into tuples with (factor, start, length) and
        # recursively process the chunks
        chunks = chunker(segment[:])
        result = 0
        for factor, start, length in chunks:
            result += factor * decompress(segment[start:start+length])
        return result

with open(f_name, 'r') as f:
    line = list(f.readline().strip('\n'))
    result = decompress(line)

print(result)
# print(decompressed_text)

# part 1: 112830
# part 2: 10931789799

