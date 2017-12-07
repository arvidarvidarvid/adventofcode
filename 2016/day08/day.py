from copy import deepcopy
import logging
import numpy as np
import re

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
    return grid


def apply(grid, instruction):

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

    prev_state = deepcopy(grid)

    if dim == 'row':
        for index, value in enumerate(grid[pos]):
            new_index = (index + dist) % len(grid[pos])
            grid[pos][new_index] = prev_state[pos][index]
    elif dim == 'column':
        grid = rotate(grid.transpose(), 'row', pos, dist)
        grid = grid.transpose()

    return grid


def rect(grid, y, x):
    for row in range(0, y):
        for col in range(0, x):
            grid[row][col] = 1
    return grid


def count_lit(grid):
    lit = 0
    for row in grid:
        for col in row:
            lit += col
    return int(lit)


def draw_code(grid):
    for row in grid:
        print(''.join([str(int(r)) for r in row]).replace(
            '0', ' ').replace('1', '#'))


def test():
    raw_instructions = """rect 3x2
    rotate column x=1 by 1
    rotate row y=0 by 4
    rotate column x=1 by 1"""
    instructions = split_instructions(raw_instructions)
    grid = get_grid(3, 7)
    grid = apply_instructions(grid, instructions)
    assert count_lit(grid) == 6
    logger.info('Tests passed')


def main():

    input = get_input()

    grid = get_grid(6, 50)
    instructions = split_instructions(input)
    grid = apply_instructions(grid, instructions)
    logger.info('Result 1: %s' % count_lit(grid))
    logger.info('Result 2')
    draw_code(grid)


if __name__ == '__main__':
    test()
    main()
