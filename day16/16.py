import re

sues = open('16.txt', 'r').read().split('\n')

rules = open('rules.txt', 'r').read().split('\n')
r_dict = dict()
for l in rules:
    k, v = l.split(': ')
    r_dict[k] = int(v)


def find_sue(part2=False):
    for sue in sues:
        characteristics = re.findall(r'(\w+): (\d+)', sue)
        failed = False
        for c in characteristics:
            if part2:
                if c[0] in ['cats', 'trees']:
                    if not int(c[1]) > r_dict[c[0]]:
                        failed = True
                elif c[0] in ['pomeranians', 'goldfish']:
                    if not int(c[1]) < r_dict[c[0]]:
                        failed = True
                elif r_dict[c[0]] != int(c[1]):
                    failed = True
                else:
                    Exception('Didnt match')
            else:
                if r_dict[c[0]] != int(c[1]):
                    failed = True
        if not failed:
            return sue
        else:
            pass

print find_sue()
print find_sue(part2=True)
