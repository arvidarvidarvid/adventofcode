from copy import deepcopy
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return [line.strip('\n') for line in file.readlines()]


class Cart(object):

    DIRECTION_TO_TURNS = {
        '^': {'left': '<', 'right': '>', 'straight': '^'},
        '>': {'left': '^', 'right': 'v', 'straight': '>'},
        'v': {'left': '>', 'right': '<', 'straight': 'v'},
        '<': {'left': 'v', 'right': '^', 'straight': '<'}
    }

    DIRECTIONS_TO_OFFSETS = {
        '^':  (0,  -1),
        '>':  (1,   0),
        'v':  (0,   1),
        '<':  (-1,  0)
    }

    DIR_TO_TURN_TO_DIR = {
        '^': {'\\': '<', '/': '>'},
        '>': {'\\': 'v', '/': '^'},
        'v': {'\\': '>', '/': '<'},
        '<': {'\\': '^', '/': 'v'}
    }

    NEXT_TURN = {
        'left': 'straight',
        'straight': 'right',
        'right': 'left'
    }

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.next_turn = 'left'

    def move(self, tracks):
        self.x = self.x + self.DIRECTIONS_TO_OFFSETS[self.direction][0]
        self.y = self.y + self.DIRECTIONS_TO_OFFSETS[self.direction][1]
        next_tile = tracks[self.y][self.x]
        if next_tile in ('\\','/'):
            self.direction = self.DIR_TO_TURN_TO_DIR[self.direction][next_tile]
        elif next_tile == '+':
            self.direction = self.DIRECTION_TO_TURNS[self.direction][self.next_turn]
            self.next_turn = self.NEXT_TURN[self.next_turn]
        return self.position()

    def position(self):
        return (self.x, self.y)

    def yx_coords(self):
        return (self.y, self.x)


def get_tracks_and_carts(puzzle_input):
    tracks = []
    carts = []
    for y, line in enumerate(puzzle_input):
        track_line = []
        for x, char in enumerate(line):
            if char in '<>v^':
                carts.append(Cart(x, y, char))
                if char in '<>':
                    track_line.append('-')
                else:
                    track_line.append('|')
            else:
                track_line.append(char)
        tracks.append(track_line)
    return tracks, carts


def draw_tracks(tracks, carts):
    _tracks = deepcopy(tracks)
    for cart in carts:
        _tracks[cart.y][cart.x] = cart.direction
    for line in _tracks:
        print(''.join(line))


def check_collissions(cart, carts):
    for _cart in carts:
        if cart != _cart:
            if _cart.position() == cart.position():
                return _cart
    return None


def p1(puzzle_input):
    tracks, carts = get_tracks_and_carts(puzzle_input)
    while True:
        for cart in sorted(carts, key=lambda c: c.yx_coords()):
            cart.move(tracks)
            if check_collissions(cart, carts) is not None:
                return cart.position()


def p2(puzzle_input):
    tracks, carts = get_tracks_and_carts(puzzle_input)
    while True:
        if len(carts) == 1:
            return carts[0].position()
        for cart in sorted(carts, key=lambda c: c.yx_coords()):
            cart.move(tracks)
            colliding_cart = check_collissions(cart, carts)
            if colliding_cart is not None:
                carts.remove(cart)
                carts.remove(colliding_cart)

def test():
    test_input_p1 = get_input('test.input')
    assert p1(test_input_p1) == (7, 3)
    test_input_p2 = get_input('test2.input')
    assert p2(test_input_p2) == (6, 4)
    logger.info('Tests passed')


def main():

    puzzle_input = get_input()

    logger.info('Result 1: %s' % str(p1(puzzle_input)))
    logger.info('Result 2: %s' % str(p2(puzzle_input)))


if __name__ == '__main__':
    test()
    main()
