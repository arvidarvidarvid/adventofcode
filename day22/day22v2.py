from copy import deepcopy

MAX_MANA_SPEND = 2000
ROUNDS = 0
actions = ['R', 'S', 'P', 'D', 'M']
state_memo = {}


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


def get_min_mana(init_state, difficulty_hard=False):
    global MAX_MANA_SPEND
    MAX_MANA_SPEND = 2000
    state = init_state
    if difficulty_hard is True:
        state['difficulty'] = 'hard'
    else:
        state['difficulty'] = 'normal'
    return min([get_mana_spent_for_win(init_state, a) for a in actions])


def get_mana_spent_for_win(state, next_action):

    global MAX_MANA_SPEND

    serialized_state = serialize_state(state)
    if serialized_state in state_memo:
        return state_memo[serialized_state]

    _state = deepcopy(state)

    if _state['mana_spent'] > MAX_MANA_SPEND:
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
        if MAX_MANA_SPEND > _state['mana_spent']:
            MAX_MANA_SPEND = _state['mana_spent']
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
        if MAX_MANA_SPEND > _state['mana_spent']:
            MAX_MANA_SPEND = _state['mana_spent']
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
        best_spend = min([get_mana_spent_for_win(_state, a) for a in actions])
        new_serialized_state = serialize_state(_state)
        state_memo[new_serialized_state] = best_spend
        return best_spend


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

print ('Part 1: The least amount of mana that can beat the boss on normal ' +
       'difficulty is %s ' % get_min_mana(init_state, difficulty_hard=False))

print ('Part 2: The least amount of mana that can beat the boss on hard ' +
       'difficulty is %s ' % get_min_mana(init_state, difficulty_hard=True))
