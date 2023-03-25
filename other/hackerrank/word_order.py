# https://www.hackerrank.com/challenges/word-order/problem?isFullScreen=true

# Enter your code here. Read input from STDIN. Print output to STDOUT
n = int(input().strip())

words = []

for _ in range(n):
    words.append(input().strip().strip("\n"))

word_count = dict()
unique_words = []

for word in words:
    word_count[word] = word_count.get(word, 0) + 1

print(len(word_count))

# print unique word counts in order, but only once
# for each word
print(" ".join(str(word_count[w]) for w in word_count))
