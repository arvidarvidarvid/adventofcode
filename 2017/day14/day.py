import logging
from knothash import input_to_hex


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    return open(filename, 'r').read()


def hex_hash_to_bits(hexhash):
    return bin(int(hexhash, 16))[2:].zfill(128)


def get_hashes(seed, count):
    hashes = []
    for i in range(0, count):
        input = ''.join([seed, '-', str(i)])
        hashes.append(hex_hash_to_bits(input_to_hex(input)))
    return hashes


def hashes_to_used(hashes):
    return sum([int(c) for h in hashes for c in h])


def pad_hashes(hashes):
    hashes = [hash.replace('0', '.').replace('1', '#') for hash in hashes]
    padded_hash = [['.' for i in range(0, len(hashes) + 2)]]
    for i in range(0, len(hashes)):
        padded_hash.append(['.'] + [c for c in hashes[i]] + ['.'])
    padded_hash += [['.' for i in range(0, len(hashes) + 2)]]
    return padded_hash


def find_groups(hashes):
    hashes = pad_hashes(hashes)
    groups = []
    num_groups = 0
    for y, hash in enumerate(hashes):
        for x, char in enumerate(hash):
            group_coords = find_related_coords(y, x, num_groups, hashes)
            groups.append(group_coords)
            if group_coords != []:
                num_groups += 1
    return num_groups, hashes


def find_related_coords(y, x, group_index, hashes):

    if hashes[y][x] != '#':
        return []

    hashes[y][x] = group_index
    _group_neighbours = [(y, x)]

    for offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        _y = y + offset[0]
        _x = x + offset[1]
        if hashes[_y][_x] == '#':
            _group_neighbours += find_related_coords(
                _y, _x, group_index, hashes)

    return list(set(_group_neighbours))


def print_rect(hashes, size):
    for hash in hashes[:size]:
        print(hash[:size])


def test():
    test_input = get_input('test.input')
    hashes = get_hashes(test_input, 128)
    assert hashes_to_used(hashes) == 8108
    groups, hashes = find_groups(hashes)
    assert groups == 1242
    logger.info('Tests passed')
    return True


def main():

    input = get_input()
    hashes = get_hashes(input, 128)

    logger.info('Result 1: %s' % hashes_to_used(hashes))
    groups, _ = find_groups(hashes)
    logger.info('Result 2: %s' % groups)


if __name__ == '__main__':
    test()
    main()
