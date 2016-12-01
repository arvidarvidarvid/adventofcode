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

total_paper = 0
total_ribbon = 0

for g in int_gifts:
    total_ribbon = total_ribbon + 2*g[0] + 2*g[1] + g[0]*g[1]*g[2]
    total_paper = (total_paper + 2*g[0]*g[1] + 2*g[1]*g[2] + 2*g[0]*g[2] +
                   g[0]*g[1])

print 'Part 1: %s sqft of paper needed' % total_paper
print 'Part 2: %s feet of ribbon needed' % total_ribbon
