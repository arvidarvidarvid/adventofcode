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


def p1(puzzle_input):
    return None


def p2(puzzle_input):
    return None


def test():
    test_input_p1 = get_input('test_p1.input')
    test_input_p2 = get_input('test_p2.input')
    assert p1(test_input_p1) == None
    assert p2(test_input_p2) == None
    logger.info('Tests passed')


def main():

    puzzle_input = get_input()

    logger.info('Result 1: %s' % p1(puzzle_input))
    logger.info('Result 2: %s' % p2(puzzle_input))


if __name__ == '__main__':
    test()
    main()
