import re
from itertools import permutations

raw_preferences = open('13.txt', 'r').read()

pref_dict = dict()
for p in raw_preferences.split('\n'):
    patt = r'(\w+) would (\w+) (\d+) happiness units by sitting next to (\w+).'
    m = re.match(patt, p)
    n1 = m.group(1)
    n2 = m.group(4)
    effect = m.group(2)
    scale = m.group(3)

    if n1 not in pref_dict:
        pref_dict[n1] = dict()
    if effect == 'gain':
        pref_dict[n1][n2] = int(scale)
    elif effect == 'lose':
        pref_dict[n1][n2] = -int(scale)

visitors = pref_dict.keys()

# Additional stuff for step 2
for k, v in pref_dict.items():
    v['Arvid'] = 0
pref_dict['Arvid'] = {k: 0 for k in visitors}
visitors.append('Arvid')
# End additional stuff

possible_arrangements = permutations(visitors, len(visitors))


def get_comb_value(arr, pref_dict):
    _value = 0
    for i in range(-1, len(arr)):
        try:
            _value += pref_dict[arr[i]][arr[i+1]] + pref_dict[arr[i+1]][arr[i]]
        except IndexError:
            pass
    return _value

best_value = 0
for arr in possible_arrangements:
    _value = get_comb_value(list(arr), pref_dict)
    if _value > best_value:
        best_value = _value

print best_value
