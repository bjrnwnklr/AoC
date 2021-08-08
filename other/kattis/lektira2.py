import sys

if __name__ == '__main__':
    for line in sys.stdin:
        word = line.strip()

        shortest = word
        for i in range(1, len(word) - 1):
            for j in range(i + 1, len(word)):
                first = word[:i]
                second = word[i:j]
                third = word[j:]
                new_word = first[::-1] + second[::-1] + third[::-1]

                shortest = min(new_word, shortest)

        print(shortest)
