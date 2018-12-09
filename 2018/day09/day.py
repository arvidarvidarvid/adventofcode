import tqdm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class Marble(object):

    def __init__(self, value, prev_marble=None, next_marble=None):
        self.value = value
        self._prev = prev_marble
        self._next = next_marble

    def next(self):
        return self._next

    def prev(self):
        return self._prev

    def set_prev(self, new):
        self._prev = new

    def set_next(self, new):
        self._next = new


def print_circle(root_marble, current_marble):

    marble = root_marble
    values = []

    while True:
        if marble == current_marble:
            values.append('({})'.format(marble.value))
        else:
            values.append('{}'.format(marble.value))
        if marble.next() == root_marble:
            break
        marble = marble.next()

    print(' '.join(values))


def play_game(n_players, last_marble_value):

    root_marble = Marble(0)
    current_marble = root_marble
    current_marble.set_prev(current_marble)
    current_marble.set_next(current_marble)

    players = [i for i in range(n_players)]
    scores = [0 for i in range(n_players)]
    rounds = 0
    next_value = 1

    for _ in tqdm.tqdm(range(last_marble_value)):

        # print_circle(root_marble, current_marble)

        player = players[rounds % n_players]

        if next_value % 23 == 0:
            to_remove = current_marble.prev().prev().prev().prev().prev().prev().prev()
            score = to_remove.value + next_value
            scores[player] += score
            current_marble = to_remove.next()
            prev = to_remove.prev()
            prev.set_next(current_marble)
            current_marble.set_prev(prev)

        else:
            new_marble = Marble(next_value,
                                current_marble.next(),
                                current_marble.next().next())
            new_marble.prev().set_next(new_marble)
            new_marble.next().set_prev(new_marble)
            current_marble = new_marble

        next_value += 1
        rounds += 1

    return max(scores)


def test():

    assert play_game(9, 25) == 32
    assert play_game(10, 1618) == 8317
    assert play_game(13, 7999) == 146373
    assert play_game(17, 1104) == 2764
    assert play_game(21, 6111) == 54718
    assert play_game(30, 5807) == 37305

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
