
with open('dl_9_25.bat', 'w', encoding='utf-8') as f:
    for i in range(9, 26):
        print(f'curl https://adventofcode.com/2019/day/{i} --cookie "session=53616c7465645f5fef72a3265f626c2b8f72497f9e328be92389299523c8d085ceb7e291c9deebbffac116a25f69e85d" -o {i}\\2019_{i}_1.html',
        file=f)
        print(f'curl https://adventofcode.com/2019/day/{i}/input --cookie "session=53616c7465645f5fef72a3265f626c2b8f72497f9e328be92389299523c8d085ceb7e291c9deebbffac116a25f69e85d" -o {i}\\input.txt', 
        file=f)

