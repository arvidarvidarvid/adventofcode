"""
from copy import deepcopy
from datetime import datetime, timedelta
import itertools
import math
import numpy as np
import re
import tqdm
"""
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]


def p1(box_ids):

    twos = 0
    threes = 0

    for box_id in box_ids:
        letters = {}
        for letter in box_id:
            if letter not in letters:
                letters[letter] = 1
            else:
                letters[letter] += 1
        counts = list(set([v for k, v in letters.items()]))
        twos += int(2 in counts)
        threes += int(3 in counts)

    return twos * threes


def p2(box_ids):

    success = False
    found_b1 = None
    found_b2 = None

    for b1 in box_ids:
        if success:
            break
        for b2 in box_ids:
            if success:
                break
            differences = 0
            for i in range(len(b1)):
                if b1[i] != b2[i]:
                    differences += 1
                if differences > 1:
                    break
            if differences == 1:
                success = True
                found_b1 = b1
                found_b2 = b2

    if success:
        overlap = ''
        for i in range(len(found_b1)):
            if found_b1[i] == found_b2[i]:
                overlap += found_b1[i]
        return overlap
    else:
        return -1


def test():
    test_input_p1 = get_input('test_p1.input')
    assert p1(test_input_p1) == 12
    test_input_p2 = get_input('test_p2.input')
    assert p2(test_input_p2) == 'fgij'
    logger.info('Tests passed')


def main():

    puzzle_input = get_input()

    logger.info('Result 1: %s' % p1(puzzle_input))
    logger.info('Result 2: %s' % p2(puzzle_input))


if __name__ == '__main__':
    test()
    main()
