with open('1.txt', 'r') as f:
    string = f.read()

result = 0

j = 0

for i in string:
    if i == '(':
        result = result+1
    if i == ')':
        result = result-1
    j = j+1
    if result < 0:
        print j
        break

print result
