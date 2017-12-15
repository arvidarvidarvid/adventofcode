def first_safe_delay(scanners):
    for i in range(0, 100000000):
        if check_val(i, scanners, True):
            return i


def check_val(i, scanners, merciless=False):
    severity = 0
    for s in scanners:
        if (i + s[0]) % s[1] == 0:
            if merciless:
                return False
            else:

    return True


input = [list(map(int, line.split(': ')))
         for line in open('day.input').readlines()]
scanners = [(s[0] % (s[1] * 2 - 2), s[1] * 2 - 2) for s in input]

print('Result 1: %s' % check_val(0, scanners))
print('Result 2: %s' % first_safe_delay(scanners))
