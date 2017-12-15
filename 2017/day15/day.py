from tqdm import tqdm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def gen_next(prev, multiplier, picky=False, picky_mod=None):
    magic = 2147483647
    val = (prev * multiplier) % magic
    if picky:
        while val % picky_mod != 0:
            val = (val * multiplier) % magic
        return val
    else:
        return val


def run_generators(start_a, start_b, iterations, picky=False):
    _a = gen_next(start_a, 16807, picky, 4)
    _b = gen_next(start_b, 48271, picky, 8)
    score = 0
    for i in tqdm(range(int(iterations))):
        score += int(bin(_a)[-16:] == bin(_b)[-16:])
        _a = gen_next(_a, 16807, picky, 4)
        _b = gen_next(_b, 48271, picky, 8)
    return score


def test():
    a, b = (65, 8921)
    assert run_generators(a, b, 5) == 1
    assert run_generators(a, b, 1056, picky=True) == 1
    logger.info('Tests passed')


def main():
    a, b = (512, 191)
    logger.info('Result 1: %s' % run_generators(a, b, 40 * 10e6))
    logger.info('Result 2: %s' % run_generators(a, b, 5 * 10e6, picky=True))


if __name__ == '__main__':
    test()
    main()
