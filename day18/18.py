def get_grid(filename):
    initial_state = [l for l in open(filename, 'r').read().split('\n')]
    grid = []
    for l in initial_state:
        line = []
        for c in l:
            line.append(c)
        grid.append(line)
    return grid


def get_next_state_for_point(grid, y, x, part2=False):

    if part2:
        if (y, x) in [
                (0, 0),
                (0, len(grid[0])-1),
                (len(grid)-1, 0),
                (len(grid)-1, len(grid[0])-1)
                ]:
            return '#'

    neighbours = []

    if x > 0:
        neighbours.append(grid[y][x-1])
    if x < len(grid[0])-1:
        neighbours.append(grid[y][x+1])

    if y > 0:  # Prev line if not first line
        if x > 0:  # Not first item in line
            neighbours.append(grid[y-1][x-1])
        neighbours.append(grid[y-1][x])
        if x < len(grid[0])-1:
            neighbours.append(grid[y-1][x+1])

    if y < len(grid)-1:  # Next line if not last line
        if x > 0:  # Not first item in line
            neighbours.append(grid[y+1][x-1])
        neighbours.append(grid[y+1][x])
        if x < len(grid[0])-1:  #
            neighbours.append(grid[y+1][x+1])

    lit_neighbours = neighbours.count('#')
    if grid[y][x] == '#':
        if lit_neighbours in (2, 3):
            return '#'
        else:
            return '.'
    elif grid[y][x] == '.':
        if lit_neighbours == 3:
            return '#'
        else:
            return '.'
    else:
        raise Exception('What?')


def get_next_grid(grid, part2=False):
    new_grid = [['.' for c in l] for l in grid]
    for y in range(len(new_grid)):
        for x in range(len(l)):
            new_grid[y][x] = get_next_state_for_point(grid, y, x, part2)
    return new_grid


def print_grid(grid):
    for l in grid:
        print ''.join(l)
    print '\n'


def get_nth_grid(grid, n, part2=False):
    for i in range(n):
        grid = get_next_grid(grid, part2)
    return grid


def count_lights(grid):
    count = 0
    for l in grid:
        for c in l:
            if c == '#':
                count += 1
    return count


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
