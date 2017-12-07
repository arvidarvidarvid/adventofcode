from copy import deepcopy
from datetime import datetime, timedelta
import itertools
import logging
import math
import numpy as np
import re
import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input():
    with open('day.input', 'r') as file:
        return file.read()


def split_instructions(raw):
    return [i.strip() for i in raw.split('\n')]


def get_grid(y, x):
    return np.zeros((y, x))


def apply_instructions(grid, instructions):
    for instruction in instructions:
        grid = apply(grid, instruction)
        print(grid)
    return grid


def apply(grid, instruction):

    print(instruction)

    rect_pattern = r'rect (\d+)x(\d+)'
    rotate_pattern = r'rotate (.+) [xy]=(\d+) by (\d+)'

    rect_m = re.match(rect_pattern, instruction)
    rot_m = re.match(rotate_pattern, instruction)

    if rect_m is not None:
        return rect(grid, y=int(rect_m[2]), x=int(rect_m[1]))
    elif rot_m is not None:
        return rotate(grid, dim=rot_m[1], pos=int(rot_m[2]),
                      dist=int(rot_m[3]))


def rotate(grid, dim, pos, dist):

    if dim == 'row':
        prev_state = deepcopy(grid[pos])
        for index, value in grid[pos]:
            new_index = index +

    elif dim == 'column':
        pass


def rect(grid, y, x):
    for row in range(0, y):
        for col in range(0, x):
            grid[row][col] = 1
    return grid


def test():
    raw_instructions = """rect 3x2
    rotate column x=1 by 1
    rotate row y=0 by 4
    rotate column x=1 by 1"""
    instructions = split_instructions(raw_instructions)
    grid = get_grid(3, 7)
    print(grid)
    apply_instructions(grid, [instructions[0]])
    logger.info('Tests passed')


def main():

    input = get_input()

    logger.info('Result 1')
    logger.info('Result 2')


if __name__ == '__main__':
    test()
    main()
