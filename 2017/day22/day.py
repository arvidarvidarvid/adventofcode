import numpy as np
import logging
import unittest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return file.read()


def get_grid(input, bursts):
    input = input.replace('#', '1').replace('.', '0')
    input_grid = np.array([[float(c) for c in line]
                           for line in input.split('\n')])

    # Need to build as small a grid as possible, assuming width=bursts will
    # run out of memory in part 2 for me.
    #
    # Did some investigations with lower burst sizes to see how much of the
    # grid is actually used and a good rule of thumb seems to be that the
    # virus will make us of a grid 15% as wide as the numbers of steps it will
    # take - assuming starting in the middle.
    target_width = int(bursts * 0.15)
    if target_width % 2 == 0:
        target_width += 1

    # Building a full size grid of zeros and then projecting the input onto the
    # center of that larger grid.
    grid = np.zeros((target_width, target_width))
    start_position = [int(target_width / 2 - len(input_grid) / 2),
                      int(target_width / 2 - len(input_grid) / 2)]

    for l, line in enumerate(input_grid):
        for c, char in enumerate(line):
            grid[start_position[0] + l][start_position[1] + c] = char

    return grid


def infections_in_bursts(input, bursts, part_a=True):

    directions = {
        'n': {'left': 'w', 'right': 'e', 'reverse': 's', 'move': [-1, 0]},
        'e': {'left': 'n', 'right': 's', 'reverse': 'w', 'move': [0, 1]},
        's': {'left': 'e', 'right': 'w', 'reverse': 'n', 'move': [1, 0]},
        'w': {'left': 's', 'right': 'n', 'reverse': 'e', 'move': [0, -1]}
    }

    grid = get_grid(input, bursts)
    pos = [int(len(grid) / 2), int(len(grid) / 2)]
    infections = 0
    direction = 'n'

    for b in range(bursts):

        # Using numbers to represent the states instead of characters since it
        # is far faster and cheaper to initiate and modify zero-arrays with
        # numpy than empty lists of lists.

        # 1 == infected
        if grid[pos[0]][pos[1]] == 1:
            direction = directions[direction]['right']
            if part_a:
                grid[pos[0]][pos[1]] = 0
            else:
                grid[pos[0]][pos[1]] = 0.5

        # 0 == clean
        elif grid[pos[0]][pos[1]] == 0:
            direction = directions[direction]['left']
            if part_a:
                grid[pos[0]][pos[1]] = 1
                infections += 1
            else:
                grid[pos[0]][pos[1]] = 0.25

        # 0.25 == weakened
        elif grid[pos[0]][pos[1]] == 0.25:
            direction = direction
            grid[pos[0]][pos[1]] = 1
            infections += 1

        # 0.5 == flagged
        elif grid[pos[0]][pos[1]] == 0.5:
            direction = directions[direction]['reverse']
            grid[pos[0]][pos[1]] = 0

        pos = list(map(sum, zip(directions[direction]['move'], pos)))

    return infections


class TestsOfTheDay(unittest.TestCase):

    def setUp(self):
        self.input = get_input('test.input')

    def test_part_a_70_bursts(self):
        self.assertEqual(infections_in_bursts(self.input, 70), 41)

    def test_part_a_10000_bursts(self):
        self.assertEqual(infections_in_bursts(self.input, 10000), 5587)

    def test_part_b_100_bursts(self):
        self.assertEqual(infections_in_bursts(self.input, 100, part_a=False),
                         26)

    def test_part_b_10000000_bursts(self):
        self.assertEqual(
            infections_in_bursts(self.input, 10000000, part_a=False), 2511944)


def main():
    input = get_input()
    logger.info('Result 1: %s' % infections_in_bursts(input, 10000))
    logger.info('Result 2: %s' % infections_in_bursts(input, 10000000, False))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestsOfTheDay)
    unittest.TextTestRunner(verbosity=2).run(suite)
    main()
