def first_safe_delay(input):
    scanners = [(s[0] % (s[1] * 2 - 2), s[1] * 2 - 2) for s in input]
    for i in range(0, 100000000):
        if check_val(i, scanners):
            return i


def check_val(i, scanners):
    for s in scanners:
        if (i + s[0]) % s[1] == 0:
            return False
    return True


print('Result 2: %s' % first_safe_delay(
    [list(map(int, line.split(': ')))
     for line in open('day.input').readlines()]))
