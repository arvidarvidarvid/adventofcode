# encoding=utf8

data = open('12.txt', 'r').read()

data = eval(data)


# Part one

def get_leaves(data):
    if isinstance(data, dict):
        return sum([get_leaves(v) for k, v in data.items()])
    elif isinstance(data, list):
        return sum([get_leaves(i) for i in data])
    elif isinstance(data, int):
        return data
    else:
        return 0

print 'Part 1: %s' % get_leaves(data)


# Part two

def get_leaves_v2(data):
    if isinstance(data, dict):
        _sum = 0
        for k, v in data.items():
            if 'red' in (k, v):
                return 0
            else:
                _sum += get_leaves_v2(v)
        return _sum
    elif isinstance(data, list):
        return sum([get_leaves_v2(i) for i in data])
    elif isinstance(data, int):
        return data
    else:
        return 0

print 'Part 2: %s' % get_leaves_v2(data)
