"""
from datetime import datetime, timedelta
import itertools
import math
import numpy as np
import re
"""
from copy import deepcopy
from tqdm import tqdm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        l = file.read().strip().split(',')
        return [int(i) for i in l]


class IntCodeComputer():

    def __init__(self, program, noun=None, verb=None):
        self.memory = deepcopy(program)
        self.pointer = 0
        self.noun = noun
        self.verb = verb
        if noun is not None:
            self.memory[1] = self.noun
        if verb is not None:
            self.memory[2] = self.verb

    def start_program(self):
        while self.memory[self.pointer] != 99:
            self.execute_instruction()
        return self.memory[0]

    def execute_instruction(self):
        op_code = self.memory[self.pointer]
        param1 = self.memory[self.pointer+1]
        param2 = self.memory[self.pointer+2]
        param3 = self.memory[self.pointer+3]
        if op_code == 1:
            self.memory[param3] = self.memory[param1] + self.memory[param2]
        if op_code == 2:
            self.memory[param3] = self.memory[param1] * self.memory[param2]
        self.pointer = self.pointer + 4


def p1(puzzle_input, noun=None, verb=None):
    cpu = IntCodeComputer(puzzle_input, noun, verb)
    return cpu.start_program()


def p2(puzzle_input):
    for noun in tqdm(range(0, 99+1)):
        for verb in range(0, 99+1):
            try:
                if p1(puzzle_input, noun, verb) == 19690720:
                    return noun * 100 + verb
            except IndexError:
                pass


def test():
    test_input_p1 = get_input('test_p1.input')
    # test_input_p2 = get_input('test_p2.input')
    assert p1(test_input_p1) == 3500
    # assert p2(test_input_p2) == None
    logger.info('Tests passed')


def main():

    puzzle_input = get_input()

    logger.info('Result 1: %s' % p1(puzzle_input, 12, 2))
    logger.info('Result 2: %s' % p2(puzzle_input))


if __name__ == '__main__':
    test()
    main()
