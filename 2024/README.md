# Advent of Code 2024

# How to set up a new day

## Manually

-   copy the files from the `template` directory:
    -   `aocyyyy_dd.py` into the `solutions` directory - this is the actual solution
    -   `test_aocyyyy_dd.py` into the `tests` directory - this contains the test cases for the day's solution
    -   `dd_1_1.txt` into the `testinput` directory - paste the day's test example into this file. Create more files with similar naming if more than one example required.
-   Rename the `solutions/aocyyyy_dd.py`, `tests/test_aocyyyy_dd.py` and `testinput/dd_1_1.txt` files with the day's number
-   Change the highlighted references in both files to the day's number (in the imports, the file names of the input / test files)
-   Download the input file using the `aoc_downloader.py` file (note this will create a new directory if it doesn't yet exist)

## Using the `aocsetup.sh` script

-   Go in the year's directory (e.g. `2024`)
-   Run `../aocsetup.sh 2024 01` to set up the files for day 01
-   The script then copies the template files into the directory and renames the files according to year and day.

## Downloading the day's puzzle input

Use curl:

```shell
$ curl https://adventofcode.com/2024/day/<DAY - no leading zeros!>/input --cookie "session=SESSION" > input/<day - with leading zeros!>.txt
$ curl https://adventofcode.com/2024/day/3/input -A "bjoern@bjoern-winkler.de via curl" --cookie "session=SESSION" > input/03.txt
```

Session cookie can be found by:

-   Chrome> Inspect
-   Under `Storage`, expand `Cookies`
-   click on the `https://adventofcode.com` cookie
-   grab the value for session.

# Run a solution

The puzzle solutions are in the `solutions` directory. Run a day's solution as a module using the `-m` option. This will get the imports (e.g. from `utils`) correct.

```shell
[aoc/2024] > python -m solutions.aoc2024_03
```

# Testing with `pytest`

Tests are located in the `tests` subdirectory and should be used to test the examples given in the puzzle description. Run a test from within the year's directory with `pytest`, using either the path/filename of the testfile to run or use the `-k` (keyword) option and specify the day:

```shell
[aoc/2024] > pytest tests/test_aoc2024_03.py
[aoc/2024] > pytest -k "03"
```

# Runtimes of each day's puzzles

| Day | Part 1 | Part 2 |
| --- | ------ | ------ |
| 01  |        |        |
| 02  |        |        |
| 03  |        |        |
| 04  |        |        |
| 05  |        |        |
| 06  |        |        |
| 07  |        |        |
| 08  |        |        |
| 09  |        |        |
| 10  |        |        |
| 11  |        |        |
| 12  |        |        |
| 13  |        |        |
| 14  |        |        |
| 15  |        |        |
| 16  |        |        |
| 17  |        |        |
| 18  |        |        |
| 19  |        |        |
| 20  |        |        |
| 21  |        |        |
| 22  |        |        |
| 23  |        |        |
| 24  |        |        |
| 24  |        |        |
| 25  |        |        |
