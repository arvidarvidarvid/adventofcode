import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]


class MusicBox():

    def __init__(self, instructions, pid):

        # State
        self.pid = pid
        self.registers = {'p': pid}
        self.instructions = instructions
        self.next_instruction = 0

        # Exit conditions
        self.waiting = False
        self.terminated = False

        # Part two parameters
        self.partner_box = None
        self.received_queue = []
        self.total_sends = 0

    def receive(self, value):
        self.received_queue.append(value)

    def get_register_value(self, x):
        if x not in self.registers:
            self.registers[x] = 0
        return self.registers[x]

    def set_register_value(self, x, value):
        self.registers[x] = int(value)

    def tick(self):

        # Check if the program has already terminated or should terminate. If
        # terminated, do not process the instruction but return.
        if self.next_instruction not in range(0, len(self.instructions)):
            self.terminated = True
        if self.terminated:
            return 'Terminated'

        # Find the parts of the instruction. The function call, the one
        # mandatory parameter and the one optional.
        gs = re.match(r'(.{3}) (.{1})\s*([a-z0-9\-]*)',
                      self.instructions[self.next_instruction]).groups()

        # Put the function call name in the instruction variable
        instruction = gs[0]

        # Check if the first parameter is a numerical value or a register
        # reference. If so, look up the underlying value and store in x_val.
        x = gs[1]
        try:
            x_val = int(gs[1])
        except ValueError:
            x_val = self.get_register_value(gs[1])

        # Do the same thing for the second parameter if there is one.
        if gs[2] != '':
            try:
                y_val = int(gs[2])
            except ValueError:
                y_val = self.get_register_value(gs[2])

        if instruction == 'snd':
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
            if len(self.received_queue) > 0:
                self.set_register_value(x, self.received_queue.pop(0))
                self.waiting = False
            else:
                self.waiting = True
                return 'Waiting to receive'

        elif instruction == 'jgz':
            if x_val != 0:
                self.next_instruction += int(y_val)
                return 'Jumping'

        self.next_instruction += 1


def dueling_music_boxes(input):

    # Create two boxes and assign them both to be eachothers partners.
    b0 = MusicBox(input, pid=0)
    b1 = MusicBox(input, pid=1)
    b0.partner_box = b1
    b1.partner_box = b0

    ticks = 0

    # For each of the two programs: if waiting or terminated is True the
    # program is halted unless the other program makes a move. If both programs
    # are either waiting or terminated no program can move and therefore the
    # loop can end.
    # 11122 is a known too high value and I kill the loop to not get stuck.
    while (not (b0.waiting or b0.terminated) or
           not (b1.waiting or b1.terminated)) and b1.total_sends < 11122:
        # Each iteration ticks both programs one time, this means that the
        # program will try to process the next iteration in line.
        b0.tick()
        b1.tick()

        # Progress debug
        if ticks % 10000 == 0:
            print(ticks)
        ticks += 1

    # Limit to not run forever, 11122 is a known too high value
    if b1.total_sends == 11122:
        return 'Failed'
    else:
        return b1.total_sends


def test():
    test_input_2 = get_input('test2.input')
    assert dueling_music_boxes(test_input_2) == 3
    logger.info('Tests passed')


def main():
    input = get_input()
    logger.info('Result 2: %s' % dueling_music_boxes(input))


if __name__ == '__main__':
    test()
    main()
