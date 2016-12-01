from random import shuffle

raw_replacements = open('19replacements.txt', 'r').read().split('\n')
raw_string = open('19string.txt', 'r').read()

replacements = {}
for l in raw_replacements:
    k, v = l.split(' => ')
    if k in replacements:
        replacements[k].append(v)
    else:
        replacements[k] = [v]


def get_replaced_strings(string, reverse=False):
    strings = []
    i = 0
    while i < len(string):
        k = None
        if string[i] in replacements:
            k = string[i]
        elif len(string)-1 > i:
            for j in range(0, 11):
                if string[i:i+j+1] in replacements:
                    k = string[i:i+j+1]
        if k is not None:
            for r in replacements[k]:
                strings.append(string[:i] + r + string[i+len(k):])
        i += 1
    return set(strings)


reversed_replacements = []
for k, v in replacements.items():
    for w in v:
        reversed_replacements.append((w, k))
reversed_replacements = sorted(reversed_replacements, key=lambda x: len(x[0]),
                               reverse=True)


def get_molecule_reversion(target_string, string='e'):

    iterations = 0
    target = target_string

    while target != string:
        comp_string = target

        for fro, to in reversed_replacements:
            if fro not in target:
                continue

            target = target.replace(fro, to, 1)
            iterations += 1

        if comp_string == target:
            iterations = 0
            target = target_string
            shuffle(reversed_replacements)

    return iterations


print ('Part 1: There are %s possible combinations' %
       len(get_replaced_strings(raw_string)))

print ('Part 2: The target molecule is generated after %s iterations' %
       get_molecule_reversion(raw_string))
