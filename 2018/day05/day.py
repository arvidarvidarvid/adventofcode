"""
from datetime import datetime, timedelta
import itertools
import math
import numpy as np
import tqdm
"""
from copy import deepcopy
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()][0]


def get_reactive_pairs():

    ascii_upper = [chr(i) for i in range(65, 91)]
    ascii_lower = [chr(i) for i in range(97, 123)]

    tuple_pairs = []
    tuple_pairs += list(zip(ascii_upper, ascii_lower))
    tuple_pairs += list(zip(ascii_lower, ascii_upper))

    reactive = []

    for pair in tuple_pairs:
        reactive.append('{}{}'.format(pair[0], pair[1]))

    return reactive


def get_length_of_reduced(to_reduce):

    reactive = get_reactive_pairs()

    reactant_present = True
    start_search_index = 0

    while reactant_present:
        reactant_present = False
        for i in range(start_search_index, len(to_reduce)):
            if i < len(to_reduce) - 1:
                if to_reduce[i] + to_reduce[i+1] in reactive:
                    to_reduce = to_reduce[:i] + to_reduce[i+2:]
                    reactant_present = True
                    start_search_index = max(0, i-2)
                    break

    return len(to_reduce)


def p1(puzzle_input):
    return get_length_of_reduced(puzzle_input)


def p2(puzzle_input):

    reactive = get_reactive_pairs()

    shortest_seen = 1e6

    for strip_char in reactive:
        stripped_input = deepcopy(puzzle_input).replace(
            strip_char[0], '').replace(strip_char[1], '')
        _length = get_length_of_reduced(stripped_input)
        if _length < shortest_seen:
            shortest_seen = _length

    return shortest_seen


def test():
    test_input_p1 = get_input('test_p1.input')
    assert p1(test_input_p1) == 10
    assert p2(test_input_p1) == 4
    logger.info('Tests passed')


def main():

    puzzle_input = get_input()

    logger.info('Result 1: %s' % p1(puzzle_input))
    logger.info('Result 2: %s' % p2(puzzle_input))


if __name__ == '__main__':
    test()
    main()
