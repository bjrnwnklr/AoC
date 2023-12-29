# Load any required modules. Most commonly used:

# import re
from collections import defaultdict, deque
import logging
from math import lcm

from utils.aoctools import aoc_timer

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# logger.addHandler(ch)
fh = logging.FileHandler("2023_20_2.log", mode="w")
fh.setLevel(logging.ERROR)
logger.addHandler(fh)


def load_input(f_name):
    """Loads the puzzle input from the specified file.

    Specify the relative path if loading files from a subdirectory,
    e.g. for loading test inputs, specify `testinput/01_1_1.txt`.
    """
    # return input as list of text lines
    with open(f_name, "r") as f:
        puzzle_input = []
        for line in f.readlines():
            puzzle_input.append(line.strip())

    return puzzle_input


HIGH = "high"
LOW = "low"


class Pulse:
    def __init__(self, sender, receiver, strength) -> None:
        self.sender = sender
        self.receiver = receiver
        self.strength = strength

    def __repr__(self) -> str:
        return f"{self.sender} -{self.strength}-> {self.receiver}"


class Module:
    def __init__(self, name, outputs) -> None:
        self.name = name
        self.outputs = outputs
        self.type = None

    def process(self, pulse: Pulse):
        pass


class FlipFlop(Module):
    def __init__(self, name, outputs) -> None:
        super().__init__(name, outputs)
        self.type = "FlipFlop"
        self.on = False

    def process(self, pulse: Pulse):
        """Process the received pulse and return a list of
        pulses to be sent to outputs.

        If the input pulse is HIGH, no pulses will be sent on, so
        an empty list is returned."""
        signals = []
        if pulse.strength == LOW:
            if self.on:
                send = LOW
            else:
                send = HIGH
            # send pulse to each output
            for o in self.outputs:
                signals.append(Pulse(self.name, o, send))
            # flip status
            self.on = False if self.on else True

        return signals

    def __repr__(self) -> str:
        return f"{self.type}: {self.name}. On: {self.on}"


class Conjunction(Module):
    def __init__(self, name, outputs) -> None:
        super().__init__(name, outputs)
        self.type = "Conjunction"
        self.mem = defaultdict(lambda: LOW)

    def process(self, pulse: Pulse):
        # update status for the input received from
        self.mem[pulse.sender] = pulse.strength
        # send a high pulse if all inputs had sent high pulses
        if all(v == HIGH for v in self.mem.values()):
            send = LOW
        else:
            send = HIGH
        signals = []
        for o in self.outputs:
            signals.append(Pulse(self.name, o, send))

        return signals

    def register_input(self, input):
        self.mem[input] == LOW

    def __repr__(self) -> str:
        return f"{self.type}: {self.name}. Memory: {self.mem.items()}"


class Broadcaster(Module):
    def __init__(self, name, outputs) -> None:
        super().__init__(name, outputs)
        self.type = "Broadcaster"

    def process(self, pulse: Pulse) -> list:
        signals = []
        for o in self.outputs:
            signals.append(Pulse(self.name, o, pulse.strength))

        return signals

    def __repr__(self) -> str:
        return f"{self.type}: {self.name}"


class Machine:
    def __init__(self, config) -> None:
        logger.debug("Initializing Machine")
        self.pulses_sent = defaultdict(int)
        self.broadcaster = None
        self.modules = dict()
        self.ff_modules = dict()
        self.con_modules = dict()
        self.config = config
        self.inputs = defaultdict(list)
        self.queue = deque([])
        self.button_presses = 0
        self.cycles = defaultdict(list)

        # load initial configuration
        self._load_config()
        logger.debug("Finished initializing Machine: {self}")

    def __repr__(self) -> str:
        return (
            f"Machine - {self.broadcaster}, Modules: {self.modules}, "
            + f"Pulses sent: {self.pulses_sent}"
        )

    def _load_config(self):
        logger.debug("Machine: Loading config")
        for line in self.config:
            logger.debug(f"Machine: loading line {line}")
            sender, receivers = line.strip().split(" -> ")
            outputs = [x.strip() for x in receivers.strip().split(",")]
            if sender == "broadcaster":
                self.broadcaster = Broadcaster(sender, outputs)
                self.modules[sender] = self.broadcaster
            elif sender[0] == "%":
                # flip flop modules
                # strip name of the pre-fix, will make it easier to reference
                sender = sender[1:]
                m = FlipFlop(sender, outputs)
                self.modules[sender] = m
                self.ff_modules[sender] = m
            elif sender[0] == "&":
                # conjunction module
                # strip name of the pre-fix, will make it easier to reference
                sender = sender[1:]
                m = Conjunction(sender, outputs)
                self.modules[sender] = m
                self.con_modules[sender] = m

            # register senders as inputs against all outputs
            for o in outputs:
                self.inputs[o].append(sender)

        # once all modules have been processed, register the inputs
        # to the conjunction modules
        for receiver in self.inputs:
            # register each logged input if it is a Conjunction module
            if receiver in self.con_modules:
                logger.debug(f"Registering inputs for {receiver}")
                for i in self.inputs[receiver]:
                    logger.debug(f"Registering input {i}")
                    self.con_modules[receiver].register_input(i)
                logger.debug(
                    f"Registered for {receiver}: {self.con_modules[receiver].mem.items()}"
                )

    def press_button(self):
        """Simulate pressing a button and running through the
        queue once until it is empty."""
        rx_low_pulses = 0
        self.button_presses += 1
        logger.debug(f"Button pressed {self.button_presses} times.")
        p = Pulse("button", self.broadcaster.name, LOW)
        self.queue.append(p)
        while self.queue:
            pulse = self.queue.popleft()
            logger.debug(f"Pulse: {pulse}")
            # increase pulse count
            self.pulses_sent[pulse.strength] += 1
            # proceed if pulse receiver is a valid module, otherwise
            # just discard (e.g. for the 'output' modules)
            if pulse.receiver in self.modules:
                # get resulting pulses from processing the pulse
                next_pulses = self.modules[pulse.receiver].process(pulse)
                if next_pulses:
                    self.queue.extend(next_pulses)
                    logger.debug(f"Received pulses and added to queue: {self.queue}")
                else:
                    logger.debug(f"No pulses received. Queue: {self.queue}")
            else:
                # part 2
                if pulse.receiver == "rx":
                    if pulse.strength == LOW:
                        # we will never get to this point as it is only reached after
                        # a lot of button presses...
                        rx_low_pulses += 1
                        logger.debug(
                            f"Low pulse received for receiver rx. low pulse count this turn: {rx_low_pulses}"
                        )
                    else:
                        # rx was pulsed but with a HIGH pulse. Meaning, one of the
                        # 4 registers feeding rx was all set to HIGH
                        lv_mem = self.modules[pulse.sender].mem
                        if sum(1 if lv_mem[x] == HIGH else 0 for x in lv_mem) >= 1:
                            logger.debug(
                                f"[{self.button_presses}]: HIGH in LV register: {lv_mem.items()}"
                            )
                            # store button press (i.e. cycles) in a dict for the register that hit all 1s
                            reg = [x for x in lv_mem if lv_mem[x] == HIGH]
                            for r in reg:
                                if self.button_presses not in self.cycles[r]:
                                    self.cycles[r].append(self.button_presses)

                                logger.info(
                                    f"[{self.button_presses}]: cycles: {self.cycles}"
                                )

                logger.debug(f"Not a valid module, discarding pulse: {pulse.receiver}")

        logger.debug(f"Completed button press. {self}")
        # check if we have found a cycle for each of the 4 key registers
        if len(self.cycles) == 4:
            # solution is the Least Common Multiple of when each of the 4 registers
            # hits all 1s or all HIGH values
            return lcm(*[self.cycles[x][0] for x in self.cycles])
        else:
            return 0

    def print_regs(self):
        """Used for debugging: prints the status of the registers
        &tn, &hh, &dt, &st, which are counted up and set &lv to
        high when all have all high inputs (i.e. when all flip-flops
        of these 4 modules are all set to high (or 1))."""
        for a, b, c in debug_registers:
            logger.info(f"[{self.button_presses}]")
            logger.info(
                f"\t{a}: {self.modules[a].mem.items()} {b}: {self.modules[b].mem.items()}"
            )
            binary = "".join("1" if self.modules[x].on else "0" for x in c)
            logger.info(f"\t\t{binary} = {int(binary, 2)}")


# we want to see the status of the following registers:
# lv depends on &st, &tn, &hh, &dt
# - &tn depends on &vc, which depends on
#   - %rv, %pc, %cf, %fk, %jq, %jp, %rj, %kz (8 bits - 1 byte)
# - &hh depends on &db, which depends on
#   - %gt, %zf, %vn, %kc, %qm, %hf, %xv, %cq
# &dt counts up each round, bits represent 2**n
# - &dt depends on &lz, which depends on
#   - %qh, %br, %bd, %ms, %ds, %xl, %vm, %qf, %vr, %xz, %gj (11 bits)
# &st represents 4**n
# - &st depends on &gr, which depends on
#   - %sg, %qq, %hx, %gg, %bc, %rq, %cd, %ld (8 bits - 1 byte)
debug_registers = [
    ["dt", "lz", ["vm", "bd", "ms", "qh", "br", "gj", "xl", "ds", "xz", "vr", "qf"]],
    ["st", "gr", ["rq", "gg", "cd", "bc", "qq", "hx", "ld", "sg"]],
    ["tn", "vc", ["cf", "jp", "rj", "rv", "kz", "fk", "jq", "pc"]],
    ["hh", "db", ["zf", "vn", "kc", "qm", "hf", "xv", "cq", "gt"]],
]


@aoc_timer
def part1(puzzle_input):
    """Solve part 1. Return the required output value."""
    machine = Machine(puzzle_input)
    # brute force, do not detect any cycles
    for bp in range(1000):
        machine.press_button()
    # get pulse count and multiply:
    result = machine.pulses_sent[LOW] * machine.pulses_sent[HIGH]

    return result


@aoc_timer
def part2(puzzle_input):
    """Solve part 2. Return the required output value."""
    machine = Machine(puzzle_input)
    # brute force, do not detect any cycles
    for bp in range(10_000_000):
        result = machine.press_button()
        if result > 0:
            break

    return result


if __name__ == "__main__":
    # read the puzzle input
    puzzle_input = load_input("input/20.txt")

    # Solve part 1 and print the answer
    p1 = part1(puzzle_input)
    print(f"Part 1: {p1}")

    puzzle_input = load_input("input/20.txt")

    # Solve part 2 and print the answer
    p2 = part2(puzzle_input)
    print(f"Part 2: {p2}")

# Part 1: Start: 11:47 End: 14:25 (with break)
# Part 2: Start: 14:26 End: 17:30

# Elapsed time to run part1: 0.23693 seconds.
# Part 1: 812721756
# Elapsed time to run part2: 0.92043 seconds.
# Part 2: 233338595643977
