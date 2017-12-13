import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]


def _set_up_scanners(input):
    _scanners = {}
    for i in input:
        depth, length = re.match(r'(\d+): (\d+)', i).groups()
        _scanners[int(depth)] = int(length)
        max_depth = int(depth)
    scanners = []
    for i in range(0, max_depth + 1):
        if i in _scanners:
            scanners.append(_scanners[i])
        else:
            scanners.append(None)
    return scanners, max_depth


def _check_collisions(position, scanners, tick, non_zero_penalty):
    penalty = 0
    length = scanners[position]
    if length is not None:
        if tick % (length * 2 - 2) == 0:
            penalty = position * length
            if non_zero_penalty and penalty == 0:
                penalty = 1
    return penalty


def _traverse(scanners, max_depth, delay, non_zero_penalty):
    position = -1
    score = 0
    for tick in range(delay, max_depth + 1 + delay):
        if tick >= delay:
            position += 1
            score += _check_collisions(position, scanners, tick,
                                       non_zero_penalty)
        if non_zero_penalty and score > 0:
            return score
    return score


def get_threat_level(input, delay=0, non_zero_penalty=False):
    scanners, max_depth = _set_up_scanners(input)
    return _traverse(scanners, max_depth, delay, non_zero_penalty)


def get_min_threat_level_delay(input, non_zero_penalty=False):
    delay = 0
    score = 1
    scanners, max_depth = _set_up_scanners(input)
    while score != 0:
        delay += 1
        score = _traverse(scanners, max_depth, delay, non_zero_penalty)
    return delay


def test():
    test_input = get_input('test.input')
    score = get_threat_level(test_input)
    assert score == 24
    assert get_min_threat_level_delay(test_input, True) == 10
    logger.info('Tests passed')
    return True


def main():

    input = get_input()

    result_1 = get_threat_level(input)
    logger.info('Result 1: %s' % result_1)

    result_2 = get_min_threat_level_delay(input, True)
    logger.info('Result 2: %s' % result_2)


if __name__ == '__main__':
    if test():
        main()
