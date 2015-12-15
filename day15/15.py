import re
from itertools import combinations_with_replacement


class Cupboard(object):
    def __init__(self):
        self.ingredients = list()
        self.best_score = 0
        self.best_mix = None

    def stack_shelves(self, filename):
        raw_ingredients = open(filename, 'r').read().split('\n')
        for i in raw_ingredients:
            name = re.match(r'(\w+):', i).group(1)
            cap, dur, fla, tex, cal = re.findall('-*\d+', i)
            ingredient = Ingredient(name, cap, dur, fla, tex, cal)
            self.ingredients.append(ingredient)
        return self.ingredients

    def find_best_mix(self):
        all_weights = list(combinations_with_replacement(
            range(0, 101), len(self.ingredients)))
        for w in all_weights:
            if sum(w) == 100:
                score = self.score_mix(w)
                if score > self.best_score:
                    self.best_score, self.best_mix = score, w
        return (self.best_score, self.best_mix)

    def score_mix(self, weights):
        _cap, _dur, _fla, _tex, _cal = 0, 0, 0, 0, 0
        for i, w in zip(self.ingredients, weights):
            _cap += i.capacity * w
            _dur += i.durability * w
            _fla += i.flavor * w
            _tex += i.texture * w
            _cal += i.calories * w
        return (max([0, _cap]) * max([0, _dur]) * max([0, _fla]) *
                max([0, _tex]) * max([0, 1]))


class Ingredient(object):
    def __init__(self, name, cap, dur, fla, tex, cal):
        self.name = name
        self.capacity = int(cap)
        self.durability = int(dur)
        self.flavor = int(fla)
        self.texture = int(tex)
        self.calories = int(cal)

    def __unicode__(self):
        return u'%s: %i %i %i %i %i' % (
            self.name, self.capacity, self.durability, self.flavor,
            self.texture, self.calories)


def main():
    cupboard = Cupboard()
    cupboard.stack_shelves('15.txt')
    for i in cupboard.ingredients:
        print unicode(i)
    print cupboard.find_best_mix()

if __name__ == "__main__":
    main()
