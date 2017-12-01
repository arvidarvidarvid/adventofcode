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

    input = [int(i) for i in get_input()]
    double_input = input + input

    captcha = [0, 0]

    for i, val in tqdm.tqdm(enumerate(input)):
        if val == input[i - 1]:
            captcha[0] += input[i - 1]
        if val == double_input[int(i + len(input) / 2)]:
            captcha[1] += val

    logger.info('Result 1: %i' % captcha[0])
    logger.info('Result 2: %i' % captcha[1])


if __name__ == '__main__':
    main()
