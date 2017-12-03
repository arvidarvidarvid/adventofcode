import logging
import math
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input():
    with open('day.input', 'r') as file:
        return file.read()


class MemorySpiral(object):

    def __init__(self, max_value, adjacent_values=False, break_for_value=None):
        self.max_value = max_value
        self.adjacent_values = adjacent_values
        self.break_for_value = break_for_value
        self.next_after_break_value = None
        self.grid = None
        self.side = None
        self.center = None

        self.initialise_grid()
        self.build_grid()

    def initialise_grid(self):
        # All grids are square, all sides have odd length, the grid is padded
        # with a layer of zeroes to not get IndexErrors from doing the adjacent
        # sums.
        self.side = math.ceil(math.sqrt(self.max_value)) + 2
        if self.side % 2 == 0:
            self.side += 1
        self.grid = np.zeros((self.side, self.side))
        self.center = (math.floor(self.side / 2), math.floor(self.side / 2))
        self.grid[self.center[0]][self.center[1]] = 1

    def build_grid(self):

        val = 2  # Starting value for the second layer

        for layer in range(1, math.ceil((self.side - 2) / 2)):
            pos = [self.center[0] + layer - 1, self.center[1] + layer]
            values_in_layer = layer * 8
            layer_start_val = val
            for _ in range(0, values_in_layer):
                if self.adjacent_values:
                    adjacent_sum = self.get_adjacent_sum(pos)
                    self.grid[pos[0]][pos[1]] = adjacent_sum
                    if self.break_for_value is not None:
                        if adjacent_sum > self.break_for_value:
                            self.next_after_break_value = adjacent_sum
                            return self.grid
                else:
                    self.grid[pos[0]][pos[1]] = val

                if val < layer_start_val + 2 * layer - 1:  # Right side
                    pos[0] -= 1
                elif val < layer_start_val + 4 * layer - 1:  # Top
                    pos[1] -= 1
                elif val < layer_start_val + 6 * layer - 1:  # Lef side
                    pos[0] += 1
                elif val < layer_start_val + 8 * layer - 1:  # Bottom
                    pos[1] += 1

                val += 1

        return self.grid

    def get_adjacent_sum(self, pos):
        return sum([
            sum(self.grid[pos[0] - 1][pos[1] - 1:pos[1] + 2]),
            self.grid[pos[0] + 0][pos[1] - 1],
            self.grid[pos[0] + 0][pos[1] + 1],
            sum(self.grid[pos[0] + 1][pos[1] - 1:pos[1] + 2])
        ])

    def get_coords_for_value_in_grid(self, val):
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if col == val:
                    return [y, x]

    def shortest_path(self, val):
        coords = self.get_coords_for_value_in_grid(val)
        center = self.center
        y_steps = max([coords[0], center[0]]) - min([coords[0], center[0]])
        x_steps = max([coords[1], center[1]]) - min([coords[1], center[1]])
        return y_steps + x_steps


def test():

    # Part 1
    spiral = MemorySpiral(1024)
    assert spiral.shortest_path(1) == 0
    assert spiral.shortest_path(12) == 3
    assert spiral.shortest_path(23) == 2
    assert spiral.shortest_path(1024) == 31

    # Part 2
    adjacent_spiral = MemorySpiral(1024,
                                   adjacent_values=True,
                                   break_for_value=362)
    assert adjacent_spiral.next_after_break_value == 747

    print('Tests pass')


def main():

    test()

    input_value = int(get_input())
    spiral = MemorySpiral(input_value)

    adjacent_spiral = MemorySpiral(input_value,
                                   adjacent_values=True,
                                   break_for_value=input_value)

    logger.info('Result 1: %s' % spiral.shortest_path(input_value))
    logger.info('Result 2: %s' % adjacent_spiral.next_after_break_value)


if __name__ == '__main__':

    main()
