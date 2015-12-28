# I'm describing coordinates as (column, row), the puzzle input will therefore
# need to be transposed


def get_next_value(prev_value):
    return (prev_value * 252533) % 33554393


def get_prev_coord(coords, grid):
    if coords[0] == 0:
        return (coords[1]-1, 0)
    else:
        return (coords[0]-1, coords[1]+1)


def get_next_coord(coords, grid):
    if coords[1] == 0:
        return (0, coords[0]+1)
    else:
        return (coords[0]+1, coords[1]-1)


def populate_grid(grid):
    height = len(grid)
    width = len(grid[0])

    print width
    print height

    grid[0][0] = 20151125

    current_coords = (0, 1)

    while current_coords[0] < width and current_coords[1] < height:
        prev_coord = get_prev_coord(current_coords, grid)
        prev_value = grid[prev_coord[0]][prev_coord[1]]
        grid[current_coords[0]][current_coords[1]] = get_next_value(prev_value)
        current_coords = get_next_coord(current_coords, grid)

    return grid


def part1():
    grid = [[None for i in range(0, 7000)] for i in range(0, 7000)]
    grid = populate_grid(grid)
    print grid[3018][3009]


def test():
    grid = [[None for i in range(0, 6)] for i in range(0, 6)]
    grid = populate_grid(grid)
    for c in grid:
        print c


part1()
