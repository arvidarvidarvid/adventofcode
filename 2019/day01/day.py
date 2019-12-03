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


def mass_to_fuel(m):
    return int((float(m) / 3)) - 2


def total_mass_to_fuel(m):
    initial_fuel = mass_to_fuel(m)
    total = 0
    latest = initial_fuel
    while latest > 0:
        total += latest
        latest = mass_to_fuel(latest)
    return total


def p1(puzzle_input):
    total_fuel = 0
    for p in puzzle_input:
        total_fuel += mass_to_fuel(p)
    return total_fuel


def p2(puzzle_input):
    return sum([total_mass_to_fuel(p) for p in puzzle_input])


def test():
    test_input_p1 = get_input('test_p1.input')
    assert p1(test_input_p1) == 34241
    assert p2([100756]) == 50346
    logger.info('Tests passed')


def main():

    puzzle_input = get_input()

    logger.info('Result 1: %s' % p1(puzzle_input))
    logger.info('Result 2: %s' % p2(puzzle_input))


if __name__ == '__main__':
    test()
    main()
