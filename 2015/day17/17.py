from itertools import combinations

containers = [int(c) for c in open('17.txt', 'r').read().split('\n')]

combs = dict()
tot_combs = 0

for i in range(1, len(containers)+1):
    for c in combinations(containers, i):
        if sum(list(c)) == 150:
            if i not in combs:
                combs[i] = 0
            combs[i] += 1
            tot_combs += 1

print tot_combs
print combs
