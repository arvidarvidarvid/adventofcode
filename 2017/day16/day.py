from copy import deepcopy
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return file.read()


def dance(input, programs):

    instructions = input.split(',')

    for i in instructions:
        if i[0] == 's':
            programs = spin(programs, int(i[1:]))
        elif i[0] == 'x':
            ix_1, ix_2 = i[1:].split('/')
            programs = exchange(programs, int(ix_1), int(ix_2))
        elif i[0] == 'p':
            programs = partner(programs, i[1], i[3])
        else:
            print('failed to parse instruction', i)

    return programs


def dances(input, programs, dances=1):

    start_programs = deepcopy(programs)
    programs = dance(input, programs)
    period = 1

    while programs != start_programs:
        programs = dance(input, programs)
        period += 1

    if period > dances:
        programs = start_programs
        remaining_dances = dances
    else:
        remaining_dances = dances - int(dances / period) * period

    for i in range(remaining_dances):
        programs = dance(input, programs)

    return programs


def spin(programs, n):
    return programs[-n:] + programs[:len(programs) - n]


def exchange(programs, ix_1, ix_2):
    first, second = (programs[ix_1], programs[ix_2])
    programs[ix_1] = second
    programs[ix_2] = first
    return programs


def partner(programs, first, second):
    first_ix, second_ix = (programs.index(first), programs.index(second))
    programs[first_ix] = second
    programs[second_ix] = first
    return programs


def test():
    programs = ['a', 'b', 'c', 'd', 'e']
    test_input = 's1,x3/4,pe/b'
    assert dance(test_input, programs) == ['b', 'a', 'e', 'd', 'c']
    assert dances(test_input, programs, 2) == ['c', 'e', 'a', 'd', 'b']
    logger.info('Tests passed')


def main():

    input = get_input()
    programs = [c for c in 'abcdefghijklmnop']

    logger.info('Result 1: %s' % ''.join(dance(input, programs)))

    programs = [c for c in 'abcdefghijklmnop']
    logger.info('Result 2: %s' % ''.join(dances(input, programs, 1000000000)))


if __name__ == '__main__':
    test()
    main()
