import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def step_and_insert(step_size, n_inserts=1):
    circle = [0]
    position = 0
    for s in range(1, n_inserts + 1):
        position = (position + step_size) % s
        circle.insert(position + 1, s)
        position += 1
    return circle


def val_after_val(circle, after_val):
    ix = circle.index(after_val)
    return circle[ix + 1]


def val_after_val_nonmaterialized():
    inserts = 50000000
    step_size = 366
    position = 0
    val_after_zero = None
    for s in range(1, inserts + 1):
        position = (position + step_size) % s
        if position == 0:
            val_after_zero = s
        position += 1
    return val_after_zero


def test():
    test_input = 3
    circle = step_and_insert(test_input, n_inserts=2017)
    assert val_after_val(circle, 2017) == 638
    logger.info('Tests passed')


def main():
    input = 366
    circle = step_and_insert(input, n_inserts=2017)
    logger.info('Result 1: %s' % val_after_val(circle, 2017))
    logger.info('Result 2: %s' % val_after_val_nonmaterialized())


if __name__ == '__main__':
    test()
    main()
