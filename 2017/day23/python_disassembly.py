
# What it turns out that this does is that it works through every 17 integers
# between 107900 and 124900 and counts the number of non-primes. This version
# is still really slow, wrote a fast one in day.py
# For some reason the slightly optimised disassembly version comes out one off
# at 906 when the correct answer is 907. I'm not going to spend any more time
# hunting that down. The reimplementation in day.py gives the right answer and
# that's enough for me.


b = 107900
c = 124900
d = 0
e = 0
f = 0
g = 0
h = 0

while c != b:

    print('b', b)

    # 0  set f 1
    f = 1
    # 1  set d 2
    d = 2
    # 2  set e 2
    e = 2

    while d <= (b / 2) + 1:

        e = 2

        while d * e <= b:
            # 3  set g d
            # g = d
            # 4  mul g e
            # g = g * e
            # 5  sub g b
            # g = g - b
            # 6  jnz g 2
            # if g == 0:
            if d * e == b:
                # 7  set f 0
                f = 0
            # 8  sub e -1
            e = e + 1
            # 9  set g e
            # g = e
            # 10 sub g b
            # g = g - b
            # 11 jnz g -8
        # 12 sub d -1
        d = d + 1
        # 13 set g d
        # g = d
        # 14 sub g b
        # g = d - b
        # 15 jnz g -13
    # 16 jnz f 2
    if f == 0:
        # 17 sub h -1
        h = h + 1
        print(h)

    # 18 set g b
    # g = b
    # 19 sub g c
    # g = g - c
    # 20 jnz g 2
    # 22 sub b -17
    b = b + 17
    # 21 jnz 1 3
    # 23 jnz 1 -23

print(h)

"""b = 107900
c = 124900
h = 0

while b != c:
    f = 1
    d = 2
    e = 2
    while d * 2 <= b:
        e = 2
        while d * e <= b:
            if d * e == b:
                f = 0
            e += 1
        d += 1
    if f == 1:
        h += 1
    b += 17
    print('b', b)

print(h)
"""
