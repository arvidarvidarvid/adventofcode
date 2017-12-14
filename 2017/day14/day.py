from knothash import input_to_hex


def get_input(filename='day.input'):
    return open(filename, 'r').read()


def hex_to_bin(hexhash):
    return bin(int(hexhash, 16))[2:].zfill(128)


def get_hashes(seed, n):
    hashes = [hex_to_bin(input_to_hex(seed + '-' + str(i)))
              .replace('1', '#').replace('0', '.') for i in range(0, n)]
    dot_line = ['.' for i in range(0, len(hashes) + 2)]
    return [dot_line] + [['.'] + [c for c in hashes[i]] + ['.']
                         for i in range(len(hashes))] + [dot_line]


def hashes_to_used(hashes):
    return sum([1 for h in hashes for c in h if c == '#'])


def count_groups(hashes):
    num_groups = 0
    for y, hash in enumerate(hashes):
        for x, char in enumerate(hash):
            num_groups += expand_group(y, x, num_groups, hashes)
    return num_groups, hashes


def expand_group(y, x, group_index, hashes):
    if hashes[y][x] != '#':
        return 0
    hashes[y][x] = group_index
    for offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        _y = y + offset[0]
        _x = x + offset[1]
        expand_group(_y, _x, group_index, hashes)
    return 1


def test():
    test_input = get_input('test.input')
    hashes = get_hashes(test_input, 128)
    assert hashes_to_used(hashes) == 8108
    assert count_groups(hashes)[0] == 1242
    print('Tests passed')


def main():
    input = get_input()
    hashes = get_hashes(input, 128)
    print('Result 1: %s' % hashes_to_used(hashes))
    groups, _ = count_groups(hashes)
    print('Result 2: %s' % groups)


if __name__ == '__main__':
    test()
    main()
