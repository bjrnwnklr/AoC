"""
Downloads input for Advent of Code.
"""

import argparse
from pathlib import Path
import logging
import requests


# Constant declarations
VERSION = "1.1"
YEAR_FROM = 2015
YEAR_TO = 2023
URL_STUB = "https://adventofcode.com"

# Update this with a valid session cookie before running
SESSION_COOKIE = "---"

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int, help="year to download")
    parser.add_argument("day", type=int, help="day to download")
    parser.add_argument(
        "-v", "--verbose", help="increase output verbosity", action="store_true"
    )
    parser.add_argument(
        "-o",
        "--offline",
        help="prepare for offline use by downloading AoC HTML page for the day",
        action="store_true",
    )
    parser.add_argument(
        "-s", "--sessioncookie", help="session cookie for the AoC website"
    )
    args = parser.parse_args()

    # check if --verbose was set
    if args.verbose:
        # set logging level to INFO
        logging.basicConfig(level=logging.INFO)
    else:
        # standard is ERRORS only
        logging.basicConfig(level=logging.ERROR)

    # handle year and day arguments
    year = args.year
    day = args.day

    # do some sense checking on the year and day
    if year < YEAR_FROM or year > YEAR_TO:
        raise ValueError(
            f"Year {year} is not valid. Year must be {YEAR_FROM} <= year <= {YEAR_TO}."
        )
    if day < 1 or day > 25:
        raise ValueError(f"Day {day} is not valid. Day must be 01 <= day <= 25.")

    # print a little message saying what we are going to do
    print(f"Advent of Code downloader, v{VERSION}.")
    print("(c) 2021, Bjoern Winkler")
    print(f"-- Downloading AoC {year}, day {day} --")

    # check if session cookie is set either via cmd line argument or in code,
    # otherwise abort
    if args.sessioncookie:
        SESSION_COOKIE = args.sessioncookie
        logging.info(f"Setting session cookie to {SESSION_COOKIE}.")
    elif SESSION_COOKIE == "---":
        raise ValueError("SESSION COOKIE NOT SET!!!!")

    # check if a directory for the day exists
    p = Path(".") / f"{day:02}"
    if not p.exists():
        logging.info(f"Directory {p} does not exist, creating it.")
        p.mkdir()

    # create a number of stub files
    files = {
        # 'stub': f'aoc{year}_{day:02}.py',
        # 'md': f'{day:02}.md',
        # 'ex': 'ex1.txt'
    }

    for file in files:
        # check if file exists
        # if not, create an empty file
        f_name = p / files[file]
        if not f_name.exists():
            logging.info(f"{file} file {f_name} does not exist, creating it")
            f_name.touch()

    # prepare session cookie etc
    cookies = {"session": SESSION_COOKIE}

    # now get the HTML page if --offline option is set
    if args.offline:
        url_offline = f"{URL_STUB}/{year}/day/{day}"
        response = requests.get(url_offline, cookies=cookies)
        website = response.content

        offline_file = p / f"{year}_{day:02}_1.html"
        with open(offline_file, "wb") as f:
            f.write(website)

        logging.info(
            f"Saving part 1 of {year}/{day} for offline use as {offline_file}."
        )

    # Get the input file - only if it doesn't yet exist in the directory
    input_file = p / "input.txt"

    if not input_file.exists():
        url_input = f"{URL_STUB}/{year}/day/{day}/input"
        response = requests.get(url_input, cookies=cookies)
        input_content = response.content

        with open(input_file, "wb") as f:
            f.write(input_content)

        logging.info(f"Saving input for {year}/{day} as {input_file}.")
