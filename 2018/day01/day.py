"""
from copy import deepcopy
from datetime import datetime, timedelta
import itertools
import math
import re
import tqdm
import numpy as np
"""
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]


def test():
    assert p2([+1, -1]) == 0
    assert p2([+3, +3, +4, -2, -4]) == 10
    assert p2([-6, +3, +8, +5, -6]) == 5
    assert p2([+7, +7, -2, -7, -4]) == 14
    logger.info('Tests passed')


def p1(puzzle_input):
    p1_val = 0
    for op in puzzle_input:
        p1_val += int(op)
    return(p1_val)


def p2(puzzle_input):
    val = 0
    seen = set([0])
    freqs = 0
    while True:
        for op in puzzle_input:
            freqs += 1
            val += int(op)
            if val in seen:
                return val
            else:
                seen.add(val)


def main():

    puzzle_input = get_input()
    logger.info('Result 1: %s' % p1(puzzle_input))
    logger.info('Result 2: %s' % p2(puzzle_input))


if __name__ == '__main__':
    test()
    main()
