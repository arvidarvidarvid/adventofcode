import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]


class MusicBox():

    def __init__(self, instructions, pid):
        self.pid = pid
        self.registers = {'p': pid}
        self.instructions = instructions
        self.next_instruction = 0
        self.latest_sound = None
        self.recieved_queue = []
        self.partner_box = None
        self.waiting = False
        self.terminated = False
        self.part_1_return = None
        self.total_sends = 0

    def set_partner_box(self, box):
        self.partner_box = box

    def recieve(self, value):
        self.recieved_queue.append(value)

    def send(self, value):
        # print(self.pid, 'sending', value)
        self.partner_box.recieve(value)
        self.total_sends += 1

    def register_value(self, x, value=None):
        if value is None:
            if x in self.registers:
                return self.registers[x]
            else:
                self.registers[x] = 0
                return self.register_value(x)
        else:
            self.register_value(x)
            self.registers[x] = int(value)
            return self.register_value(x)

    def run_instructions(self):
        total = 0
        while self.part_1_return is None and total < 10000000:
            self.tick()
            total += 1
        return self.part_1_return

    def tick(self):

        if self.next_instruction not in range(0, len(self.instructions)):
            print('terminating')
            self.terminated = True
            return False

        gs = re.match(r'(.{3}) (.{1})\s*([a-z0-9\-]*)',
                      self.instructions[self.next_instruction]).groups()

        instruction = gs[0]

        x = gs[1]
        try:
            x_val = int(gs[1])
        except ValueError:
            x_val = self.register_value(gs[1])

        if gs[2] != '':
            try:
                y_val = int(gs[2])
            except ValueError:
                y_val = self.register_value(gs[2])

        if instruction == 'snd':
            if self.partner_box is None:
                self.latest_sound = x_val
            else:
                self.send(x_val)

        elif instruction == 'set':
            self.register_value(x, y_val)

        elif instruction == 'add':
            self.register_value(x, x_val + y_val)

        elif instruction == 'mul':
            self.register_value(x, x_val * y_val)

        elif instruction == 'mod':
            self.register_value(x, x_val % y_val)

        elif instruction == 'rcv':
            if self.partner_box is None:
                if x_val != 0:
                    self.part_1_return = self.latest_sound
            else:
                if len(self.recieved_queue) > 0:
                    self.register_value(x, self.recieved_queue.pop(0))
                    self.waiting = False
                else:
                    self.waiting = True
                    return 'Waiting to recieve'

        elif instruction == 'jgz':
            if x_val != 0:
                self.next_instruction += int(y_val)
                return 'Jumping'

        self.next_instruction += 1


def dueling_music_boxes(input):
    b0 = MusicBox(input, pid=0)
    b1 = MusicBox(input, pid=1)
    b0.set_partner_box(b1)
    b1.set_partner_box(b0)

    while (not (b0.waiting or b0.terminated) or
           not (b1.waiting or b1.terminated)) and b1.total_sends < 11122:
        b0.tick()
        b1.tick()

    print(b0.total_sends, len(b0.recieved_queue))
    print(b1.total_sends, len(b1.recieved_queue))

    if b1.total_sends == 11122:
        return 'Failed'
    else:
        return b1.total_sends


def test():
    test_input_1 = get_input('test.input')
    test_input_2 = get_input('test2.input')
    mb = MusicBox(test_input_1, pid=0)
    assert mb.run_instructions() == 4
    assert dueling_music_boxes(test_input_2) == 3
    logger.info('Tests passed')


def main():

    input = get_input()
    mb = MusicBox(input, pid=0)
    logger.info('Result 1: %s' % mb.run_instructions())
    logger.info('Result 2: %s' % dueling_music_boxes(input))


if __name__ == '__main__':
    test()
    main()
