from copy import deepcopy


START_DIRECTION = 'N'


def get_instructions():
    with open('1.txt', 'r') as input:
        instructions = input.read().split(',')
    return instructions


def get_new_direction(current_direction, turn_direction):

    turns = {
        'N': {
            'R': 'E',
            'L': 'W'},
        'S': {
            'R': 'W',
            'L': 'E'
        },
        'E': {
            'R': 'S',
            'L': 'N'
        },
        'W': {
            'R': 'N',
            'L': 'S'
        },
    }

    return turns[current_direction][turn_direction]


def follow_instructions(instructions):

    current_position = [0, 0]
    current_direction = START_DIRECTION
    visited_positions = [(0, 0)]
    first_intersect = None

    for i in instructions:

        i = i.strip()
        turn_direction = i[0]
        distance = int(i[1:])

        current_direction = get_new_direction(current_direction,
                                              turn_direction)

        for m in range(1, distance + 1):

            if current_direction == 'N':
                current_position[0] = current_position[0] + 1
            elif current_direction == 'S':
                current_position[0] = current_position[0] - 1
            elif current_direction == 'E':
                current_position[1] = current_position[1] + 1
            elif current_direction == 'W':
                current_position[1] = current_position[1] - 1

            if first_intersect is None:
                if current_position in visited_positions:
                    first_intersect = deepcopy(current_position)

            visited_positions.append(deepcopy(current_position))

    return {
        'current_position': current_position,
        'first_intersect': first_intersect
    }


def get_distance(position):
    return abs(position[0]) + abs(position[1])


def main():

    results = follow_instructions(get_instructions())
    tot_distance = get_distance(results['current_position'])
    intersect_distance = get_distance(results['first_intersect'])

    print('Part 1: Distance to final destination: {tot_distance}'.format(
        tot_distance=tot_distance))
    print('Part 2: Distance to first intersect: {intersect_distance}'.format(
        intersect_distance=intersect_distance))


if __name__ == '__main__':
    main()
