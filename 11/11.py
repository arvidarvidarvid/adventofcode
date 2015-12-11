import re

input_pass = 'cqjxjnds'
test_prev = 'ghijklmn'
test_next = 'ghjaabcc'

ALFABET = 'abcdefghijklmnopqrstuvwxyz'


def increment_letter(l):
    global ALFABET
    if l == ALFABET[-1]:
        return ALFABET[0]
    else:
        curr_pos = ALFABET.find(l)
        return ALFABET[curr_pos+1]


def get_next(password):
    next_pass = password
    rotated = False
    i = 0
    while rotated is False:
        first_part = next_pass[:-i-1]
        rotated_part = increment_letter(next_pass[-i-1])
        last_part = next_pass[-i:] if i > 0 else ''
        next_pass = ''.join([
            first_part,
            rotated_part,
            last_part
            ])
        if re.match(r'(^[a]+$)', next_pass[-i-1:]) is not None:
            rotated = False
        else:
            rotated = True
        i += 1
    return next_pass


def pass_iol_rule(password):
    if re.match(r'.*([iol]).*', password) is not None:
        return False
    else:
        return True


def pass_straight_rule(password):
    global ALFABET
    prev_char = password[0]
    straight = 1
    i = 0
    while straight != 3 and i < len(password)-1:
        prev_c_alpb_pos = ALFABET.find(prev_char)
        if ALFABET.find(password[i+1]) == prev_c_alpb_pos+1:
            straight += 1
        else:
            straight = 1
        prev_char = password[i+1]
        i += 1
    if straight == 3:
        return True
    else:
        return False


def pass_double_digit_rule(password):
    if re.match(r'.*([a-z])\1.*([a-z])\2.*', password) is not None:
        return True
    else:
        return False


def check_for_rules(password):
    if (pass_iol_rule(password) and
            pass_straight_rule(password) and
            pass_double_digit_rule(password)):
        return True
    else:
        return False


def get_next_valid(prev):
    passing_next_pass = None
    password = prev
    while passing_next_pass is None:
        password = get_next(password)
        if check_for_rules(password):
            passing_next_pass = password
        else:
            pass
    return passing_next_pass


assert check_for_rules('ghjaabcc') is True
assert check_for_rules('ghlaabcc') is False
assert check_for_rules('ghjdabcd') is False
assert check_for_rules('ghjadbcc') is False
assert get_next('aaaaaaaa') == 'aaaaaaab'

# Part one
print get_next_valid(input_pass)

# Part two
print get_next_valid(get_next_valid(input_pass))
