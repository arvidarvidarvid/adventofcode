import re

FUNCS = dict()


def init_funcs():
    global FUNCS
    with open('7.txt', 'r') as f:
        for i in f.read().split('\n'):
            instr = i.split(' -> ')
            FUNCS[instr[1]] = [instr[0], None]


def _not(i):
    return 0xffff - int(get_value(i))


def _and(i1, i2):
    return int(get_value(i1)) & int(get_value(i2))


def _rshift(i, s):
    return int(get_value(i)) >> int(s)


def _lshift(i, s):
    return int(get_value(i)) << int(s)


def _or(i1, i2):
    return int(get_value(i1)) | int(get_value(i2))


def string_to_result(s, key):

    direct_p = re.match(r'^([a-z]{1,2}|\d+)$', s)
    not_p = re.match(r'^NOT ([a-z]{1,2}|\d+)$', s)
    and_p = re.match(r'^([a-z]{1,2}|\d+) AND ([a-z]{1,2}|\d+)$', s)
    or_p = re.match(r'^([a-z]{1,2}|\d+) OR ([a-z]{1,2}|\d+)$', s)
    rshift_p = re.match(r'^([a-z]{1,2}|\d+) RSHIFT (\d{1,2})$', s)
    lshift_p = re.match(r'^([a-z]{1,2}|\d+) LSHIFT (\d{1,2})$', s)

    if direct_p is not None:
        res = get_value(direct_p.group(1))
    elif not_p is not None:
        res = _not(not_p.group(1))
    elif and_p is not None:
        res = _and(and_p.group(1), and_p.group(2))
    elif or_p is not None:
        res = _or(or_p.group(1), or_p.group(2))
    elif rshift_p is not None:
        res = _rshift(rshift_p.group(1), rshift_p.group(2))
    elif lshift_p is not None:
        res = _lshift(lshift_p.group(1), lshift_p.group(2))
    else:
        raise Exception('Failed to match to function.')

    FUNCS[key][1] = res
    return res


def get_value(key):
    if re.match(r'^\d+$', key):
        return key
    elif FUNCS[key][1] is not None:
        return FUNCS[key][1]
    else:
        return string_to_result(FUNCS[key][0], key)


init_funcs()
first_result = get_value('a')
print 'Part one result: %s' % first_result

init_funcs()
FUNCS['b'] = [unicode(first_result), None]
second_result = get_value('a')
print 'Part two result: %s' % second_result
