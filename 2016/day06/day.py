import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input():
    with open('day.input', 'r') as file:
        return [row.strip() for row in file.readlines()]


def recover_message(rows, reversed=False):

    reversed = not reversed
    chars = [chr(i) for i in range(97, 123)]
    message = ''
    for i in range(len(rows[0])):
        candidates = []
        for row in rows:
            candidates.append(row[i])
        counts = []
        for c in chars:
            if candidates.count(c) != 0:
                counts.append((candidates.count(c), c))
        counts = sorted(counts, reverse=reversed)
        message += counts[0][1]

    return message


def test():
    raw_test_input = """eedadn
    drvtee
    eandsr
    raavrd
    atevrs
    tsrnev
    sdttsa
    rasrtv
    nssdts
    ntnada
    svetve
    tesnvt
    vntsnd
    vrdear
    dvrsen
    enarar"""
    test_input = [row.strip() for row in raw_test_input.split('\n')]
    assert recover_message(test_input, False) == 'easter'
    assert recover_message(test_input, True) == 'advent'
    logger.info('Tests passed')


def main():

    input = get_input()
    logger.info('Result 1: %s' % recover_message(input, False))
    logger.info('Result 2: %s' % recover_message(input, True))


if __name__ == '__main__':

    test()
    main()
