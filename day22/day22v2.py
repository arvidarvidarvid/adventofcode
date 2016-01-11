from copy import deepcopy


class Battle(object):

    ACTIONS = ['R', 'S', 'P', 'D', 'M']

    def __init__(self, init_state, difficulty='normal'):
        self.init_state = init_state
        self.init_state['difficulty'] = difficulty
        self.max_mana_spend = 2000
        self.state_memo = dict()
        self.winning_attack_sequences = list()

    def get_min_mana(self):
        least_spend = min([get_mana_spent_for_win(
            self, self.init_state, a) for a in self.ACTIONS])
        return (least_spend,
                sorted(self.winning_attack_sequences, key=lambda x: x[1]))


def serialize_state(state):
    return u''.join([
        unicode(state['player']['health']),
        unicode(state['player']['mana']),
        unicode(state['boss']['health']),
        unicode(state['recharge_charges']),
        unicode(state['shield_turns']),
        unicode(state['poison_charges']),
        unicode(state['mana_spent'])
        ])


def get_mana_spent_for_win(battle, state, next_action):

    serialized_state = serialize_state(state)
    if serialized_state in battle.state_memo:
        return battle.state_memo[serialized_state]

    _state = deepcopy(state)

    if _state['mana_spent'] > battle.max_mana_spend:
        return 99999

    # PLAYER TURN

    if _state['difficulty'] == 'hard':
        _state['player']['health'] -= 1
        if _state['player']['health'] < 1:
            return 99999

    # Effects

    if _state['recharge_charges'] > 0:
        _state['player']['mana'] += 101
        _state['recharge_charges'] -= 1

    if _state['poison_charges'] > 0:
        _state['boss']['health'] -= 3
        _state['poison_charges'] -= 1

    if _state['shield_turns'] > 0:
        _state['shield_turns'] -= 1

    # Player Action

    _state['attack_sequence'] += next_action

    if next_action == 'R':
        if _state['recharge_charges'] > 0 or _state['player']['mana'] < 229:
            return 99999
        else:
            _state['player']['mana'] -= 229
            _state['mana_spent'] += 229
            _state['recharge_charges'] = 5
    elif next_action == 'S':
        if _state['shield_turns'] > 0 or _state['player']['mana'] < 113:
            return 99999
        else:
            _state['player']['mana'] -= 113
            _state['mana_spent'] += 113
            _state['shield_turns'] = 6
    elif next_action == 'P':
        if _state['poison_charges'] > 0 or _state['player']['mana'] < 173:
            return 99999
        else:
            _state['player']['mana'] -= 173
            _state['mana_spent'] += 173
            _state['poison_charges'] = 6
    elif next_action == 'D':
        if _state['player']['mana'] < 73:
            return 99999
        else:
            _state['player']['mana'] -= 73
            _state['mana_spent'] += 73
            _state['player']['health'] += 2
            _state['boss']['health'] -= 2
    elif next_action == 'M':
        if _state['player']['mana'] < 53:
            return 99999
        else:
            _state['player']['mana'] -= 53
            _state['mana_spent'] += 53
            _state['boss']['health'] -= 4

    # Check for boss death

    if _state['boss']['health'] < 1:
        if battle.max_mana_spend > _state['mana_spent']:
            battle.max_mana_spend = _state['mana_spent']
        battle.winning_attack_sequences.append(
            (_state['attack_sequence'], _state['mana_spent']))
        return _state['mana_spent']

    # BOSS TURN

    # Effects

    shield_this_turn = False

    if _state['recharge_charges'] > 0:
        _state['player']['mana'] += 101
        _state['recharge_charges'] -= 1

    if _state['poison_charges'] > 0:
        _state['boss']['health'] -= 3
        _state['poison_charges'] -= 1

    if _state['shield_turns'] > 0:
        shield_this_turn = True
        _state['shield_turns'] -= 1

    # Check for boss death

    if _state['boss']['health'] < 1:
        if battle.max_mana_spend > _state['mana_spent']:
            battle.max_mana_spend = _state['mana_spent']
        battle.winning_attack_sequences.append(
            (_state['attack_sequence'], _state['mana_spent']))
        return _state['mana_spent']

    # Boss Action

    if shield_this_turn:
        _state['player']['health'] -= max([(_state['boss']['damage'] - 7), 1])
    else:
        _state['player']['health'] -= max([(_state['boss']['damage']), 1])

    # Check for player death

    if _state['player']['health'] < 1:
        return 99999
    else:
        least_spend = min([get_mana_spent_for_win(
            battle, _state, a)
            for a in battle.ACTIONS])
        new_serialized_state = serialize_state(_state)
        battle.state_memo[new_serialized_state] = least_spend
        return least_spend


init_state = {
    'player': {
        'health': 50,
        'damage': 0,
        'mana': 500},
    'boss': {
        'health': 71,
        'damage': 10,
        'mana': 0},
    'recharge_charges': 0,
    'shield_turns': 0,
    'poison_charges': 0,
    'mana_spent': 0,
    'attack_sequence': ''
}

p1_battle = Battle(init_state, difficulty='normal')
part1 = p1_battle.get_min_mana()
print ('Part 1: The least amount of mana that can beat the boss on normal ' +
       'difficulty is %s with the sequence %s' % (part1[0], part1[1][0][0]))

p2_battle = Battle(init_state, difficulty='hard')
part2 = p2_battle.get_min_mana()
print ('Part 1: The least amount of mana that can beat the boss on hard ' +
       'difficulty is %s with the sequence %s' % (part2[0], part2[1][0][0]))
