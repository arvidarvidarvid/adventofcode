import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]


class MusicBox():

    def __init__(self, instructions, pid, part):

        self.part = part
        self.pid = pid
        self.registers = {'p': pid}
        self.instructions = instructions
        self.next_instruction = 0

        self.waiting = False
        self.terminated = False

        self.latest_sound = None
        self.recovered_frequency = None

        self.partner_box = None
        self.received_queue = []
        self.total_sends = 0

    def get_register_value(self, reference):
        if reference not in self.registers:
            self.registers[reference] = 0
        return self.registers[reference]

    def set_register_value(self, reference, value):
        self.registers[reference] = value

    def receive(self, value):
        self.received_queue.append(value)

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

        if instruction == 'snd':
            if self.part == 1:
                self.latest_sound = x_val
            else:
                self.partner_box.receive(x_val)
                self.total_sends += 1

        elif instruction == 'set':
            self.set_register_value(x, y_val)

        elif instruction == 'add':
            self.set_register_value(x, x_val + y_val)

        elif instruction == 'mul':
            self.set_register_value(x, x_val * y_val)

        elif instruction == 'mod':
            self.set_register_value(x, x_val % y_val)

        elif instruction == 'rcv':
            if self.part == 1:
                if x_val != 0:
                    self.recovered_frequency = self.latest_sound
            else:
                if len(self.received_queue) > 0:
                    value = self.received_queue.pop(0)
                    self.set_register_value(x, value)
                    self.waiting = False
                else:
                    self.waiting = True
                    return 'Waiting to receive'

        elif instruction == 'jgz':
            if x_val > 0:
                self.next_instruction += int(y_val)
                return 'Jumping'

        self.next_instruction += 1


def recover_frequency(box):
    while box.recovered_frequency is None:
        box.tick()
    return box.recovered_frequency


def sends_before_deadlock(input):
    b0 = MusicBox(input, pid=0, part=2)
    b1 = MusicBox(input, pid=1, part=2)
    b0.partner_box = b1
    b1.partner_box = b0

    while not ((b0.waiting or b0.terminated) and
               (b1.waiting or b1.terminated)):
        b0.tick()
        b1.tick()

    return b1.total_sends


def test():
    test_input_1 = get_input('test.input')
    test_input_2 = get_input('test2.input')
    mb = MusicBox(test_input_1, pid=0, part=1)
    assert recover_frequency(mb) == 4
    assert sends_before_deadlock(test_input_2) == 3
    logger.info('Tests passed')


def main():
    input = get_input()
    mb = MusicBox(input, pid=0, part=1)
    logger.info('Result 1: %s' % recover_frequency(mb))
    logger.info('Result 2: %s' % sends_before_deadlock(input))


if __name__ == '__main__':
    test()
    main()
