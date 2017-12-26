from tqdm import tqdm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]


class TuringMachine(object):

    def __init__(self, start_state, states):
        self.state = 'A'
        self.states = states
        self.state_dict = {}
        self.tape = [0 for i in range(0, 13000000)]
        self.cursor = 500000
        for state in states:
            self.state_dict[state[0]] = {
                0: {
                    'write': state[1],
                    'move': state[2],
                    'next': state[3]
                }, 1: {
                    'write': state[4],
                    'move': state[5],
                    'next': state[6]
                }
            }

    def tick(self):
        current_value = self.tape[self.cursor]
        value = self.state_dict[self.state][current_value]['write']
        next = self.state_dict[self.state][current_value]['next']
        next_cursor = (self.cursor -
                       self.state_dict[self.state][current_value]['move'])
        self.tape[self.cursor] = value
        self.cursor = next_cursor
        self.state = next

    def run_ticks(self, ticks):
        for i in tqdm(range(ticks)):
            self.tick()

    def checksum(self):
        return sum(self.tape)


def test():
    states = [
        ['A', 1, 1, 'B', 0, -1, 'B'],
        ['B', 1, -1, 'A', 1, 1, 'A'],
    ]
    machine = TuringMachine('A', states)
    machine.run_ticks(6)
    assert machine.checksum() == 3
    logger.info('Tests passed')


def main():

    states = [
        ['A', 1,  1, 'B', 0, -1, 'B'],
        ['B', 1, -1, 'C', 0,  1, 'E'],
        ['C', 1,  1, 'E', 0, -1, 'D'],
        ['D', 1, -1, 'A', 1, -1, 'A'],
        ['E', 0,  1, 'A', 0,  1, 'F'],
        ['F', 1,  1, 'E', 1,  1, 'A']
    ]

    machine = TuringMachine('A', states)
    machine.run_ticks(12861455)

    logger.info('Result: %s' % machine.checksum())


if __name__ == '__main__':
    test()
    main()
