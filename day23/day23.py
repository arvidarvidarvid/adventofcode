instructions = open('day23input.txt', 'r').read().split('\n')


def get_results(a=0, b=0):
    i = 0
    while i < len(instructions):
        inst = instructions[i].split()
        action = inst[0]
        if action == 'hlf':
            r = inst[1]
            if r == 'a':
                a = a/2
            if r == 'b':
                b = b/2
            i += 1
        elif action == 'tpl':
            r = inst[1]
            if r == 'a':
                a = a*3
            if r == 'b':
                b = b*3
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
            jmp = inst[2]
            direction = jmp[0]
            r = inst[1][0]
            distance = jmp[1:]
            jump = False
            if r == 'a':
                if a % 2 == 0:
                    jump = True
            if r == 'b':
                if b % 2 == 0:
                    jump = True
            if jump is True:
                if direction == '-':
                    i -= int(distance)
                if direction == '+':
                    i += int(distance)
            else:
                i += 1
        elif action == 'jio':
            jmp = inst[2]
            direction = jmp[0]
            r = inst[1][0]
            distance = jmp[1:]
            jump = False
            if r == 'a':
                if a == 1:
                    jump = True
            if r == 'b':
                if b == 1:
                    jump = True
            if jump is True:
                if direction == '-':
                    i -= int(distance)
                if direction == '+':
                    i += int(distance)
            else:
                i += 1
        else:
            break
    return (a, b)

# Part 1
print (u'Part 1: The value of b after processing all instructions is %i' %
       get_results()[1])

# Part 2
print (u'Part 2: The value of b after processing all instructions is %i' %
       get_results(1, 0)[1])
