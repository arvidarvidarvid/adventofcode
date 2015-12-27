instructions = open('day23input.txt', 'r').read().split('\n')

a = 1
b = 0

"""
hlf r sets register r to half its current value, then continues with the next instruction.
tpl r sets register r to triple its current value, then continues with the next instruction.
inc r increments register r, adding 1 to it, then continues with the next instruction.
jmp offset is a jump; it continues with the instruction offset away relative to itself.
jie r, offset is like jmp, but only jumps if register r is even ("jump if even").
jio r, offset is like jmp, but only jumps if register r is 1 ("jump if one", not odd).
"""

print instructions

i = 0
while i < len(instructions):
    inst = instructions[i].split()
    action = inst[0]
    print inst
    if action == 'hlf':
        print 'hlf'
        r = inst[1]
        if r == 'a':
            print 'a'
            a = a/2
        if r == 'b':
            print 'b'
            b = b/2
        i += 1
    elif action == 'tpl':
        print 'tpl'
        r = inst[1]
        if r == 'a':
            a = a*3
            print 'a'
        if r == 'b':
            b = b*3
            print 'b'
        i += 1
    elif action == 'inc':
        r = inst[1]
        if r == 'a':
            a += 1
        if r == 'b':
            b += 1
        i += 1
    elif action == 'jmp':
        jmp = inst[1]
        direction = jmp[0]
        distance = jmp[1:]
        if direction == '-':
            i -= int(distance)
        if direction == '+':
            i += int(distance)
    elif action == 'jie':
        print 'jie'
        jmp = inst[2]
        direction = jmp[0]
        r = inst[1][0]
        distance = jmp[1:]
        jump = False
        if r == 'a':
            print 'a'
            if a % 2 == 0:
                print 'a: ' + str(a) + ' is even'
                jump = True
        if r == 'b':
            print 'b'
            if b % 2 == 0:
                print 'b: ' + str(b) + ' is even'
                jump = True
        if jump is True:
            if direction == '-':
                i -= int(distance)
            if direction == '+':
                i += int(distance)
        else:
            i += 1
    elif action == 'jio':
        print 'jio'
        jmp = inst[2]
        direction = jmp[0]
        r = inst[1][0]
        distance = jmp[1:]
        jump = False
        if r == 'a':
            print 'a'
            if a == 1:
                print 'a: ' + str(a) + ' is odd'
                jump = True
        if r == 'b':
            print 'b'
            if b == 1:
                print 'b: ' + str(b) + ' is odd'
                jump = True
        if jump is True:
            if direction == '-':
                i -= int(distance)
            if direction == '+':
                i += int(distance)
        else:
            i += 1
    else:
        print inst
        break

print a
print b
