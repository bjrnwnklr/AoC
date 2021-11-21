import logging
from gameconsole import GameConsole

if __name__ == '__main__':
    # set logging level
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)

    # read in input
    f_name = 'input.txt'

    hgc = GameConsole.from_file(f_name)
    status = hgc.run()

    # part 1: 1087
