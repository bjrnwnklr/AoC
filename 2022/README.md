# Advent of Code 2022

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

-   Go in the year's directory (e.g. `2022`)
-   Run `../aocsetup.sh 2022 01` to set up the files for day 01
-   The script then copies the template files into the directory and renames the files according to year and day.

## Downloading the day's puzzle input

Use curl:

```shell
$ curl https://adventofcode.com/2022/day/<DAY - no leading zeros!>/input --cookie "session=SESSION" > input/<day - with leading zeros!>.txt
$ curl https://adventofcode.com/2022/day/3/input -A "bjoern@bjoern-winkler.de via curl" --cookie "session=SESSION" > input/03.txt
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
[aoc/2022] > python -m solutions.aoc2021_03
```

# Testing with `pytest`

Tests are located in the `tests` subdirectory and should be used to test the examples given in the puzzle description. Run a test from within the year's directory with `pytest`, using either the path/filename of the testfile to run or use the `-k` (keyword) option and specify the day:

```shell
[aoc/2022] > pytest tests/test_aoc2022_03.py
[aoc/2022] > pytest -k "03"
```

# Runtimes of each day's puzzles

| Day | Part 1  | Part 2   |
| --- | ------- | -------- |
| 01  | 0.00040 | 0.00039  |
| 02  | 0.00097 | 0.00094  |
| 03  | 0.00065 | 0.00069  |
| 04  | 0.00008 | 0.00006  |
| 05  | 0.00060 | 0.00075  |
| 06  | 0.00046 | 0.00271  |
| 07  | 0.00090 | 0.00084  |
| 08  | 0.05325 | 0.04276  |
| 09  | 0.01072 | 0.04979  |
| 10  | 0.00012 | 0.00047  |
| 11  | 0.00471 | 2.02125  |
| 12  | 0.01336 | 1.18422  |
| 13  | 0.00068 | 0.01076  |
| 14  | 0.20075 | 5.63967  |
| 15  | 0.01006 | 23.29471 |
| 16  | 2.88282 | 2.55046  |
| 17  |         |          |
| 18  |         |          |
| 19  |         |          |
| 20  |         |          |
| 21  |         |          |
| 22  |         |          |
| 23  |         |          |
| 24  |         |          |
| 24  |         |          |
| 25  |         |          |
