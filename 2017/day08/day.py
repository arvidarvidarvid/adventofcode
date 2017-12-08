import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]


class Memory(object):

    def __init__(self):
        self.registers = {}
        self.global_max = 0

    def get_or_create_register(self, register):
        if register in self.registers:
            if self.registers[register] > self.global_max:
                self.global_max = self.registers[register]
            return self.registers[register]
        else:
            self.registers[register] = 0
            return self.get_or_create_register(register)

    def alter_register_value(self, register, func, delta):
        _register = self.get_or_create_register(register)
        if func == 'inc':
            value = _register + int(delta)
        elif func == 'dec':
            value = _register - int(delta)
        self.registers[register] = value
        return self.get_or_create_register(register)

    def evaluate_condition(self, register, comp, threshold):
        register_value = self.get_or_create_register(register)
        threshold = int(threshold)
        return eval('%s %s %s' % (register_value, comp, threshold))

    def largest_registry(self):
        return max([v for k, v in self.registers.items()])


def apply_instructions(memory, instructions):
    for i in instructions:
        apply_instruction(memory, i)


def apply_instruction(memory, instruction):
    reg, fun, delta, _, c_reg, c_comp, c_val = instruction.strip().split()
    if memory.evaluate_condition(c_reg, c_comp, c_val):
        memory.alter_register_value(reg, fun, delta)


def test():
    test_input = get_input('test.input')
    memory = Memory()
    apply_instructions(memory, test_input)
    assert memory.largest_registry() == 1
    logger.info('Tests passed')


def main():

    input = get_input()
    memory = Memory()
    apply_instructions(memory, input)

    logger.info('Result 1: %s' % memory.largest_registry())
    logger.info('Result 2: %s' % memory.global_max)


if __name__ == '__main__':
    test()
    main()
