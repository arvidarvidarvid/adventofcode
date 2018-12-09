import numpy as np
import tqdm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_circle_insert_index(length, current_index):
    if length == 1:
        return 1
    else:
        if current_index + 2 <= length:
            return current_index + 2
        else:
            if current_index == length-1:
                return 1
            else:
                return 0
        return -(length - current_index - 2) % (length - 1)


def remove_marble(circle, length, current_index):
    remove_index = (current_index - 7) % length
    removed_marble = circle[remove_index]
    circle = np.delete(circle, remove_index)
    return circle, length-1, removed_marble, remove_index


def recenter_circle(circle, length, current_index):
    zero_index = np.where(circle == 0)[0][0]
    circle = np.concatenate((circle[zero_index:],
                             circle[:zero_index]))
    current_index = (current_index - zero_index) % len(circle)
    return circle, current_index


def print_circle(circle, length, current_index):

    _circle, _current_index = recenter_circle(
        circle, length, current_index)

    s = ''
    for ix, marble in enumerate(_circle[:length]):
        if ix == _current_index:
            s += ' ({}) '.format(marble)
        else:
            s += ' {} '.format(marble)
    print(s)


def play_game(players, last_marble_value):

    circle = np.array([0])
    length = 1
    rounds = 0

    player_list = [i+1 for i in range(players)]
    scores = [0 for i in range(players)]

    next_marble = 1
    current_index = 0

    for _ in tqdm.tqdm(range(int(last_marble_value))):
    # for _ in range(int(last_marble_value)):
        next_player = player_list[rounds % players]

        if next_marble > 0 and next_marble % 23 == 0:
            circle, length, removed_marble, current_index = remove_marble(
                circle, length, current_index)
            score = next_marble + removed_marble
            scores[next_player-1] += score

        else:
            insert_index = get_circle_insert_index(length,
                                                   current_index)
            circle = np.insert(circle, insert_index, next_marble)
            length += 1
            current_index = insert_index

        next_marble += 1
        rounds += 1

        # print_circle(circle, length, current_index)

    #print('elf ', int(player_list[scores.index(max(scores))]),
    #      ' wins with ', int(max(scores)), ' points')

    return max(scores)


def test():

    assert play_game(9, 25) == 32
    assert play_game(10, 1618) == 8317
    assert play_game(13, 7999) == 146373
    assert play_game(17, 1104) == 2764
    assert play_game(21, 6111) == 54718
    assert play_game(30, 5807) == 37305

    # assert p2(test_input_play_game) == 'ABC'
    logger.info('Tests passed')


def main():

    """
    Input: 428 players; last marble is worth 70825 points
    """

    players = 428
    last_marble_value = 70825

    logger.info('Result 1: %s' % play_game(players, last_marble_value))
    logger.info('Result 2: %s' % play_game(players, last_marble_value*100))


if __name__ == '__main__':
    test()
    main()
