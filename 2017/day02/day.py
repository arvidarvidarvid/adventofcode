import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input():
    with open('day.input', 'r') as file:
        return file.readlines()


def main():

    input = get_input()
    grid = [list(map(lambda x: int(x), line.split())) for line in input]
    checksum_1 = sum([max(line) - min(line) for line in grid])
    logger.info('Result 1: %s' % checksum_1)

    checksum_2 = sum([
        int(nom / den) for line in grid for i, den in enumerate(sorted(line))
        for nom in sorted(line)[i + 1:] if nom % den == 0])
    logger.info('Result 2: %s' % checksum_2)


if __name__ == '__main__':

    main()
