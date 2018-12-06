import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]


def get_nodes(puzzle_input):
    nodes = []
    for node in puzzle_input:
        pattern = r'(\d+), (\d+)'
        groups = re.match(pattern, node).groups()
        nodes.append((int(groups[0]), int(groups[1])))
    return nodes


def generate_board(nodes):

    all_x = [n[0] for n in nodes]
    all_y = [n[1] for n in nodes]

    board = [[' ' for i in range(0, max(all_x)+2)] for j in range(0, max(all_y) + 2)]

    return board


def position_nodes(nodes, board):

    for node, coordinates in enumerate(nodes):
        board[coordinates[1]][coordinates[0]] = node

    return board


def draw_board(board):
    for row in board:
        print(''.join(list(map(str, row))))


def manhattan_distance(c0, c1):
    return abs(c0[0] - c1[0]) + abs(c0[1] - c1[1])


def find_closest_node(nodes, coords):
    distances = []
    for node, node_coords in enumerate(nodes):
        distances.append((manhattan_distance(node_coords, coords), node))
    distances = sorted(distances, key=lambda x: x[0])
    if distances[0][0] == distances[1][0]:
        return '.'
    else:
        return distances[0][1]


def assign_positions(nodes, board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            board[y][x] = find_closest_node(nodes, (x, y))

    return board


def strip_infinite_fields(board):

    edge_nodes = []
    for cell in board[0]:
        edge_nodes.append(cell)
    for cell in board[len(board)-1]:
        edge_nodes.append(cell)
    for row in board:
        edge_nodes.append(row[0])
        edge_nodes.append(row[len(row)-1])

    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if board[y][x] in edge_nodes:
                board[y][x] = '.'

    return board


def find_largest_area(board):

    areas = {}

    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            label = board[y][x]
            if label in areas and label != '.':
                areas[label] += 1
            else:
                areas[label] = 1

    largest_size = 0
    for label, size in areas.items():
        if size > largest_size:
            largest_size = size

    return largest_size


def distance_if_within_max_distance_to_all_nodes(nodes, coord, max_distance):
    total_distances = 0
    for node in nodes:
        total_distances += manhattan_distance(node, coord)
    if total_distances < max_distance:
        return total_distances
    else:
        return None


def assign_area_within_max_distance_from_all_nodes(nodes, board, max_distance):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            total_distances = distance_if_within_max_distance_to_all_nodes(
                nodes, (x, y), max_distance)
            if total_distances is not None:
                board[y][x] = '#'
    return board


def get_size_of_highlighted_area(board, highlight_marker='#'):
    area = 0
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if board[y][x] == highlight_marker:
                area += 1
    return area


def p1(puzzle_input):
    nodes = get_nodes(puzzle_input)
    board = generate_board(nodes)
    board = position_nodes(nodes, board)
    board = assign_positions(nodes, board)
    board = strip_infinite_fields(board)
    return find_largest_area(board)


def p2(puzzle_input, max_distance=10000):
    nodes = get_nodes(puzzle_input)
    board = generate_board(nodes)
    board = position_nodes(nodes, board)
    board = assign_area_within_max_distance_from_all_nodes(
        nodes, board, max_distance)
    return get_size_of_highlighted_area(board)


def test():
    test_input_p1 = get_input('test_p1.input')
    assert p1(test_input_p1) == 17
    assert p2(test_input_p1, max_distance=32) == 16
    logger.info('Tests passed')


def main():

    puzzle_input = get_input()

    logger.info('Result 1: %s' % p1(puzzle_input))
    logger.info('Result 2: %s' % p2(puzzle_input))


if __name__ == '__main__':
    test()
    main()
