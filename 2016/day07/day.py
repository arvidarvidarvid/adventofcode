import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input():
    with open('day.input', 'r') as file:
        return [line.strip() for line in file.readlines()]


def string_is(string, format='abba'):
    if format == 'abba':
        if len(string) == 4:
            return (string[0] == string[3] and
                    string[1] == string[2] and
                    string[0] != string[1])
    elif format == 'aba':
        if len(string) == 3:
            return (string[0] == string[2] and
                    string[0] != string[1])


def sequence_contains_abba(sequence, return_all=False, format='abba'):
    return_set = []
    if return_all:
        seq_len = 3
    else:
        seq_len = 4
    if len(sequence) < seq_len:
        return False
    if len(sequence) == seq_len:
        if string_is(sequence, format):
            if return_all:
                if string_is(sequence, format):
                    return_set.append(sequence)
            else:
                return string_is(sequence, format)
    if len(sequence) > seq_len:
        for offset in range(0, len(sequence) - (seq_len - 1)):
            test_string = sequence[offset:][:seq_len]
            if string_is(sequence[offset:][:seq_len], format):
                if return_all:
                    return_set.append(test_string)
                else:
                    return True
    if return_all:
        return return_set
    return False


def supports_tls(ip, ssl=False):

    sequences = []
    hypersequences = []

    current_buffer = ''
    current_buffer_type = 'SEQUENCE'
    for index, char in enumerate(ip):
        if current_buffer_type == 'SEQUENCE':
            if char != '[':
                current_buffer += char
                if len(ip) == index + 1:
                    sequences.append(current_buffer)
            else:
                sequences.append(current_buffer)
                current_buffer_type = 'HYPERSEQUENCE'
                current_buffer = ''
        elif current_buffer_type == 'HYPERSEQUENCE':
            if char != ']':
                current_buffer += char
            else:
                hypersequences.append(current_buffer)
                current_buffer_type = 'SEQUENCE'
                current_buffer = ''

    if ssl:

        abas = []
        babs = []

        for hs in hypersequences:
            abas += sequence_contains_abba(hs, True, 'aba')

        for s in sequences:
            babs += sequence_contains_abba(s, True, 'aba')

        for a in abas:
            for b in babs:
                if a[0] == b[1] and a[1] == b[0]:
                    return True

    else:

        for hs in hypersequences:
            if sequence_contains_abba(hs):
                return False

        for s in sequences:
            if sequence_contains_abba(s):
                return True

    return False


def supports_ssl(ip):
    return supports_tls(ip, True)


def test():
    assert supports_tls('abba[mnop]qrst') is True
    assert supports_tls('abcd[bddb]xyyx') is False
    assert supports_tls('aaaa[qwer]tyui') is False
    assert supports_tls('ioxxoj[asdfgh]zxcvbn') is True

    assert supports_ssl('aba[bab]xyz') is True
    assert supports_ssl('xyx[xyx]xyx') is False
    assert supports_ssl('aaa[kek]eke') is True
    assert supports_ssl('zazbz[bzb]cdb') is True

    logger.info('Tests passed')


def main():

    input = get_input()

    logger.info('Result 1: %s' % sum([1 for ip in input if supports_tls(ip)]))
    logger.info('Result 2: %s' % sum([1 for ip in input if supports_ssl(ip)]))


if __name__ == '__main__':
    test()
    main()
