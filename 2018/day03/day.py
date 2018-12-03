"""
from copy import deepcopy
from datetime import datetime, timedelta
import itertools
import math
import numpy as np
import tqdm
"""
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]


def parse_line(line):
    pattern = r'(#\d+) @ (\d+),(\d+): (\d+)x(\d+)'
    groups = re.match(pattern, line)
    claim, left, top, width, height = groups.groups()
    return (claim, int(left), int(top), int(width), int(height))


def get_overlap_dict(puzzle_input):

    claims = {}

    for line in puzzle_input:
        claim, _l, _t, _w, _h = parse_line(line)

        for left in range(_l, _l + _w):
            for top in range(_t, _t + _h):
                if (left, top) in claims:
                    claims[(left, top)].append(claim)
                else:
                    claims[(left, top)] = [claim]

    return claims


def get_all_claim_ids(puzzle_input):
    ids = []
    for line in puzzle_input:
        claim, _l, _t, _w, _h = parse_line(line)
        ids.append(claim)
    return ids


def p1(puzzle_input):

    claims = get_overlap_dict(puzzle_input)

    overlapping_inches = 0
    for _, v in claims.items():
        if len(v) > 1:
            overlapping_inches += 1

    return overlapping_inches


def p2(puzzle_input):

    claims = get_overlap_dict(puzzle_input)
    ids = set(get_all_claim_ids(puzzle_input))

    for k, v in claims.items():
        if len(v) > 1:
            ids = ids - set(v)

    return list(ids)[0]


def test():
    test_input_p1 = get_input('test_p1.input')
    assert p1(test_input_p1) == 4
    test_input_p2 = get_input('test_p1.input')
    assert p2(test_input_p2) == '#3'
    logger.info('Tests passed')


def main():

    puzzle_input = get_input()

    logger.info('Result 1: %s' % p1(puzzle_input))
    logger.info('Result 2: %s' % p2(puzzle_input))


if __name__ == '__main__':
    test()
    main()
