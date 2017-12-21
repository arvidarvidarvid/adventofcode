import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


KNOWN_VARIATIONS = {}


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]


def get_start_grid():
    return """.#.
..#
###"""


def input_to_replacements(input):
    replacements = {}
    for i in input:
        _from, _to = i.split(' => ')
        _from = matrix_to_tuple(grid_to_matrix(_from.replace('/', '\n')))
        _to = grid_to_matrix(_to.replace('/', '\n'))
        replacements[_from] = _to
    return replacements


def grid_to_matrix(grid):
    # Build a 2d numpy array from the string version of the grid to be able to
    # easily perform transformations such as rotate and flip.
    grid = grid.split('\n')
    matrix = np.zeros((len(grid), len(grid)))
    for l, line in enumerate(grid):
        for c, char in enumerate(line):
            if char == '#':
                matrix[l][c] = 1
    return matrix


def matrix_to_tuple(grid):
    # To be able to use arrays as keys in the replacement dictionary we need to
    # be able to cast them to nested tuples since the dict type wants immutable
    # hashable types as keys.
    return tuple(tuple(line) for line in grid)


def matrix_to_string(grid):
    return ''.join([''.join([str(int(char)) for char in line] + ['\n'])
                    for line in grid]).replace('0', '.').replace('1', '#')


def replace_matrix(matrix, replacements):

    # Generate the tuple version of this matrix to first be able to look up if
    # the possible rotate/flip variations are already memorised since before.
    # If not: generate the possible variations, cast them to tuples and check
    # which exists as a key in the replacements dict.

    global KNOWN_VARIATIONS
    matrix_as_tuple = matrix_to_tuple(matrix)

    if matrix_as_tuple in KNOWN_VARIATIONS:
        variations = KNOWN_VARIATIONS[matrix_to_tuple(matrix)]
    else:
        variations = [matrix, np.flipud(matrix), np.fliplr(matrix),
                      np.rot90(matrix, 1), np.rot90(matrix, 3),
                      np.rot90(np.flipud(matrix), 1),
                      np.rot90(np.flipud(matrix), 3),
                      np.rot90(np.fliplr(matrix), 1),
                      np.rot90(np.fliplr(matrix), 3)]
        variations = tuple(matrix_to_tuple(v) for v in variations)
        KNOWN_VARIATIONS[matrix_as_tuple] = variations

    for variation in variations:
        if variation in replacements:
            return replacements[variation]

    raise(Exception('Could not find a valid replacement'))


def write_submatrix_to_matrix(submatrix, matrix, start_position):
    # Take the incoming submatrix and the assumed blank matrix and write the
    # values from the submatrix into the matrix at the position start_position.
    for l, line in enumerate(submatrix):
        for c, char in enumerate(line):
            matrix[start_position[0] + l][start_position[1] + c] = char
    return matrix


def enhance(input, grid, iterations=1):
    replacements = input_to_replacements(input)
    matrix = grid_to_matrix(grid)

    for i in range(iterations):

        # Determine if we should split the existing matrix in 2x2 or 3x3
        # sections.
        if len(matrix) % 2 == 0:
            split_length = 2
            new_width = int((len(matrix) / 2) * 3)
        else:
            split_length = 3
            new_width = int((len(matrix) / 3) * 4)

        # Create a new matrix with the expected dimensions based on how many
        # new columns and rows we expect compared to the previous one.
        next_matrix = np.zeros((new_width, new_width))

        # Walk through the matrix x lines at the time according to if we are
        # operating with a "split in 3x3" or "split by 2x2" recorded in
        # split_length.
        for line_set in range(int(len(matrix) / split_length)):
            _line_set = matrix[line_set * split_length:
                               (line_set + 1) * split_length]

            # Within the line-set, pick x columns at a time, this is now giving
            # us a 3x3 or 2x2 sub-matrix.
            for column_set in range(int(len(matrix) / split_length)):
                _m = np.array([
                    line[column_set * split_length:
                         (column_set + 1) * split_length]
                    for line in _line_set])

                # Resolve the sub-matrix to the expected replacement according
                # to the puzzle input.
                replacement = replace_matrix(_m, replacements)

                # Write the replacement matrix into the blank new matrix at the
                # new position.
                next_matrix = write_submatrix_to_matrix(
                    replacement,
                    next_matrix,
                    (line_set * (split_length + 1),
                     column_set * (split_length + 1)))

        matrix = next_matrix

    return matrix_to_string(matrix)


def sum_turned_on(grid):
    return int(sum(sum(grid_to_matrix(grid))))


def test():
    test_input = get_input('test.input')
    grid = get_start_grid()
    assert sum_turned_on(enhance(test_input, grid, 2)) == 12
    logger.info('Tests passed')


def main():
    input = get_input()
    grid_1 = enhance(input, get_start_grid(), 5)
    logger.info('Result 1: %s' % sum_turned_on(grid_1))
    grid_2 = enhance(input, get_start_grid(), 18)
    logger.info('Result 2: %s' % sum_turned_on(grid_2))


if __name__ == '__main__':
    test()
    main()
