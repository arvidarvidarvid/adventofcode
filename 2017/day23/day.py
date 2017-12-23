import math
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]


class CoProcessor():

    def __init__(self, instructions, production_mode=False):
        self.registers = {'a': int(production_mode), 'h': 0}
        self.instructions = instructions
        self.next_instruction = 0
        self.terminated = False
        self.debug_counter = 0

    def get_register_value(self, reference):
        if reference not in self.registers:
            self.registers[reference] = 0
        return self.registers[reference]

    def set_register_value(self, reference, value):
        if reference == 'h':
            print(value)
        self.registers[reference] = value

    def reference_to_integer(self, reference):
        try:
            value = int(reference)
        except ValueError:
            value = self.get_register_value(reference)
        return value

    def tick(self):

        if self.next_instruction not in range(0, len(self.instructions)):
            self.terminated = True
        if self.terminated:
            return 'Terminated'

        instruction, x, y = re.match(r'(.{3}) (.{1})\s*([a-z0-9\-]*)',
                                     self.instructions[self.next_instruction]
                                     ).groups()

        x_val = self.reference_to_integer(x)
        y_val = self.reference_to_integer(y)

        if instruction == 'set':
            self.set_register_value(x, y_val)

        elif instruction == 'sub':
            self.set_register_value(x, x_val - y_val)

        elif instruction == 'mul':
            self.debug_counter += 1
            self.set_register_value(x, x_val * y_val)

        elif instruction == 'jnz':
            if x_val != 0:
                self.next_instruction += int(y_val)
                return 'Jumping'

        self.next_instruction += 1


def run_debug(input):
    ccpu = CoProcessor(input)
    while ccpu.terminated is False:
        ccpu.tick()
    return ccpu.debug_counter


def run_prod(input):
    ccpu = CoProcessor(input, production_mode=True)
    i = 0
    while ccpu.terminated is False:
        ccpu.tick()
        i += 1
        if i % 1000 == 0:
            print(i, ccpu.registers)
    return ccpu.debug_counter


def non_primes_in_range():
    # See explanation of why this is the right thing to do in
    # python_disassembly.py, this will NOT work for any input.
    primes = 0
    non_primes = 0
    for i in range(107900, 124901)[::17]:
        prime = True
        for j in range(2, int(math.sqrt(i) + 1)):
            if i % j == 0:
                prime = False
        if prime:
            primes += 1
        else:
            non_primes += 1
    return non_primes


def test():
    test_input = get_input('test.input')
    run_prod(test_input)
    assert True is True
    logger.info('Tests passed')


def main():

    input = get_input()
    logger.info('Result 1: %s' % run_debug(input))
    logger.info('Result 2: %s' % non_primes_in_range())


if __name__ == '__main__':
    # test()
    main()

"""
FAILED GUESSES
1000 (too high)
999
800
801
94
"""
