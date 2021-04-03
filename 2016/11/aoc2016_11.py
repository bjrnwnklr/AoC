from copy import deepcopy
import logging
from itertools import combinations
from collections import deque

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

input_pt2 = [
    ('G', 'strontium', 1),
    ('M', 'strontium', 1),
    ('G', 'plutonium', 1),
    ('M', 'plutonium', 1),
    ('G', 'elerium', 1),
    ('M', 'elerium', 1),
    # ('G', 'dilithium', 1),
    # ('M', 'dilithium', 1),
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
        self.counterpart = f'{self.abbr[0]}{"G" if self.abbr[1] == "M" else "M"}'

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

    def is_valid(self):
        """
        Check if the current state represents a valid state, or if any chips on any floor get fried.

        Chips get fried if there is a generator without its associated microchip and another microchip without generator
        on the same floor.
        :return: True if the current state is valid, False otherwise
        """
        fried = False
        floor = 1
        while not fried and floor <= 4:
            # get all components on the floor - we will need this to cover the case where a single
            # microchip is on the floor together with a microchip/generator combination
            all_comps_on_floor = {c for c in self.components if
                                    self.components[c].floor == floor}
            # If there is only one component on the floor, or the components are all of the same type,
            # we have a valid state so only investigate further if not
            if len(all_comps_on_floor) > 1 and len({c[1] for c in all_comps_on_floor}) > 1:
                # get all components on the floor that are single type (i.e. their counterpart is on a different floor)
                single_comps_on_floor = {c for c in all_comps_on_floor if
                                            self.components[self.components[c].counterpart].floor != floor}
                # logging.debug(f'Single elements on floor {floor}: {single_comps_on_floor}')

                # if there is at least one component on the floor, check if there is a (M)icrochip
                # - as we already know there must be a generator with corresponding microchip,
                # which would fry any single chips
                if len(single_comps_on_floor) >= 1 and 'M' in {c[1] for c in single_comps_on_floor}:
                    fried = True

            floor += 1
        # logging.debug(f'State is valid: {not fried}')
        return not fried

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
        # logging.debug('POSSIBLE MOVES')
        next_floors = [self.elevator + i for i in [-1, 1] if 1 <= self.elevator + i <= 4]
        # logging.debug(f'Next floors: {next_floors}')

        # get combinations of components on the current floor
        comps_on_floor = [c for c in self.components if self.components[c].floor == self.elevator]
        # logging.debug(f'Components on current floor: {comps_on_floor}')
        single_combinations = combinations(comps_on_floor, 1)
        dual_combinations = combinations(comps_on_floor, 2)
        # logging.debug(f'1-2 combinations of available components: {available_combinations}')

        # create a copy of the current state, move all combinations of elements to available floors
        # and evaluate if it is a valid state. If yes, add it to a list
        valid_states = []
        for floor in next_floors:
            available_combinations = single_combinations if floor < self.elevator else list(single_combinations) + list(dual_combinations)
            for comb in available_combinations:
                next_state = deepcopy(self)
                # move the elevator
                next_state.elevator = floor
                # move the components
                for c in comb:
                    next_state.move_component(c, floor)
                # logging.debug(f'Created copy for move to floor {floor} with components {comb}:\n{next_state}')
                if next_state.is_valid():
                    valid_states.append(next_state)

        # logging.debug(f'Found {len(valid_states)} valid states.')
        return valid_states



if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    fc = FloorConfig()

    # inp = input_ex1
    # inp = input_puz
    inp = input_pt2

    for c, e, f in inp:
        fc.add_component(Component(c, e, f))

    logging.debug(f'Starting, initial configuration:\n{fc}')
    logging.debug(f'Endstate: {fc.endstate}')

    # run a BFS until we reach the endstate
    q = deque([(fc, 0, [str(fc)])])
    endstate = fc.endstate
    seen = set()

    while q:
        current_config, current_steps, path = q.pop()

        if current_config.current_state() in seen:
            continue

        seen.add(current_config.current_state())

        if current_config.current_state() == endstate:
            print(f'Path:')
            for p in path:
                print(p)
            print(f'End state reached after {current_steps} steps.')
            break

        for next_state in current_config.possible_moves():
            q.appendleft((next_state, current_steps + 1, path + [str(next_state)]))

    # we're done
    print('END!')

    # Part 1: 37 steps (takes 5-10 minutes without optimization)
    # Part 2: 61 steps (takes 20-25 minutes) We can probably count steps to get to the right result?
