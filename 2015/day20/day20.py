import numpy as np


def np_elf_by_elf(target):

    """I had an uglier version of this but the numpy stuff was too elegant not
    to use instead. Played around with it a bit to make sure I understand
    what's going on."""

    UPPER_HOUSE_LIMIT = 1000000

    houses_part1 = np.zeros(UPPER_HOUSE_LIMIT)
    houses_part2 = np.zeros(UPPER_HOUSE_LIMIT)

    for elf in xrange(1, UPPER_HOUSE_LIMIT):
        houses_part1[elf::elf] += 10 * elf
        houses_part2[elf:(elf+1)*50:elf] += 11 * elf

    return (np.nonzero(houses_part1 >= target)[0][0],
            np.nonzero(houses_part2 >= target)[0][0])


target_present_count = int(open('day20.txt', 'r').read())
houses = np_elf_by_elf(target_present_count)

print ('Part 1: The first house with at least %s presents is house %s' %
       (target_present_count, houses[0]))
print ("""Part 2: The first house with at least %s presents when the elves only
        choose to visit 50 houses each is house %s""" % (target_present_count,
       houses[1]))
