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


def get_visited_tuples(instructions):
    visits = set([(0,0)])
    position = [0,0]
    visit_distances = {}
    total_moves = 0
    for instruction in instructions:
        d = instruction[0]
        distance = int(instruction[1:])
        directions = {
            'U': (1, 0),
            'D': (-1, 0),
            'L': (0, -1),
            'R': (0, 1)
        }
        for moves in range(0, distance):
            position[0] += directions[d][0]
            position[1] += directions[d][1]
            total_moves += 1
            visits.add((position[0], position[1]))
            if position[0] not in visit_distances:
                visit_distances[position[0]] = {}
            if position[1] not in visit_distances[position[0]]:
                visit_distances[position[0]][position[1]] = total_moves

    visits.remove((0, 0))
    return visits, visit_distances


def get_manhattan_distance(t):
    return abs(t[0]) + abs(t[1])


def p1(puzzle_input):
    first_wire_instructions = puzzle_input[0].split(',')
    second_wire_instructions = puzzle_input[1].split(',')
    first_wire_visits, first_wire_distances = get_visited_tuples(first_wire_instructions)
    second_wire_visits, second_wire_distances = get_visited_tuples(second_wire_instructions)
    overlaps = first_wire_visits.intersection(second_wire_visits)
    shortest_distance = 1000000000000
    for overlap in overlaps:
        _distance = get_manhattan_distance(overlap)
        if _distance < shortest_distance:
            shortest_distance = _distance
    return shortest_distance


def p2(puzzle_input):
    first_wire_instructions = puzzle_input[0].split(',')
    second_wire_instructions = puzzle_input[1].split(',')
    first_wire_visits, first_wire_distances = get_visited_tuples(first_wire_instructions)
    second_wire_visits, second_wire_distances = get_visited_tuples(second_wire_instructions)
    overlaps = first_wire_visits.intersection(second_wire_visits)
    fewest_combined_steps = 1000000000000
    for overlap in overlaps:
        _d1 = first_wire_distances[overlap[0]][overlap[1]]
        _d2 = second_wire_distances[overlap[0]][overlap[1]]
        fewest_combined_steps = min([fewest_combined_steps, _d1+_d2])
    return fewest_combined_steps


def test():
    test_input_p1 = get_input('test_p1.input')
    #test_input_p2 = get_input('test_p2.input')
    assert p1(test_input_p1) == 6
    #assert p2(test_input_p2) == None
    logger.info('Tests passed')


def main():

    puzzle_input = get_input()

    logger.info('Result 1: %s' % p1(puzzle_input))
    logger.info('Result 2: %s' % p2(puzzle_input))


if __name__ == '__main__':
    test()
    main()
