import logging
import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input():
    with open('day.input') as file:
        return file.read()


def get_test_input():
    return '1122'


def main():

    input = get_input()
    double_input = input + input

    sum_1 = 0
    sum_2 = 0

    for i, val in tqdm(enumerate(input)):
        if int(val) == int(input[i - 1]):
            sum_1 += int(input[i - 1])
        if int(val) == int(double_input[int(i + len(input) / 2)]):
            sum_2 += int(val)

    logger.info('Result 1: %s' % sum_1)
    logger.info('Result 2: %s' % sum_2)


if __name__ == '__main__':
    main()
