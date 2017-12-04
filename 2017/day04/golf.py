print(sum([1 for p in open('i', 'r').readlines() if len(p.split()) == len(set(p.split()))]))
print(sum([1 for p in open('i', 'r').readlines() if len(p.split()) == len(set(''.join(sorted(w)) for w in p.split()))]))
