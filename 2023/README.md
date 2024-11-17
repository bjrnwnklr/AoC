# Advent of Code 2023

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

-   Go in the year's directory (e.g. `2023`)
-   Run `../aocsetup.sh 2023 01` to set up the files for day 01
-   The script then copies the template files into the directory and renames the files according to year and day.

## Downloading the day's puzzle input

Use curl:

```shell
$ curl https://adventofcode.com/2023/day/<DAY - no leading zeros!>/input --cookie "session=SESSION" > input/<day - with leading zeros!>.txt
$ curl https://adventofcode.com/2023/day/3/input -A "bjoern@bjoern-winkler.de via curl" --cookie "session=SESSION" > input/03.txt
```

Session cookie can be found by:

-   Chrome> Inspect
-   Under `Storage`, expand `Cookies`
-   click on the `https://adventofcode.com` cookie
-   grab the value for session.

# Run a solution

The puzzle solutions are in the `solutions` directory. Run a day's solution as a module using the `-m` option. This will get the imports (e.g. from `utils`) correct.

```shell
[aoc/2023] > python -m solutions.aoc2021_03
```

# Testing with `pytest`

Tests are located in the `tests` subdirectory and should be used to test the examples given in the puzzle description. Run a test from within the year's directory with `pytest`, using either the path/filename of the testfile to run or use the `-k` (keyword) option and specify the day:

```shell
[aoc/2023] > pytest tests/test_aoc2023_03.py
[aoc/2023] > pytest -k "03"
```

# Runtimes of each day's puzzles

| Day | Part 1   | Part 2    |
| --- | -------- | --------- |
| 01  | 0.00110s | 0.00298s  |
| 02  | 0.00068s | 0.00065s  |
| 03  | 0.00242s | 0.00185s  |
| 04  | 0.00184s | 0.00153s  |
| 05  | 0.00056s | 0.00092s  |
| 06  | 0.00002s | 3.87630s  |
| 07  | 0.00448s | 0.01991s  |
| 08  | 0.00381s | 0.02567s  |
| 09  | 0.00250s | 0.00243s  |
| 10  | 0.01347s | 0.32280s  |
| 11  | 0.01365s | 0.01895s  |
| 12  | 0.02617s | 0.77054s  |
| 13  | 0.00601s | 0.37268s  |
| 14  | 0.00129s | 5.03380s  |
| 15  | 0.00202s | 0.00297s  |
| 16  | 0.00878s | 2.45749s  |
| 17  | 0.56034s | 1.95548s  |
| 18  | 0.00041s | 0.00041s  |
| 19  | 0.00304s | 0.00189s  |
| 20  | 0.35214s | 1.20569s  |
| 21  | 0.01164s | 0.18673s  |
| 22  | 0.06124s | 6.81641s  |
| 23  | 1.36435s | 77.03804s |
| 24  | 0.06566s | 2.22686s  |
| 25  | 0.13716s |           |
