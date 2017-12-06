from copy import deepcopy
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input():
    with open('day.input', 'r') as file:
        return [line.split() for line in file.readlines()]


def validate_triangle(sides):
    sides = list(map(int, sides))
    sides.sort()
    return sides[2] < sides[0] + sides[1]


def valid_triangles(lengths):
    return sum([1 for t in lengths if validate_triangle(t)])


def row_set_to_column_based_set(input):
    row_count = 0
    partial_rows = [[None, None, None],
                    [None, None, None],
                    [None, None, None]]
    complete_rows = []
    for i in input:
        partial_rows[0][row_count] = int(i[0])
        partial_rows[1][row_count] = int(i[1])
        partial_rows[2][row_count] = int(i[2])
        row_count += 1
        if row_count == 3:
            complete_rows += deepcopy(partial_rows)
            row_count = 0
    return complete_rows


def main():

    input = get_input()
    input_2 = row_set_to_column_based_set(input)

    logger.info('Result 1: %s' % valid_triangles(input))
    logger.info('Result 2: %s' % valid_triangles(input_2))


if __name__ == '__main__':

    main()
