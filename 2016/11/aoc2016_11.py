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
        self.floors = {
            i: set()
            for i in range(1, 5)
        }
        self.components = dict()
        self.endstate = '4'

    def add_component(self, component):
        self.floors[component.floor].add(component)
        self.components[component.abbr] = component.floor
        # update endstate
        self.endstate += '4'

    def current_state(self):
        cs = f'{str(self.elevator)}'
        for c, f in sorted(self.components.items()):
            cs += f'{str(f)}'
        return cs

    def __repr__(self):
        representation = ''
        for floor in range(4, 0, -1):
            representation += f'F{floor}\t'
            representation += 'E\t' if self.elevator == floor else '\t'
            representation += '\t'.join(c.abbr for c in self.floors[floor]) + '\n'
        representation += self.current_state() + '\n'
        return representation


if __name__ == '__main__':
    fc = FloorConfig()
    fc.add_component(Component('M', 'hydrogen', 1))
    fc.add_component(Component('M', 'lithium', 1))
    fc.add_component(Component('G', 'hydrogen', 2))
    fc.add_component(Component('G', 'lithium', 3))

    print(fc)
    print(fc.endstate)