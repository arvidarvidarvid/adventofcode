import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]


def get_line_of_pots(puzzle_input):
    string = puzzle_input[0][15:].strip()
    pots = []
    for ix, char in enumerate(string):
        pots.append((ix, char))
    return re_pad_line(pots)


def re_pad_line(pots):
    as_string = pots_as_string(pots)
    stripped = pots[as_string.index('#'):as_string.rindex('#')+1]
    return ([(stripped[0][0]-3, '.'), (stripped[0][0]-2, '.'), (stripped[0][0]-1, '.')] + stripped +
            [(stripped[-1][0]+1, '.'), (stripped[-1][0]+2, '.'), (stripped[-1][0]+3, '.')])


def get_evolutions(puzzle_input):
    evolutions = {}
    for line in puzzle_input[2:]:
        pattern, outcome = line.split(' => ')
        evolutions[pattern] = outcome
    return evolutions


def get_pot_line_score(pots):
    score = 0
    for pot in pots:
        if pot[1] == '#':
            score += pot[0]
    return score


def get_next_generation(pots, evolutions):

    new_pots = []
    for ix, pot in enumerate(pots):
        if ix < 2 or ix > len(pots) - 3:
            new_pots.append(pot)
        else:
            try:
                pattern = ''.join([p[1] for p in pots[ix-2:ix+3]])
                new_pots.append((pot[0], evolutions[pattern]))
                #print(pattern, pot, evolutions[pattern])
            except KeyError:
                new_pots.append((pot[0], '.'))

    return new_pots


def pots_as_string(pots):
    return ''.join([pot[1] for pot in pots])


def print_pots(pots):
    string = ''
    for pot in pots:
        if pot[1] == '#':
            string += str(pot[0])
        else:
            string += '.'
    print(string)


def p1(puzzle_input, iterations):
    pots = get_line_of_pots(puzzle_input)
    evolutions = get_evolutions(puzzle_input)
    for _ in range(iterations):
        pots = get_next_generation(pots, evolutions)
        pots = re_pad_line(pots)
    return get_pot_line_score(pots)


def p2(puzzle_input, total_iterations):

    pots = get_line_of_pots(puzzle_input)
    evolutions = get_evolutions(puzzle_input)
    iterations = 0
    new_pots = None

    while True:
        iterations += 1
        new_pots = get_next_generation(pots, evolutions)
        new_pots = re_pad_line(new_pots)
        if pots_as_string(pots) == pots_as_string(new_pots):
            break
        pots = new_pots

    score_per_round = get_pot_line_score(new_pots) - get_pot_line_score(pots)
    score = (get_pot_line_score(new_pots) +
             (total_iterations-iterations)*score_per_round)

    return score


def test():
    test_input_p1 = get_input('test.input')
    assert p1(test_input_p1, 20) == 325
    # assert p2(test_input_p1) == 'ABC'
    logger.info('Tests passed')


def main():

    puzzle_input = get_input()

    logger.info('Result 1: %s' % p1(puzzle_input, 20))
    logger.info('Result 2: %s' % p2(puzzle_input, 50000000000))


if __name__ == '__main__':
    test()
    main()
