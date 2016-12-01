import re

with open('8.txt', 'r') as f:
    d = f.read()

data = d.split('\n')

total = 0
te = 0
for d in data:
    print re.escape(d)
    te += len(re.escape(d))+2
    total += len(d)
print total
print te
print te - total
