with open('2.txt', 'r') as f:
    gifts = f.read()


gs = gifts.split('\n')

int_gifts = []


for g in gs[1:-1]:
    sides = g.split('x')
    l = int(sides[0])
    w = int(sides[1])
    h = int(sides[2])
    int_gifts.append(sorted([l, w, h]))

total = 0
tot_ribbon = 0

for g in int_gifts:

    tot_ribbon = tot_ribbon + 2*g[0] + 2*g[1] + g[0]*g[1]*g[2]

    total = total + 2*g[0]*g[1] + 2*g[1]*g[2] + 2*g[0]*g[2] + g[0]*g[1]

print total
print tot_ribbon
