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


def test():
    test_input = get_input('test.input')
    assert True is True
    logger.info('Tests passed')


def main():

    input = get_input()

    logger.info('Result 1')
    logger.info('Result 2')


if __name__ == '__main__':
    test()
    main()
