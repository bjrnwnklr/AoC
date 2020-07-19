import hashlib
import re


puzzle_input = 'cuanljph'
sample_input = 'abc'

def keygen(salt, part):
    _hashes = {}
    def _gen_hash(ind):
        if ind not in _hashes:
            if part == 1:
                _hashes[ind] = hashlib.md5(str(salt + str(ind)).encode()).hexdigest()
            else:
                temp_str = salt + str(ind)
                # run 2017 cycles of MD5 stretching
                for _ in range(2017):
                    temp_str = hashlib.md5(temp_str.encode()).hexdigest()
                _hashes[ind] = temp_str
        return _hashes[ind]

    i = 0
    while True:
        curr_hash = _gen_hash(i)
        # check if triple chars in hash - using:
        # (\w) - any character
        # \1 - a backreference to the matched character
        # {2} - repeat the backreference 2 times
        triple_char = re.compile(r'(.)\1{2}')
        match = triple_char.search(curr_hash)
        if match:
            # get the first char of the match
            c = match[0][0]
            # check if same char exists 5 times in one of the next 1000 hashes
            five_char = re.compile('(' + c + '{5})')
            found = False
            for j in range(i + 1, i + 1001):
                match_2 = five_char.search(_gen_hash(j))
                if match_2:
                    # we found a match! Return hash as key
                    found = True
                    break
            if found:
                yield i, curr_hash
        # check next index
        i += 1

for pt in (1, 2):

    print(f'------- Part {pt} ---------')
    keygen_generator = keygen(puzzle_input, pt)
    for i in range(64):
        k, hashval = next(keygen_generator)
        print(f'{i}: {k} - {hashval}')


# Part 1: 23769
# Part 2: 20606