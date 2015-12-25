import math
import logging
import re

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class Actor(object):

    def __init__(self, name, health, damage, armor, mana):
        self.name = name
        self.initial_health = int(health)
        self.health = int(health)
        self.damage = int(damage)
        self.armor = int(armor)
        self.mana = int(mana)
        self.mana_spent = 0
        self.ongoing_battle = None

    def __unicode__(self):
        if self.ongoing_battle is not None:
            return '%s: (%s (-%s) hp, %s dmg, %s arm, %s mp)' % (
                unicode(self.name), self.health,
                self.incoming_damage(self.ongoing_battle, 10), self.damage,
                self.get_armor(self.ongoing_battle), self.mana)
        else:
            return '%s: (%s hp, %s dmg, %s arm, %s mp)' % (
                unicode(self.name), self.health, self.damage, self.armor,
                self.mana)

    def mana_to_spend(self, battle):
        recharge_cost = 229

        e = battle.effect_is_active('Recharge', self)
        if e is not False:
            mana_to_come = 101 * e.duration
        else:
            mana_to_come = 0
        tot_mana = self.mana + mana_to_come

        # Need to be able to cast a future recharge
        mts = min([tot_mana - recharge_cost, self.mana])
        return mts

    def spend_mana(self, amount):
        if self.mana >= amount:
            self.mana -= amount
            self.mana_spent += amount
            return True
        else:
            return False

    def incoming_damage(self, battle, turns):
        e = battle.effect_is_active('Poison', self)
        if e is not False:
            return 3 * min([turns, e.duration])
        else:
            return 0

    def get_armor(self, battle, at_future_turn=None):
        e = battle.effect_is_active('Shield', self)
        if e is not False:
            if at_future_turn is None:
                return self.armor + 7
            else:
                if e.duration >= at_future_turn:
                    return self.armor + 7
                else:
                    return self.armor
        return self.armor

    def attack(self, battle):
        o = [r for r in battle.remaining_actors if r != self][0]  # Opponent

        if self.damage > 0:
            damage = max([0, self.damage - o.get_armor(battle)])
            o.health -= damage
            logger.debug(u'%s deals %s damage to %s' % (
                  unicode(self), damage, unicode(o)))

        elif self.mana > 0:

            logger.debug(u'Deciding what to do to %s' % o)

            # Try to finish the boss quickly in the late game with a series of
            # magic missiles

            conseq_mms_to_win = int(math.ceil((o.health - o.incoming_damage(
                battle, 6))/4))
            incoming_damage_during_conseq_mms = (
                conseq_mms_to_win * o.damage - sum([self.get_armor(battle, i)
                                                    for i in xrange(
                                                        conseq_mms_to_win)
                                                    if i % 2 != 0]))

            if (self.mana >= (conseq_mms_to_win * 53) and
                    self.health > incoming_damage_during_conseq_mms):
                logger.debug('Trying to finish off with %s magic missiles' %
                             (int(conseq_mms_to_win)+1))
                self.cast_magic_missile(battle, o)

            # Quickest way to do damage over 1 turn:
            elif (self.mana >= 53 and o.health <= (
                    4 + o.incoming_damage(battle, 1))):
                logger.debug('Trying to finish boss off with a magic missile')
                self.cast_magic_missile(battle, o)

            # Quickest way to do damage over 2 turns:
            elif (self.mana >= 106 and o.health <= (
                    8 + o.incoming_damage(battle, 3)) and
                    (self.health + self.get_armor(battle, 2) > 9)):
                logger.debug('Trying to finish boss off in two turns with' +
                             ' two magic missiles')
                self.cast_magic_missile(battle, o)
            elif (self.mana >= 126 and o.health <= (
                    6 + o.incoming_damage(battle, 3)) and
                    (self.health + self.get_armor(battle, 2) > 7)):
                logger.debug('Trying to finish boss off in two turns with' +
                             ' a drain and a magic missile')
                self.cast_drain(battle, o)

            # Normal endless game optimal strategy

            elif (self.mana_to_spend(battle) < 173 and
                    battle.effect_is_active('Recharge', self) is False):
                self.cast_recharge(battle, o)
            elif (self.mana_to_spend(battle) >= 113 and
                    battle.effect_is_active('Shield', self) is False):
                self.cast_shield(battle, o)
            elif (self.mana_to_spend(battle) >= 173 and
                    battle.effect_is_active('Poison', o) is False):
                self.cast_poison(battle, o)
            elif (self.mana_to_spend(battle) >= 73 and
                    self.health < (9 - self.get_armor(battle))):
                self.cast_drain(battle, o)
            elif self.mana_to_spend(battle) >= 53:
                self.cast_magic_missile(battle, o)
            else:
                battle.winner = o
                logger.info(unicode(self) +
                            ' can make no action and has lost.')
        else:
            logger.warning(unicode(self) + u' has no attack resources!')

    def cast_magic_missile(self, battle, opponent):
        # Cast Magic Missile (53 mana, 4 damage) (13,25 MPD, 4 DPT)
        if self.spend_mana(53):
            logger.debug(unicode(self) + ' casts magic missile')
            opponent.health -= 4
            return True
        else:
            logger.debug(unicode(self) + ' tries to cast magic missile but' +
                         ' fails!')
            return False

    def cast_recharge(self, battle, opponent):
        # Cast Effect:Recharge (229 mana, 5 turns, gain 101 mana)
        if self.spend_mana(229):
            logger.debug(unicode(self) + ' casts recharge')
            e = Effect('Recharge', self, 5, 0, 101)
            battle.effects.append(e)
            return True
        else:
            logger.debug(unicode(self) + ' tries to cast recharge but fails!')
            return False

    def cast_drain(self, battle, opponent):
        # Cast Drain (73 mana, 2 damage, 2 health to self) (36,5 MPD, 2 DPT)
        if self.spend_mana(73):
            logger.debug(unicode(self) + ' casts drain')
            self.health += 2
            opponent.health -= 2
            return True
        else:
            logger.debug(unicode(self) + ' tries to cast drain but fails!')
            return False

    def cast_shield(self, battle, opponent):
        # Cast Effect:Shield (113 mana, 6 turns, armor increased by 7)
        if self.spend_mana(113):
            logger.debug(unicode(self) + ' casts shield')
            e = Effect('Shield', self, 6, 0, 0)
            battle.effects.append(e)
            return True
        else:
            logger.debug(unicode(self) + ' tries to cast shield but fails!')
            return False

    def cast_poison(self, battle, opponent):
        # Cast Effect:Poison (173, 6 turns, 3 damage) (9,61 MPD, 3 DPT)
        if self.spend_mana(173):
            logger.debug(unicode(self) + ' casts poison')
            e = Effect('Poison', opponent, 6, -3, 0)
            battle.effects.append(e)
            return True
        else:
            logger.debug(unicode(self) + ' tries to cast poison but fails!')
            return False

    def reset(self):
        self.health = self.initial_health


class Effect(object):

    def __init__(self, name, target, duration, delta_health, delta_mana):
        self.name = name
        self.target = target
        self.duration = duration
        self.delta_health = delta_health
        self.delta_mana = delta_mana

    def __unicode__(self):
        return self.name

    def tick(self):
        if self.delta_health != 0:
            logger.debug(self.name + ' ticks and ' + unicode(self.target) +
                         ' takes ' + unicode(self.delta_health) + ' damage.')
            self.target.health += self.delta_health
        if self.delta_mana != 0:
            logger.debug(self.name + ' ticks and ' + unicode(self.target) +
                         ' gains ' + unicode(self.delta_mana) + ' mana.')
            self.target.mana += self.delta_mana
        self.duration -= 1


class Battle(object):

    def __init__(self, actors):
        self.actors = actors
        self.remaining_actors = self.actors
        self.effects = []
        self.winner = None
        for a in actors:
            a.ongoing_battle = self

    def check_actors(self):
        for r in self.remaining_actors:
            if r.health < 1:
                logger.info(unicode(r) + u' has died!')
                self.remaining_actors.remove(r)
        if len(self.remaining_actors) > 1:
            return True
        else:
            self.winner = self.remaining_actors[0]
            return False

    def apply_effects(self):
        for e in self.effects:
            e.tick()
            if e.duration == 0:
                logger.debug(unicode(e) + u' fades')
                self.effects.remove(e)

    def effect_is_active(self, name, target):
        for e in self.effects:
            if e.target is target and e.name == name:
                return e
        return False

    def to_death(self):

        logger.info(u'Starting a battle')
        logger.info(u'Actors:')
        for a in self.actors:
            logger.info(unicode(a))
        logger.info(u'Turns:')

        self.remaining_actors = self.actors

        while self.winner is None:
            for a in self.remaining_actors:
                self.apply_effects()     # Apply all active effects
                if self.check_actors():  # See if someone died from effects
                    a.attack(self)       # Attack if still alive
                self.check_actors()      # See if someone died from attacks

        logger.info(u'Winner: %s, mana spent: %s' % (
            unicode(self.winner), unicode(self.winner.mana_spent)))
        logger.info(u'Battle ended.')

        return {'winner': self.winner}


def get_actor_from_file(filename, name):
    f = open(filename, 'r').read().split('\n')
    health = re.search(r'(\d+)', f[0]).group(1)
    damage = re.search(r'(\d+)', f[1]).group(1)
    return Actor(name, health, damage, 0, 0)


def testcase_melee():
    player = Actor('Player', 8, 5, 5, 0)
    boss = Actor('Boss', 12, 7, 2, 0)
    battle = Battle([player, boss])
    return battle.to_death()


def testcase_spellcasting():
    player = Actor('Player', 50, 0, 0, 500)
    boss = get_actor_from_file('day22input.txt', 'Boss')
    battle = Battle([player, boss])
    return battle.to_death()


# print testcase_melee()
print testcase_spellcasting()
