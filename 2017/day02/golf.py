g = [sorted(list(map(lambda x: int(x), l.split()))) for l in open('day.input', 'r').readlines()]
print(sum([max(l) - min(l) for l in g]))
print(sum([n / l[i] for l in g for i in range(len(l)) for n in l[i + 1:] if not n % l[i]]))
