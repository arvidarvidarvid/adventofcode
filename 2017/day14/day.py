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
    s = 0
    for h in hashes:
        for c in h:
            s += int(c)
    return s


def pad_hashes(hashes):
    padded_hash = [''.join(['0' for i in range(0, len(hashes) + 2)])]
    for i in range(0, len(hashes)):
        padded_hash.append('0' + hashes[i] + '0')
    padded_hash.append(''.join(['0' for i in range(0, len(hashes) + 2)]))
    return padded_hash


def find_groups(hashes):
    hashes = pad_hashes(hashes)
    groups = []
    seen_coords = []
    for y, hash in enumerate(hashes):
        for x, char in enumerate(hash):
            group_coords = find_related_coords(y, x, seen_coords, hashes)
            groups.append(group_coords)
            seen_coords += group_coords
            seen_coords = list(set(seen_coords))
    return sum([1 for g in groups if len(g) > 0])


def find_related_coords(y, x, seen_coords, hashes):

    if hashes[y][x] == '0' or (y, x) in seen_coords:
        return []

    _seen = seen_coords
    _seen.append((y, x))
    _group_neighbours = [(y, x)]

    for offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        _y = y + offset[0]
        _x = x + offset[1]
        if hashes[_y][_x] == '1':
            if (_y, _x) not in _seen:
                _group_neighbours += find_related_coords(_y, _x, _seen, hashes)
                _seen += _group_neighbours

    return list(set(_group_neighbours))


def test():
    test_input = get_input('test.input')
    hashes = get_hashes(test_input, 128)
    assert hashes_to_used(hashes) == 8108
    groups = find_groups(hashes)
    assert groups == 1242
    logger.info('Tests passed')
    return True


def main():

    input = get_input()
    hashes = get_hashes(input, 128)

    logger.info('Result 1: %s' % hashes_to_used(hashes))
    logger.info('Result 2: %s' % find_groups(hashes))


if __name__ == '__main__':
    test()
    main()
