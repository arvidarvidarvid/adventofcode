# encoding=utf8

from itertools import groupby

seed = '3113322113'
test_seed = '111221'
test_output = '312211'

"""
So this commented part was an iterative solution that took minutes to run for
just 40 rounds on the input seed. Found the itertools groupby method and
applied that for the final solution.
"""

# def find_first_seq(string):
#     first = string[0]
#     if len(string) == 1:
#         return (1, first)
#     else:
#         for i in range(len(string[1:])):
#             if string[1:][i] == first:
#                 continue
#             else:
#                 return (str(i+1), str(first))


# def look_and_say(string):
#     new_string = ''
#     while len(string) > 0:
#         ffs = find_first_seq(string)
#         new_string += '%s%s' % ffs
#         string = string[int(ffs[0]):]
#     return new_string


def look_and_say(string):
    return ''.join([str(len(list(v))) + k for k, v in groupby(string)])


def looped_las(string, loops):
    string = string
    for i in range(0, loops):
        string = look_and_say(string)
    return string


print len(looped_las(seed, 50))
