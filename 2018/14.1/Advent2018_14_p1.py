input_len = '084601'
n = int(input_len)

scoreboard = '37'
elf1 = 0
elf2 = 1

for i in range(n+11):
    scoreboard += str(int(scoreboard[elf1]) + int(scoreboard[elf2]))
    elf1 = (elf1 + 1 + int(scoreboard[elf1])) % len(scoreboard)
    elf2 = (elf2 + 1 + int(scoreboard[elf2])) % len(scoreboard)
print(scoreboard[n:n+10])
