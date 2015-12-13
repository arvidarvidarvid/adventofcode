import re

with open('6.txt', 'r') as f:
    instructions = f.read()


def apply_instruction(inst, grid):
    m = re.match(r'(?P<action>[a-z ]*)(?P<c1>[\d,]+)[a-z ]*(?P<c2>[\d,]+)',
                 inst)
    action = m.group('action').strip()
    coord1 = m.group('c1').split(',')
    coord2 = m.group('c2').split(',')

    for row in range(int(coord1[1]), int(coord2[1])+1):
        for col in range(int(coord1[0]), int(coord2[0])+1):
            if action == 'toggle':
                grid[col][row] = grid[col][row] + 2
            elif action == 'turn on':
                grid[col][row] = grid[col][row] + 1
            elif action == 'turn off':
                if grid[col][row] > 0:
                    grid[col][row] = grid[col][row] - 1


def active_lights(grid):
    total = 0
    for row in grid:
        total = total + sum(row)
    return total


grid = [[0 for i in range(0, 1000)] for j in range(0, 1000)]

for inst in instructions.split('\n'):
    apply_instruction(inst, grid)

print active_lights(grid)
