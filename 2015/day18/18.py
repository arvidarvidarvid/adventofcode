def get_grid(fn):
    return [[c for c in l] for l in open(fn, 'r').read().split('\n')]


def get_next_state_for_point(grid, y, x, part2=False):

    if part2:
        y_max, x_max = len(grid[0])-1, len(grid)-1
        if (y, x) in [(0, 0), (0, x_max), (y_max, 0), (y_max, x_max)]:
            return '#'

    neighbours = []

    if x > 0: neighbours.append(grid[y][x-1])
    if x < len(grid[0])-1: neighbours.append(grid[y][x+1])

    if y > 0:
        if x > 0: neighbours.append(grid[y-1][x-1])
        if x < len(grid[0])-1: neighbours.append(grid[y-1][x+1])
        neighbours.append(grid[y-1][x])

    if y < len(grid)-1:
        if x > 0: neighbours.append(grid[y+1][x-1])
        if x < len(grid[0])-1: neighbours.append(grid[y+1][x+1])
        neighbours.append(grid[y+1][x])

    lit_neighbours = neighbours.count('#')
    if lit_neighbours == 3: return '#'
    elif lit_neighbours == 2 and grid[y][x] == '#': return '#'
    else: return '.'


def get_next_grid(grid, part2=False):
    new_grid = [['X' for c in l] for l in grid]
    for y in range(len(new_grid)):
        for x in range(len(l)):
            new_grid[y][x] = get_next_state_for_point(grid, y, x, part2)
    return new_grid


def print_grid(grid):
    for l in grid: print ''.join(l)
    print '\n'


def get_nth_grid(grid, n, part2=False):
    for i in range(n): grid = get_next_grid(grid, part2)
    return grid


def count_lights(grid):
    flat = ''.join(sum(grid, []))
    return flat.count('#')


def break_lights(grid):
    grid[0][0] = '#'
    grid[0][len(grid[0])-1] = '#'
    grid[len(grid)-1][0] = '#'
    grid[len(grid)-1][len(grid[0])-1] = '#'
    return grid


def main():
    grid = get_grid('18.txt')
    hundreth_grid = get_nth_grid(grid, 100, part2=False)
    print ('Part 1: There are %s lights turned on after 100 iterations' %
           count_lights(hundreth_grid))

    grid = get_grid('18.txt')
    grid = break_lights(grid)
    hundreth_grid = get_nth_grid(grid, 100, part2=True)
    print ('Part 2: There are %s lights turned on with broken corners' %
           count_lights(hundreth_grid))


if __name__ == "__main__":
    main()
