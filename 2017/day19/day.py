import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        lines = [line for line in file.readlines()]
        # Make sure that there are trailing whitespace to make the puzzle
        # rectangular
        puzzle_width = max([len(line) for line in lines])
        for i, line in enumerate(lines):
            pad = ''.join([' ' for i in range(0, puzzle_width - len(line))])
            lines[i] += pad
        return lines


def walk_path(path):
    position = [0, path[0].index('|')]
    direction = [1, 0]
    characters = ''
    steps = 0
    while direction is not None:
        steps += 1
        position[0] += direction[0]
        position[1] += direction[1]
        current_value = path[position[0]][position[1]]
        if current_value == ' ':
            # We fell off the path, hopefully at the end!
            direction = None
            break
        if current_value not in ('|', '-', '+'):
            # Something on the path, must be a letter!
            characters += current_value
        if current_value == '+':
            # Tuuuurn
            new_direction = None
            if direction[0] != 0:
                # We have a y-axes direction, which x-direction should we go
                if path[position[0]][position[1] - 1] != ' ':
                    new_direction = [0, -1]
                elif path[position[0]][position[1] + 1] != ' ':
                    new_direction = [0, 1]
            elif direction[1] != 0:
                # We have a x-axes direction, which y-direction should we go
                if path[position[0] - 1][position[1]] != ' ':
                    new_direction = [-1, 0]
                elif path[position[0] + 1][position[1]] != ' ':
                    new_direction = [1, 0]
            # We didn't find a direction? Must be a dead end, done!
            direction = new_direction
    return characters, steps


def test():
    test_path = get_input('test.input')
    assert ('ABCDEF', 38) == walk_path(test_path)
    logger.info('Tests passed')


def main():
    path = get_input()
    characters, steps = walk_path(path)
    logger.info('Result 1: %s' % characters)
    logger.info('Result 2: %s' % steps)


if __name__ == '__main__':
    test()
    main()
