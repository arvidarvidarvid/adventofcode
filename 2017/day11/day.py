import tqdm
from copy import deepcopy
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return file.read()


def get_distance(raw_moves):
    moves = raw_moves.split(',')
    lost_position, largest_distance = get_lost(moves)
    moves_back = trace_back(lost_position)
    return moves_back, largest_distance


def get_lost(moves):
    pos = [0, 0]
    furthest_from_home = 0
    for move in tqdm.tqdm(moves):
        pos = apply_move(pos, move)
        distance = trace_back(pos)
        furthest_from_home = max([distance, furthest_from_home])
    return pos, furthest_from_home


def trace_back(pos):
    moves_back = 0
    pos = deepcopy(pos)
    while pos != [0, 0]:
        if pos[0] > 0:
            if pos[1] >= 0:
                pos = apply_move(pos, 'n')
            else:
                pos = apply_move(pos, 'ne')
        if pos[0] == 0:
            if pos[1] > 0:
                pos = apply_move(pos, 'nw')
            else:
                pos = apply_move(pos, 'se')
        if pos[0] < 0:
            if pos[1] < 0:
                pos = apply_move(pos, 's')
            else:
                pos = apply_move(pos, 'sw')
        moves_back += 1
    return moves_back


def apply_move(position, move):
    valid_moves = {'n': (-1, -1),
                   'nw': (0, -1),
                   'ne': (-1, 0),
                   's': (1, 1),
                   'sw': (1, 0),
                   'se': (0, 1)}
    position[0] += valid_moves[move][0]
    position[1] += valid_moves[move][1]
    return position


def test():
    assert get_distance('ne,ne,ne')[0] == 3
    assert get_distance('ne,ne,sw,sw')[0] == 0
    assert get_distance('ne,ne,s,s')[0] == 2
    assert get_distance('se,sw,se,sw,sw')[0] == 3
    assert True is True
    logger.info('Tests passed')


def main():

    input = get_input()

    moves_home, largest_distance = get_distance(input)

    logger.info('Result 1: %s' % moves_home)
    logger.info('Result 2: %s' % largest_distance)


if __name__ == '__main__':
    test()
    main()
