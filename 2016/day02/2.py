def get_instructions(file='2.txt'):
    with open(file, 'r') as raw_instructions:
        instructions = raw_instructions.readlines()
        return instructions


def get_grid(part=1):

    if part == 1:
        return [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9']
        ]
    elif part == 2:
        return [
            [None, None, '1', None, None],
            [None,  '2', '3',  '4', None],
            ['5',   '6', '7',  '8',  '9'],
            [None,  'A', 'B',  'C', None],
            [None, None, 'D', None, None]
        ]


def get_code(instructions, grid, start_coords=(1, 1)):

    y = start_coords[0]
    x = start_coords[1]

    code = ''

    for instruction_set in instructions:

        for instruction in instruction_set:

            prev_y = y
            prev_x = x

            if instruction == 'U':
                y = y - 1
            elif instruction == 'D':
                y = y + 1
            elif instruction == 'L':
                x = x - 1
            elif instruction == 'R':
                x = x + 1

            try:
                if grid[y][x] is not None and y >= 0 and x >= 0:
                    pass
                else:
                    y = prev_y
                    x = prev_x
            except IndexError:
                y = prev_y
                x = prev_x

        code += grid[y][x]

    return code


def main():
    instructions = get_instructions('2.txt')
    print(get_code(instructions, get_grid(1), (1, 1)))
    print(get_code(instructions, get_grid(2), (2, 0)))


if __name__ == '__main__':
    main()
