import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]


class Point(object):

    def __init__(self, pos_x, pos_y, vel_x, vel_y):
        self.pos_x = int(pos_x)
        self.pos_y = int(pos_y)
        self.vel_x = int(vel_x)
        self.vel_y = int(vel_y)

    def update_position(self):
        self.pos_x = self.pos_x + self.vel_x
        self.pos_y = self.pos_y + self.vel_y

    def reverse_position(self):
        self.pos_x = self.pos_x - self.vel_x
        self.pos_y = self.pos_y - self.vel_y

    def yx_pos(self):
        return (self.pos_y, self.pos_x)


def line_to_point(line):
    pattern = r'position=<(.*)> velocity=<(.*)>'
    pos, vel = re.match(pattern, line).groups()
    pos_x, pos_y = pos.strip().split(', ')
    vel_x, vel_y = vel.strip().split(', ')
    return Point(pos_x, pos_y, vel_x, vel_y)


def get_dimensions(points):
    all_x = [p.pos_x for p in points]
    all_y = [p.pos_y for p in points]

    min_x = min(all_x)
    max_x = max(all_x)
    min_y = min(all_y)
    max_y = max(all_y)

    width = max_x - min_x
    height = max_y - min_y

    return width, height, min_x, min_y


def draw_points(points, max_size=1000000):

    width, height, min_x, min_y = get_dimensions(points)

    plane = [[' ' for x in range(width+1)] for y in range(height+1)]

    for point in points:
        _y, _x = point.yx_pos()
        plane[_y - min_y][_x - min_x] = '#'

    for row in plane:
        print(''.join(row))

def p1(puzzle_input):

    points = [line_to_point(line) for line in puzzle_input]
    width, height, _, _ = get_dimensions(points)
    print('Loaded', str(len(points)), 'points')

    # Assuming that constellation shrinks until the message is shown, find
    # time of smallest constellation

    smallest_time = 0
    smallest_size = width * height

    time = 0
    while True:
        time += 1
        for point in points:
            point.update_position()
        width, height, _, _ = get_dimensions(points)
        if width * height < smallest_size:
            smallest_size = width * height
            smallest_time = time
        else:
            for point in points:
                point.reverse_position()
            time -= 1
            break

    draw_points(points)
    print('Message shows up after', str(smallest_time), 'seconds')

    return smallest_time


def main():

    puzzle_input = get_input()
    p1(puzzle_input)

if __name__ == '__main__':
    main()
