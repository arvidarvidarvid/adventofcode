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


def get_input():
    with open('day.input', 'r') as file:
        return file.read()


def test():
    logger.info('Tests passed')


def main():

    input = get_input()

    logger.info('Result 1')
    logger.info('Result 2')


if __name__ == '__main__':
    test()
    main()
