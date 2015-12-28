from itertools import combinations
from tqdm import tqdm
import numpy as np


def get_groups(packages, number_of_groups):

    valid_combinations = []

    groups = []
    for i in range(1, len(packages)/number_of_groups-1):
        combs = combinations(packages, i)
        for c in combs:
            if sum(c) == sum(packages)/number_of_groups:
                groups.append(c)

    for g in tqdm(groups):
        rem = set(packages) - set(g)
        base_length = len(rem)/number_of_groups
        r_combs = list(combinations(rem, base_length-1))
        r_combs += list(combinations(rem, base_length))
        r_combs += list(combinations(rem, base_length+1))
        clean_r_combs = [r for r in r_combs
                         if sum(r) == sum(packages)/number_of_groups]
        for r in clean_r_combs:
            if number_of_groups == 3:
                g1 = g
                g2 = r
                g3 = set(packages) - set(g) - set(r)
                valid_combinations.append((g1, g2, g3))
                break
            elif number_of_groups == 4:
                for c in clean_r_combs:
                    if not any(i in c for i in r):
                        g1 = g
                        g2 = r
                        g3 = c
                        g4 = set(packages) - set(g) - set(r) - set(c)
                        valid_combinations.append((g1, g2, g3, g4))
                        break

    return valid_combinations


def find_smalles_qe(valid_combinations):
    min_qe = None
    for c in valid_combinations:
        _qe = np.prod(c[0])
        if _qe < min_qe or min_qe is None:
            min_qe = _qe
    return min_qe

raw_packages = open('day24input.txt', 'r').read().split('\n')
packages = [int(p) for p in raw_packages]

part1_valid_combinations = get_groups(packages, 3)
print (u'Part 1: The smallest QE possible with three bags is %s' %
       find_smalles_qe(part1_valid_combinations))

part2_valid_combinations = get_groups(packages, 4)
print (u'Part 2: The smallest QE possible with four bags is %s' %
       find_smalles_qe(part2_valid_combinations))
