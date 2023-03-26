# https://www.hackerrank.com/challenges/the-minion-game/problem
def minion_game(string):
    # your code goes here
    vowels = ["A", "E", "I", "O", "U"]

    # Stuart: consonants
    # Kevin: vowels

    # create all possible substrings, then allocate points
    # based on whether the substring starts with a consonant
    # or a vowel
    stuart = 0
    kevin = 0
    l = len(string)
    for i in range(l):
        if string[i] in vowels:
            kevin += l - i
        else:
            stuart += l - i

    if kevin > stuart:
        result = f"Kevin {kevin}"
    elif kevin < stuart:
        result = f"Stuart {stuart}"
    else:
        result = "Draw"

    print(result)


if __name__ == "__main__":
    s = input()
    minion_game(s)

    # expected
    # test case 5
    # Kevin 25005000
