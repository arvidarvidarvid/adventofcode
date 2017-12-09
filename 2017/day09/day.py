import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]


def score_line(line, return_garbage_length=False):
    line = apply_cancels(line)
    line, garbage_length = clean_garbage(line)
    while len(line) != len(clean_stray_commas(line)):
        line = clean_stray_commas(line)
    line = line.replace('{', '[').replace('}', ']')
    list_struct = eval(line)
    score = calculate_score(list_struct)
    if return_garbage_length:
        return score, garbage_length
    else:
        return score


def apply_cancels(line):
    while len(line) > len(re.sub(r'(<.*?)!.(.*?[^!]>)', r'\1\2', line)):
        line = re.sub(r'(<.*?)!.(.*?[^!]>)', r'\1\2', line)
    return line.replace('!!', '')


def clean_garbage(line):
    garbage = re.findall(r'<(.*?)>', line)
    garbage_length = sum([len(g) for g in garbage])
    line = re.sub(r'(<.*?>)', '', line)
    return line, garbage_length


def clean_stray_commas(line):
    line = re.sub(r'(\{),*?(\})', r'\1\2', line)
    line = line.replace(r'},}', r'}}')
    line = line.replace(r'{,{', r'{{')
    return line


def calculate_score(list_struct, level=1):
    sub_values = []
    for l in list_struct:
        sub_values.append(calculate_score(l, level=level + 1))
    return level + sum(sub_values)


def test():
    test_input = get_input('test.input')
    assert score_line(test_input[0]) == 1
    assert score_line(test_input[1]) == 6
    assert score_line(test_input[2]) == 5
    assert score_line(test_input[3]) == 16
    assert score_line(test_input[4]) == 1
    assert score_line(test_input[5]) == 9
    assert score_line(test_input[6]) == 9
    assert score_line(test_input[7]) == 3
    logger.info('Tests passed')


def main():

    input = get_input()

    score, garbage_length = score_line(input[0], return_garbage_length=True)

    logger.info('Result 1: %s' % score)
    logger.info('Result 2: %s' % garbage_length)


if __name__ == '__main__':
    test()
    main()
