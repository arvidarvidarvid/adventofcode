from copy import deepcopy
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input():
    with open('day.input', 'r') as file:
        return list(map(int, file.read().split()))


def reallocate(banks, break_for_banks=False):

    previous_banks = []
    rounds = 0
    initial_banks = deepcopy(banks)

    while True:

        # One round of reallocation
        max_val = max(banks)
        max_index = banks.index(max_val)
        to_distribute = banks[max_index]
        banks[max_index] = 0
        update_index = max_index + 1
        while to_distribute > 0:
            banks[update_index % (len(banks))] += 1
            update_index += 1
            to_distribute -= 1
        rounds += 1

        # Memoize and check for exit condiitions
        if break_for_banks and banks == initial_banks:
            return rounds, banks
        elif banks not in previous_banks:
            previous_banks.append(deepcopy(banks))
        else:
            return rounds, banks


def test():
    banks = [0, 2, 7, 0]
    rounds, banks = reallocate(banks)
    assert rounds == 5
    rounds, banks = reallocate(banks, True)
    assert rounds == 4
    return True


def main():

    input = get_input()
    rounds_1, banks = reallocate(input)
    rounds_2, banks = reallocate(banks, True)
    logger.info('Result 1: %s' % rounds_1)
    logger.info('Result 2: %s' % rounds_2)


if __name__ == '__main__':
    test()
    main()
