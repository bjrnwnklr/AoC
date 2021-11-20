# Advent of Code 2021

# How to set up a new day

- copy the `template` directory and rename to the day's number (with leading zero, e.g. `01`).
- Rename the `aoc2021_nn.py` and `test/test_aoc2021_nn.py` files with the day's number
- Change the highlighted references in both files to the day's number
- Download the input file using the `aoc_downloader.py` file (note this will create a new directory if it doesn't yet exist)

```shell
[aoc/2021] > python ../aoc_downloader.py 2021 01 -s <sessioncookie> --offline --verbose
```

```
usage: aoc_downloader.py [-h] [-v] [-o] [-s SESSIONCOOKIE] year day

positional arguments:
  year                  year to download
  day                   day to download

options:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -o, --offline         prepare for offline use by downloading AoC HTML page for the day
  -s SESSIONCOOKIE, --sessioncookie SESSIONCOOKIE
                        session cookie for the AoC website
```

# Testing with `pytest`

Tests are located in the `test` subdirectory and should be used to test the examples given in the puzzle description. Run a test from within the day's directory with `pytest`:

```shell
[aoc/2021/01] > pytest
```
