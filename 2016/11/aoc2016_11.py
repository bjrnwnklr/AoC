from copy import deepcopy
import logging

input_ex1 = [
    ('M', 'hydrogen', 1),
    ('M', 'lithium', 1),
    ('G', 'hydrogen', 2),
    ('G', 'lithium', 3)
]

input_puz = [
    ('G', 'strontium', 1),
    ('M', 'strontium', 1),
    ('G', 'plutonium', 1),
    ('M', 'plutonium', 1),
    ('G', 'thulium', 2),
    ('G', 'ruthenium', 2),
    ('M', 'ruthenium', 2),
    ('G', 'curium', 2),
    ('M', 'curium', 2),
    ('M', 'thulium', 3)
]

class Component:
    def __init__(self, comp_type, comp_element, floor):
        self.comp_type = comp_type
        self.comp_element = comp_element
        self.floor = floor
        self.abbr = f'{self.comp_element[0].upper()}{self.comp_type}'

    def __repr__(self):
        return f'{self.comp_element}-{self.comp_type}: f{self.floor}'


class FloorConfig:
    def __init__(self):
        self.elevator = 1
        # dictionary with component abbreviation (e.g. 'HG' for hydrogen generator): component object pairs
        self.components = dict()
        self.endstate = '4'

    def add_component(self, component):
        self.components[component.abbr] = component
        # update endstate
        self.endstate += '4'

    def current_state(self):
        cs = f'{str(self.elevator)}'
        for c in sorted(self.components):
            cs += f'{str(self.components[c].floor)}'
        return cs

    def move_component(self, abbr, floor):
        self.components[abbr].floor = floor

    def __repr__(self):
        representation = ''
        for floor in range(4, 0, -1):
            representation += f'F{floor}\t'
            representation += 'E\t' if self.elevator == floor else '\t'
            representation += '\t'.join(c.abbr for c in self.components.values() if c.floor == floor) + '\n'
        representation += self.current_state() + '\n'
        return representation

    def possible_moves(self):
        """
        Generate a list of possible moves, i.e. possible states. This will generate all possible combinations
        of moving 1-2 components from the current floor to the floors -1 and +1 and check if the new state generated
        is possible, i.e. that no chips get fried.

        The method will return a list of copies of the current state with the respective components and the
        elevator moved to the new floor.

        This list can then be used to run a BFS on the possible next moves.
        :return: A list of FloorConfig objects, representing a possible next move.
        """
        # get list of possible floors
        next_floors = [self.elevator + i for i in [-1, 1] if 1 <= self.elevator + i <= 4]
        logging.debug(f'Next floors: {next_floors}')



if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    fc = FloorConfig()

    inp = input_ex1
    # inp = input_puz

    for c, e, f in inp:
        fc.add_component(Component(c, e, f))

    print(fc)
    print(fc.endstate)

    # test deepcopy and changing an element in the copy
    fc_copy = deepcopy(fc)

    print(fc_copy)

    # fc_copy.components['HM'].floor = 2
    fc_copy.move_component('HM', 2)
    print(fc)
    print(fc_copy)

    fc.possible_moves()