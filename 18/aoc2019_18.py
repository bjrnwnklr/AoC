# AOC 2019, day 18
import logging





#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.INFO)

    f_name = 'input.txt'

    with open(f_name) as f:
        orbits = [l.strip('\n').split(')') for l in f.readlines()]