# Advent of Code 2021

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

-   Go in the year's directory (e.g. `2021`)
-   Run `../aocsetup.sh 2021 01` to set up the files for day 01
-   The script then copies the template files into the directory and renames the files according to year and day.

## Downloading the day's puzzle input

Use curl:

```shell
$ curl https://adventofcode.com/2021/day/<DAY - no leading zeros!>/input --cookie "session=SESSION" > input/<day - with leading zeros!>.txt
$ curl https://adventofcode.com/2021/day/3/input --cookie "session=SESSION" > input/03.txt
```

Session cookie can be found by:

-   Chrome> Inspect
-   tab over to `Application`
-   Under `Storage`, expand `Cookies`
-   click on the `https://adventofcode.com` cookie
-   grab the value for session.

# Run a solution

The puzzle solutions are in the `solutions` directory. Run a day's solution as a module using the `-m` option. This will get the imports (e.g. from `utils`) correct.

```shell
[aoc/2021] > python -m solutions.aoc2021_03
```

# Testing with `pytest`

Tests are located in the `tests` subdirectory and should be used to test the examples given in the puzzle description. Run a test from within the year's directory with `pytest`, using either the path/filename of the testfile to run or use the `-k` (keyword) option and specify the day:

```shell
[aoc/2021] > pytest tests/test_aoc2021_03.py
[aoc/2021] > pytest -k "03"
```

# Runtimes of each day's puzzles

| Day            | Part 1    | Part 2    |
| -------------- | --------- | --------- |
| 01             | 0.00011s  | 0.00010s  |
| 02             | 0.00046s  | 0.00053s  |
| 03             | 0.00111s  | 0.24616s  |
| 04             | 0.03663s  | 0.08512s  |
| 05             | 0.00963s  | 0.04935s  |
| 06             | 0.26910s  | 0.00005s  |
| 07             | 0.17909s  | 0.21780s  |
| 08             | 0.00011s  | 0.00569s  |
| 09             | 0.01703s  | 0.03075s  |
| 10             | 0.00096s  | 0.00162s  |
| 11             | 0.01309s  | 0.02497s  |
| 12             | 0.02804s  | 0.18777s  |
| 13             | 0.00125s  | 0.00110s  |
| 14             | 0.00488s  | 0.00184s  |
| 15             | 0.02843s  | 1.01795s  |
| 16             | 0.00303s  | 0.00339s  |
| 17             | 0.04259s  | 0.04227s  |
| 18             | 0.12547s  | 2.06122s  |
| 19             |           | 0.54753s  |
| 20             | 0.07050s  | 3.87139s  |
| 21             | 0.00019s  | 0.03530s  |
| 22             | 0.00159s  | 1.09830s  |
| 23             | 0.94221s  | 4.67143s  |
| 24             | 50.75133s | 50.80724s |
| 24 (optimized) | 0.52629s  | 0.51274s  |
| 25             | 1.43875s  |           |

Notes:

-   Day 06, part 1 needs to be optimized to use the same algorithm as part 2 (which is highly optimized)
-   Day 19, part 2 runs both part 1 and 2 solutions at the same time. Runtime for part 1 is the same as part 2 as part 2 does not add a lot of overhead
-   Day 23, part 1: Resolved in a few hours, however getting it to perform was hard. Took several attempts at refactoring. The results are based on the A\* algorithm (run `aoc2021_23_astar.py` for part 1 and `aoc2021_23_solver.py` for part 1 and part 2 results).
