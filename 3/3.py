with open('3.txt', 'r') as f:
    directions = f.read()

GIFTS = []


class Santa(object):
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0


def log_location(santa):

    global GIFTS

    GIFTS.append((santa.pos_x, santa.pos_y))


santa = Santa()
robosanta = Santa()

log_location(santa)

d = 1
for m in directions:

    if d % 2 == 0:
        this_santa = robosanta
    else:
        this_santa = santa

    if m == '^':
        this_santa.pos_y = this_santa.pos_y + 1
    elif m == 'v':
        this_santa.pos_y = this_santa.pos_y - 1
    elif m == '<':
        this_santa.pos_x = this_santa.pos_x - 1
    elif m == '>':
        this_santa.pos_x = this_santa.pos_x + 1

    log_location(this_santa)
    d = d+1


print len(set(GIFTS))
