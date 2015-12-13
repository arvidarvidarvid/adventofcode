# encoding=utf8


def get_leaves(data, care_about_red=False):
    if isinstance(data, dict):
        _sum = 0
        for k, v in data.items():
            if care_about_red:
                if 'red' in (k, v):
                    return 0
            _sum += get_leaves(v, care_about_red)
        return _sum
    elif isinstance(data, list):
        return sum([get_leaves(i, care_about_red) for i in data])
    elif isinstance(data, int):
        return data
    else:
        return 0


data = eval(open('12.txt', 'r').read())
print 'Part 1: %s' % get_leaves(data, False)
print 'Part 2: %s' % get_leaves(data, True)
