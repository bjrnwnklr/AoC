recipe = '084601'
found = False

scoreboard = '37'
elf1 = 0
elf2 = 1

while not found:
    for i in range(1000):
        scoreboard += str(int(scoreboard[elf1]) + int(scoreboard[elf2]))
        elf1 = (elf1 + 1 + int(scoreboard[elf1])) % len(scoreboard)
        elf2 = (elf2 + 1 + int(scoreboard[elf2])) % len(scoreboard)
    print(i, len(scoreboard))
    if recipe in scoreboard:
        found = True
        j = scoreboard.index(recipe)    
        score = scoreboard[j:j+len(recipe)]
        print('Found %s at %d. Compare: %s' % (recipe, j, score))
