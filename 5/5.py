import re

with open('5.txt', 'r') as f:
    string = f.read()


def test_string_v1(s):
    vowel_match = re.findall(r'[aeiou]', s)
    double_letter_match = re.match(r'.*([a-z])\1.*', s)
    not_allowed_match = re.match(r'.*(ab|cd|pq|xy).*', s)
    if (len(vowel_match) >= 3 and double_letter_match and
            not_allowed_match is None):
        return True
    else:
        return False


def test_string_v2(s):
    two_doubles_match = re.match(r'.*([a-z]{2}).*\1.*', s)
    repeat_with_inbetween = re.match(r'.*([a-z]).\1.*', s)
    if two_doubles_match and repeat_with_inbetween:
        return True
    else:
        return False


count = 0
for s in string.split('\n'):
    if test_string_v2(s):
        count = count+1

print count
