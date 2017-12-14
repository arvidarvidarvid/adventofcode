import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return list(map(int, file.read().split(',')))


def get_raw_input(filename='day.input'):
    with open(filename, 'r') as file:
        return file.read()


def get_list(length=5):
    return list(range(length))


def input_as_bytes_to_lengths(input):
    return [ord(c) for c in input] + [17, 31, 73, 47, 23]


def apply_instructions(circle, instructions, rounds=1):
    index = 0
    skip_size = 0
    _round = 0
    while _round < rounds:
        for length in instructions:
            index = index % len(circle)
            if length <= len(circle):
                double_circle = circle + circle
                sub_list = double_circle[index:index + length]
                sub_list.reverse()
                for i, v in enumerate(sub_list):
                    circle[(index + i) % len(circle)] = v
            index += length + skip_size
            skip_size += 1
        _round += 1
    return circle


def to_dense_hash(circle):
    blocks = []
    for i in range(16):
        blocks.append(circle[i * 16:(i + 1) * 16])
    hash = ''
    for block in blocks:
        hash += block_to_hex(block)
    return hash


def block_to_hex(block):
    _val = block[0] ^ block[1]
    for j in range(14):
        _val = _val ^ block[j + 2]
    _hex = format(_val, 'x')
    if len(_hex) == 1:
        _hex = '0' + _hex
    return _hex


def validate(circle):
    return circle[0] * circle[1]


def ih(input):
    return to_dense_hash(apply_instructions(
        get_list(256), input_as_bytes_to_lengths(input), 64))


def test():
    test_input = get_input('test.input')
    assert validate(apply_instructions(get_list(), test_input)) == 12
    assert (input_as_bytes_to_lengths('1,2,3') ==
            [49, 44, 50, 44, 51, 17, 31, 73, 47, 23])
    assert ih('') == 'a2582a3a0e66e6e86e3812dcb672a272'
    ih('AoC 2017') == '33efeb34ea91902bb2f59c9920caa6cd'
    ih('1,2,3') == '3efbe78a8d82f29979031a4aa0b16a9d'
    ih('1,2,4') == '63960835bcdc130f0b66d7ff4f6a5a8e'

    logger.info('Tests passed')


def main():
    logger.info('Result 1: %s' % validate(
        apply_instructions(get_list(256), get_input())))
    logger.info('Result 2: %s' % ih(get_raw_input()))


if __name__ == '__main__':
    test()
    main()
