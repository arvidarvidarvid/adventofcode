import logging
import hashlib


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input():
    with open('day.input', 'r') as file:
        return file.read()


def find_password(seed, password_length=8, position_specific=False):
    password = ''
    positioned_password = [None for i in range(password_length)]
    pad_int = 0
    while len(password) < password_length and None in positioned_password:
        m = hashlib.md5()
        to_hash = seed + str(pad_int)
        to_hash = to_hash.encode('utf-8')
        m.update(to_hash)
        if m.hexdigest()[:5] == '00000':
            if position_specific:
                try:
                    index = int(m.hexdigest()[5])
                    value = m.hexdigest()[6]
                    if positioned_password[index] is None:
                        positioned_password[index] = value
                except IndexError:
                    pass
                except ValueError:
                    pass
            else:
                password += m.hexdigest()[5]
        pad_int += 1
    if position_specific:
        return ''.join(positioned_password)
    else:
        return password


def test():
    assert find_password('abc', 3) == '18f'
    assert find_password('abc', 3, True) == '05a'
    logger.info('Tests passed')


def main():

    input = get_input()

    logger.info('Result 1: %s' % find_password(input))
    logger.info('Result 2: %s' % find_password(input, position_specific=True))


if __name__ == '__main__':

    test()
    main()
