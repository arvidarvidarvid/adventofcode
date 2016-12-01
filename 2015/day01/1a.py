with open('1.txt', 'r') as f:
    parentheses = f.read()

floor = 0
position_in_string = 0

for p in parentheses:
    if p == '(':
        floor = floor+1
    if p == ')':
        floor = floor-1
    position_in_string = position_in_string+1
    # Part 2, comment out to get the part 1 result
    if floor < 0:
        print ('Part 2: Santa ends up in the basement at position %s' %
               position_in_string)
        break

# Part 1 result
print 'Part 1: Santa ends up on %s' % floor
