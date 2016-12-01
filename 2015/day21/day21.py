import re


def get_shop(filename):
    shop_sections = open(filename, 'r').read().split('\n\n')
    shop = dict()
    for section in shop_sections:
        lines = section.split('\n')
        section_name = (lines[0].split()[0])[:-1].lower()
        shop[section_name] = dict()
        for item in lines[1:]:
            name, c, d, a = re.match(
                r'([A-Za-z 0-9+]+) [ ]*(\d+).*(\d+).*(\d+)', item).groups()
            shop[section_name][name.strip()] = {
                'cost': int(c), 'damage': int(d), 'armor': int(a)}
    return shop


class Actor(object):

    def __init__(self, name, health, damage, armor):
        self.name = name
        self.initial_health = int(health)
        self.health = int(health)
        self.damage = int(damage)
        self.armor = int(armor)

    def __unicode__(self):
        return '%s: (%s %s %s)' % (
            unicode(self.name), self.health, self.damage, self.armor)

    def attack(self, opponents, verbose=False):
        for o in opponents:
            damage = max([0, self.damage - o.armor])
            o.health -= damage
            if verbose:
                print u'%s deals %s damage to %s' % (
                      unicode(self), damage, unicode(o))

    def equip(self, equipment):
        self.damage = equipment[1]
        self.armor = equipment[2]

    def reset(self):
        self.health = self.initial_health


def get_actor_from_file(filename, name):
    f = open(filename, 'r').read().split('\n')
    health = re.search(r'(\d+)', f[0]).group(1)
    damage = re.search(r'(\d+)', f[1]).group(1)
    armor = re.search(r'(\d+)', f[2]).group(1)
    return Actor(name, health, damage, armor)


def battle(actors, verbose=False):
    if verbose is True:
        print u"""        ===
        Starting a battle between:
        %s
        %s
        """ % (actors[0], actors[1])
    remaining_actors = actors
    while len(remaining_actors) > 1:
        for a in remaining_actors:
            opponents = [r for r in remaining_actors if r != a]
            a.attack(opponents, verbose)
            for r in remaining_actors:
                if r.health < 1:
                    remaining_actors.remove(r)
    if verbose is True:
        print u'        Winner: %s\n        ===' % remaining_actors[0]
    return {'winner': remaining_actors[0]}


def player_equipment_combinations(shop):
    weapons = [(c['cost'], c['damage'], c['armor'])
               for n, c in shop['weapons'].items()]
    armors = [(c['cost'], c['damage'], c['armor'])
              for n, c in shop['armor'].items()]
    rings = [(c['cost'], c['damage'], c['armor'])
             for n, c in shop['rings'].items()]
    armors.append((0, 0, 0))
    rings.append((0, 0, 0))
    rings.append((0, 0, 0))
    combinations = []
    for w in weapons:
        for a in armors:
            for r1 in rings:
                for r2 in rings:
                    if r2 != r1:
                        tot_c = w[0] + a[0] + r1[0] + r2[0]
                        tot_d = w[1] + a[1] + r1[1] + r2[1]
                        tot_a = w[2] + a[2] + r1[2] + r2[2]
                        combinations.append((tot_c, tot_d, tot_a))
    return sorted(combinations, key=lambda x: x[0])


def testcase():
    player = Actor('Player', 8, 5, 5)
    boss = Actor('Boss', 12, 7, 2)
    battle([player, boss])


def part1(shop):
    player = Actor('Player', 100, 0, 0)
    boss = get_actor_from_file('day21.txt', 'Boss')
    winner = None
    equipment_sets = player_equipment_combinations(shop)
    equipped_index = -1
    while winner != 'Player':
        player.reset()
        boss.reset()
        equipped_index += 1
        player.equip(equipment_sets[equipped_index])
        winner = battle([player, boss])['winner'].name
    return equipment_sets[equipped_index][0]


def part2(shop):
    player = Actor('Player', 100, 0, 0)
    boss = get_actor_from_file('day21.txt', 'Boss')
    winner = None
    equipment_sets = player_equipment_combinations(shop)
    equipped_index = len(equipment_sets)
    while winner != 'Boss':
        player.reset()
        boss.reset()
        equipped_index -= 1
        player.equip(equipment_sets[equipped_index])
        winner = battle([player, boss])['winner'].name
    return equipment_sets[equipped_index][0]


shop = get_shop('day21shop.txt')

print ('Part 1: The least you can spend on gear to beat the boss is %s' %
       part1(shop))
print ("""Part 2: The most expensive set that the shop keeper can trick you
        into buying and still have you lose costs %s""" % part2(shop))
