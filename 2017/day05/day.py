from copy import deepcopy
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input():
    with open('day.input', 'r') as file:
        return file.readlines()


def increment_and_jump(input, index, jumps=0, increment_only=True):
    while True:
        try:
            instruction = input[int(index)]
            if instruction > 2 and increment_only is False:
                input[int(index)] -= 1
            else:
                input[int(index)] += 1
            index = int(index) + instruction
            jumps = jumps + 1
        except IndexError:
            break
    return(jumps)


def test():
    input = [0, 3, 0, 1, -3]
    first_test = increment_and_jump(deepcopy(input), 0, 0, True)
    assert first_test == 5
    second_test = increment_and_jump(deepcopy(input), 0, 0, False)
    assert second_test == 10
    return True


def main():

    input = get_input()
    input = [int(row) for row in input]

    logger.info('Result 1: %s' % increment_and_jump(
        deepcopy(input), 0, 0, True))
    logger.info('Result 2: %s' % increment_and_jump(
        deepcopy(input), 0, 0, False))


if __name__ == '__main__':

    if test():
        main()
