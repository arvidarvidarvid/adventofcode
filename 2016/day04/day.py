import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input():
    with open('day.input', 'r') as file:
        return file.readlines()


def validate_room(line, decrypt=False):
    pattern = r'([a-z\-]+)([0-9]*)\[([a-z0-9]{5})\]'
    groups = re.match(pattern, line.strip())
    code = ''.join(sorted(groups[1])).replace('-', '')
    sector_id = groups[2]
    checksum = groups[3]
    chars = [chr(i) for i in range(97, 123)]
    counts = []
    for c in chars:
        if code.count(c) != 0:
            counts.append((code.count(c), -ord(c)))
    counts = sorted(counts, reverse=True)
    valid_checksum = ''.join([chr(-c[1]) for c in counts[:5]])
    if valid_checksum == checksum:
        if decrypt:
            return int(sector_id), decrypt_string(groups[1], int(sector_id))
        return int(sector_id), code, checksum
    else:
        return False


def get_sector_id_for_decrypted_room(inputs, room_name):
    for line in inputs:
        result = validate_room(line, decrypt=True)
        if result is not False:
            sector_id, decrypted_name = result
            if decrypted_name == room_name:
                return sector_id


def decrypt_string(string, offset):
    offset = offset % 26
    chars = [chr(i) for i in range(97, 123)]
    chars += chars
    decrypted = ''
    for char in string:
        if char in chars:
            decrypted += chars[chars.index(char) + offset]
        else:
            decrypted += char
    return decrypted.strip('-')


def test():
    assert validate_room('aaaaa-bbb-z-y-x-123[abxyz]')[0] == 123
    assert validate_room('a-b-c-d-e-f-g-h-987[abcde]')[0] == 987
    assert validate_room('not-a-real-room-404[oarel]')[0] == 404
    assert validate_room('totally-real-room-200[decoy]') is False
    assert (decrypt_string('qzmt-zixmtkozy-ivhz-', 343) ==
            'very-encrypted-name')


def main():

    input = list(get_input())

    logger.info('Result 1: %s' % sum(
        [validate_room(i)[0] for i in input if validate_room(i)]))
    logger.info('Result 2: %s' % get_sector_id_for_decrypted_room(
        input, 'northpole-object-storage'))


if __name__ == '__main__':

    test()
    main()
