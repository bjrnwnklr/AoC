import re


class TuringComputer:
    def __init__(self, pgm):
        self.registers = {
            'a': 0,
            'b': 0
        }
        self.ip = 0
        self.pgm = pgm
        self.upper_boundary = len(self.pgm)

    @classmethod
    def from_file(cls, f_name):
        pgm = dict()
        with open(f_name, 'r') as f:
            for i, line in enumerate(f.readlines()):
                pgm[i] = line.strip()

        return cls(pgm)

    def run(self):
        while self.ip < self.upper_boundary:
            instruction = self.pgm[self.ip]
            cmd = instruction[:3]
            if cmd == 'hlf':
                reg = instruction[4:5]
                self.registers[reg] = self.registers[reg] // 2
                self.ip += 1
            elif cmd == 'tpl':
                reg = instruction[4:5]
                self.registers[reg] = self.registers[reg] * 3
                self.ip += 1
            elif cmd == 'inc':
                reg = instruction[4:5]
                self.registers[reg] += 1
                self.ip += 1
            elif cmd == 'jmp':
                m = re.search(r'(-?\d+)', instruction)
                offset = int(m.group(1))
                self.ip += offset
            elif cmd == 'jie':
                reg = instruction[4:5]
                m = re.search(r'(-?\d+)', instruction)
                offset = int(m.group(1))
                if self.registers[reg] % 2 == 0:
                    self.ip += offset
                else:
                    self.ip += 1
            elif cmd == 'jio':
                reg = instruction[4:5]
                m = re.search(r'(-?\d+)', instruction)
                offset = int(m.group(1))
                if self.registers[reg] == 1:
                    self.ip += offset
                else:
                    self.ip += 1

    def get_result(self):
        return self.registers['b']

if __name__ == '__main__':

    # f_name = 'ex1.txt'
    f_name = 'input.txt'

    tc = TuringComputer.from_file(f_name)
    tc.registers['a'] = 1
    tc.run()
    print(tc.get_result())

    # Part 1: 170
    # Part 2: 247

