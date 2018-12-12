import numpy as np
from tqdm import tqdm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_grid(width, height):
    grid = [[None for i in range(width)] for y in range(height)]
    return np.array(grid)


def power_level(x, y, grid_serial_number):
    rack_id = x + 10
    power = rack_id * y
    power = power + grid_serial_number
    power = power * rack_id
    power = int(power)
    if len(str(power)) > 2:
        power = int(str(power)[-3])
    else:
        power = 0
    return power - 5


def popoulate_grid(grid, grid_serial_number):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            grid[y][x] = power_level(x+1, y+1, grid_serial_number)
    return grid


def draw_grid(grid):
    for row in grid:
        print(' '.join(list(map(str, row))))


def draw_section(grid, x, y, width, height):
    for row in grid[y:y+height]:
        print(row[x:x+width])


def find_highest_power(grid, side):

    search_height = len(grid) - (side-1)
    search_width = len(grid[0]) - (side-1)

    highest_power_seen = -1e6
    highest_power_x = None
    highest_power_y = None

    for y in range(search_height):
        for x in range(search_width):
            power = grid[y:y+side, x:x+side].sum()
            if power > highest_power_seen:
                highest_power_seen = power
                highest_power_x = x
                highest_power_y = y

    return (highest_power_x+1, highest_power_y+1), highest_power_seen


def p1(grid_serial_number, width=300, height=300):
    grid = get_grid(width, height)
    grid = popoulate_grid(grid, grid_serial_number)
    coords, power = find_highest_power(grid, 3)
    return coords


def p2(grid_serial_number, width=300, height=300):
    grid = get_grid(width, height)
    grid = popoulate_grid(grid, grid_serial_number)

    highest_power_seen = -1e6
    highest_power_coords = None
    highest_power_grid_size = None

    for grid_size in tqdm(range(1, 301)):
        coords, power = find_highest_power(grid, grid_size)
        if power > highest_power_seen:
            highest_power_seen = power
            highest_power_coords = coords
            highest_power_grid_size = grid_size

    return highest_power_coords, highest_power_grid_size


def test():
    assert power_level(3,5,8) == 4
    assert power_level(122,79,57) == -5
    assert power_level(217,196,39) == 0
    assert power_level(101,153,71) == 4
    assert p1(18) == (33, 45)
    logger.info('Tests passed')


def main():

    puzzle_input = 9424
    print(p1(puzzle_input))
    print(p2(puzzle_input))


if __name__ == '__main__':
    test()
    main()
