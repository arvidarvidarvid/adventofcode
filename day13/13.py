import re
from itertools import permutations


def setup_pref_dict(raw_preferences):
    pref_dict = dict()
    for p in raw_preferences.split('\n'):
        m = re.match(r'(\w+) would (\w+) (\d+) .* (\w+)\.', p)
        n1, n2, effect, scale = m.group(1), m.group(4), m.group(2), m.group(3)
        if n1 not in pref_dict:
            pref_dict[n1] = dict()
        if effect == 'gain':
            pref_dict[n1][n2] = int(scale)
        elif effect == 'lose':
            pref_dict[n1][n2] = -int(scale)
    return pref_dict


def get_comb_value(arr, pref_dict):
    _value = 0
    for i in range(-1, len(arr)-1):
        _value += pref_dict[arr[i]][arr[i+1]] + pref_dict[arr[i+1]][arr[i]]
    return _value


def add_arvid(pref_dict):
    for k, v in pref_dict.items():
        v['Arvid'] = 0
    pref_dict['Arvid'] = {k: 0 for k in pref_dict.keys()}
    return pref_dict


def get_happiest_arrangement(pref_dict):
    visitors = pref_dict.keys()
    possible_arrangements = permutations(visitors, len(visitors))
    best_value = 0
    for arr in possible_arrangements:
        _value = get_comb_value(list(arr), pref_dict)
        if _value > best_value:
            best_value = _value
    return best_value


raw_preferences = open('13.txt', 'r').read()

pref_dict = setup_pref_dict(raw_preferences)
print ('Step 1, happiest combination scores: %s' %
       get_happiest_arrangement(pref_dict))
pref_dict = add_arvid(pref_dict)
print ('Step 2, happiest combination including me scores: %s' %
       get_happiest_arrangement(pref_dict))
