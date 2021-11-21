"""
Creates a neat little batch file that can be used to download Advent of Code input files and also stores the day's part 1 website for offline use

Prep work:
- get the session cookie value (e.g. from Chrome's cookies) and update it below
- create the required directories (mkdir xx from a command prompt) - i should really add this to the script!
- run this python script
- run the batch file

Don't forget to check if any of the daily inputs is included in the website and not an input file.

To do:
- instead of creating a batch file, retrieve the input directly via Python, e.g. using Requests 
- create a daily downloader in Python that takes a day / year combo and creates the dir, downloads the input and creates a stub Python file
- include creating a stub Python file e.g. `aoc2020_10.py` - maybe even using a template file

"""

# Update this before running
session_cookie = "---"
year = 2020
day_from = 10
day_to = 23

with open('dl_aoc_batch.bat', 'w', encoding='utf-8') as f:
    for i in range(day_from, day_to + 1):
        print(f'curl https://adventofcode.com/{year}/day/{i} --cookie "session={session_cookie}" -o {i}\\{year}_{i}_1.html',
        file=f)
        print(f'curl https://adventofcode.com/{year}/day/{i}/input --cookie "session={session_cookie}" -o {i}\\input.txt', 
        file=f)
