import re

raw_props = open('14.txt', 'r').read()


class Reindeer(object):
    def __init__(self, name, speed, endurance, rest):
        self.name = name
        self.speed = int(speed)
        self.endurance = int(endurance)
        self.rest = int(rest)
        self.travel_func = ([self.speed for i in range(0, self.endurance)] +
                            [0 for i in range(0, self.rest)])
        self.race_score = 0

    def __unicode__(self):
        return unicode(self.name)

    def get_distance_at_time(self, time):
        while time > len(self.travel_func):
            self.travel_func = self.travel_func + self.travel_func
        return sum(self.travel_func[:time])


def import_reindeer(raw_props):
    reindeer = []
    p = re.compile(r'(\w+) .* (\d+) .* (\d+) .* (\d+) \w+.')
    for l in raw_props.split('\n'):
        m = re.match(p, l)
        name, speed, endurance, rest = (m.group(1), m.group(2), m.group(3),
                                        m.group(4))
        reindeer.append(Reindeer(name, speed, endurance, rest))
    return reindeer


def distance_race(reindeer, time):
    best_distance, best_deer = None, None
    for r in reindeer:
        d = r.get_distance_at_time(time)
        if d > best_distance or best_distance is None:
            best_distance, best_deer = d, r
    return (best_deer, best_distance)


def points_race(reindeer, time):
    for r in reindeer:
        r.race_score = 0
    for t in range(1, time):
        _c_best_deer, _c_best_dist = None, 0
        for r in reindeer:
            _c_dist = r.get_distance_at_time(t)
            if _c_dist > _c_best_dist:
                _c_best_dist, _c_best_deer = _c_dist, r
        _c_best_deer.race_score += 1
    winner, best_score = None, 0
    for r in reindeer:
        if r.race_score > best_score:
            best_score, winner = r.race_score, r
    return (winner, winner.race_score)


reindeer = import_reindeer(raw_props)

winner = distance_race(reindeer, 2503)
print u'%s: %s' % (winner[0], winner[1])

winner = points_race(reindeer, 2503)
print u'%s: %s' % (winner[0], winner[1])
