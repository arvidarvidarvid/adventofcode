from copy import deepcopy
from datetime import datetime, timedelta
import itertools
import logging
import math
import numpy as np
import re
import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]


def test():
    logger.info('Tests passed')


def main():

    input = get_input()

    logger.info('Result 1')
    logger.info('Result 2')


if __name__ == '__main__':
    test()
    main()
