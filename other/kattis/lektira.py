import sys
import re


def next_words(w, n):
    # return the reversed word if we are at the last word (n == 0)
    if n == 0:
        return w[::-1]

    # find the lowest letter in the eligible words (eligible - needs to leave enough letters to generate additional
    # words if required
    elig_word = w[:-n]
    min_letter = sorted(list(elig_word))[0]

    # find positions of lowest letter in eligible word
    matches = re.finditer(min_letter, elig_word)
    pos_list = [m.start(0) for m in matches]

    # generate pairs of words:
    # 1) word starting with lowest character (reversed)
    # 2) remaining word (not reversed)
    list_of_results = [
        (elig_word[p::-1], w[p + 1:])
        for p in pos_list
    ]

    # get list of results and concat with w1, sort concatenated words and return the first word
    return sorted([
        w1 + next_words(w2, n - 1)
        for w1, w2 in list_of_results
    ])[0]


if __name__ == '__main__':
    for line in sys.stdin:
        word = line.strip()

        print(next_words(word, 2))
