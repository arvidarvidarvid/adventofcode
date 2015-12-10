import re

TOTAL_LOOKUPS = 0

funcs = {
    'ai': ['af AND ah', None],
    'll': ['NOT lk', None],
    'is': ['hz RSHIFT 1', None],
    'gp': ['NOT go', None],
    'dv': ['du OR dt', None],
    'aa': ['x RSHIFT 5', None],
    'ba': ['at OR az', None],
    'es': ['eo LSHIFT 15', None],
    'cu': ['ci OR ct', None],
    'f': ['b RSHIFT 5', None],
    'fo': ['fm OR fn', None],
    'ah': ['NOT ag', None],
    'x': ['v OR w', None],
    'j': ['g AND i', None],
    'ar': ['an LSHIFT 15', None],
    'cy': ['1 AND cx', None],
    'jy': ['jq AND jw', None],
    'ix': ['iu RSHIFT 5', None],
    'go': ['gl AND gm', None],
    'bx': ['NOT bw', None],
    'jr': ['jp RSHIFT 3', None],
    'hj': ['hg AND hh', None],
    'by': ['bv AND bx', None],
    'et': ['er OR es', None],
    'ks': ['kl OR kr', None],
    'fm': ['et RSHIFT 1', None],
    'h': ['e AND f', None],
    'ao': ['u LSHIFT 1', None],
    'hx': ['he RSHIFT 1', None],
    'ej': ['eg AND ei', None],
    'bw': ['bo AND bu', None],
    'eg': ['dz OR ef', None],
    'ea': ['dy RSHIFT 3', None],
    'gn': ['gl OR gm', None],
    'du': ['da LSHIFT 1', None],
    'aw': ['au OR av', None],
    'gv': ['gj OR gu', None],
    'fb': ['eu OR fa', None],
    'ln': ['lg OR lm', None],
    'g': ['e OR f', None],
    'dn': ['NOT dm', None],
    'm': ['NOT l', None],
    'as': ['aq OR ar', None],
    'gm': ['gj RSHIFT 5', None],
    'hp': ['hm AND ho', None],
    'gi': ['ge LSHIFT 15', None],
    'ki': ['jp RSHIFT 1', None],
    'hi': ['hg OR hh', None],
    'lw': ['lc LSHIFT 1', None],
    'ko': ['km OR kn', None],
    'fk': ['eq LSHIFT 1', None],
    'an': ['1 AND am', None],
    'hc': ['gj RSHIFT 1', None],
    'am': ['aj AND al', None],
    'gw': ['gj AND gu', None],
    'kr': ['ko AND kq', None],
    'hb': ['ha OR gz', None],
    'bz': ['bn OR by', None],
    'jc': ['iv OR jb', None],
    'ad': ['NOT ac', None],
    'bv': ['bo OR bu', None],
    'l': ['d AND j', None],
    'ce': ['bk LSHIFT 1', None],
    'dl': ['de OR dk', None],
    'dw': ['dd RSHIFT 1', None],
    'im': ['hz AND ik', None],
    'je': ['NOT jd', None],
    'fp': ['fo RSHIFT 2', None],
    'hv': ['hb LSHIFT 1', None],
    'lg': ['lf RSHIFT 2', None],
    'gl': ['gj RSHIFT 3', None],
    'kk': ['ki OR kj', None],
    'al': ['NOT ak', None],
    'lf': ['ld OR le', None],
    'ck': ['ci RSHIFT 3', None],
    'cd': ['1 AND cc', None],
    'ky': ['NOT kx', None],
    'fw': ['fp OR fv', None],
    'ey': ['ev AND ew', None],
    'dx': ['dt LSHIFT 15', None],
    'ay': ['NOT ax', None],
    'bs': ['bp AND bq', None],
    'ij': ['NOT ii', None],
    'cv': ['ci AND ct', None],
    'ir': ['iq OR ip', None],
    'y': ['x RSHIFT 2', None],
    'fs': ['fq OR fr', None],
    'bq': ['bn RSHIFT 5', None],
    'c': ['0', None],
    'b': ['956', None],
    'k': ['d OR j', None],
    'ab': ['z OR aa', None],
    'gg': ['gf OR ge', None],
    'dh': ['df OR dg', None],
    'hk': ['NOT hj', None],
    'dj': ['NOT di', None],
    'fn': ['fj LSHIFT 15', None],
    'ly': ['lf RSHIFT 1', None],
    'p': ['b AND n', None],
    'jx': ['jq OR jw', None],
    'gq': ['gn AND gp', None],
    'aq': ['x RSHIFT 1', None],
    'fa': ['ex AND ez', None],
    'fd': ['NOT fc', None],
    'bk': ['bj OR bi', None],
    'av': ['as RSHIFT 5', None],
    'hy': ['hu LSHIFT 15', None],
    'gt': ['NOT gs', None],
    'fv': ['fs AND fu', None],
    'dk': ['dh AND dj', None],
    'cc': ['bz AND cb', None],
    'er': ['dy RSHIFT 1', None],
    'he': ['hc OR hd', None],
    'ga': ['fo OR fz', None],
    'u': ['t OR s', None],
    'd': ['b RSHIFT 2', None],
    'jz': ['NOT jy', None],
    'ia': ['hz RSHIFT 2', None],
    'kx': ['kk AND kv', None],
    'gd': ['ga AND gc', None],
    'gf': ['fl LSHIFT 1', None],
    'ca': ['bn AND by', None],
    'hs': ['NOT hr', None],
    'bt': ['NOT bs', None],
    'lh': ['lf RSHIFT 3', None],
    'ax': ['au AND av', None],
    'ge': ['1 AND gd', None],
    'jt': ['jr OR js', None],
    'fz': ['fw AND fy', None],
    'ja': ['NOT iz', None],
    't': ['c LSHIFT 1', None],
    'eb': ['dy RSHIFT 5', None],
    'br': ['bp OR bq', None],
    'i': ['NOT h', None],
    'dt': ['1 AND ds', None],
    'ae': ['ab AND ad', None],
    'bj': ['ap LSHIFT 1', None],
    'bu': ['br AND bt', None],
    'cb': ['NOT ca', None],
    'em': ['NOT el', None],
    'w': ['s LSHIFT 15', None],
    'gr': ['gk OR gq', None],
    'fi': ['ff AND fh', None],
    'kj': ['kf LSHIFT 15', None],
    'fx': ['fp AND fv', None],
    'lj': ['lh OR li', None],
    'bp': ['bn RSHIFT 3', None],
    'kb': ['jp OR ka', None],
    'lx': ['lw OR lv', None],
    'jb': ['iy AND ja', None],
    'ek': ['dy OR ej', None],
    'bi': ['1 AND bh', None],
    'ku': ['NOT kt', None],
    'ap': ['ao OR an', None],
    'ii': ['ia AND ig', None],
    'ez': ['NOT ey', None],
    'cg': ['bn RSHIFT 1', None],
    'fl': ['fk OR fj', None],
    'cf': ['ce OR cd', None],
    'fc': ['eu AND fa', None],
    'kh': ['kg OR kf', None],
    'ju': ['jr AND js', None],
    'iw': ['iu RSHIFT 3', None],
    'di': ['df AND dg', None],
    'do': ['dl AND dn', None],
    'le': ['la LSHIFT 15', None],
    'gh': ['fo RSHIFT 1', None],
    'gx': ['NOT gw', None],
    'gc': ['NOT gb', None],
    'jl': ['ir LSHIFT 1', None],
    'ak': ['x AND ai', None],
    'hh': ['he RSHIFT 5', None],
    'lv': ['1 AND lu', None],
    'fu': ['NOT ft', None],
    'gj': ['gh OR gi', None],
    'li': ['lf RSHIFT 5', None],
    'z': ['x RSHIFT 3', None],
    'e': ['b RSHIFT 3', None],
    'hf': ['he RSHIFT 2', None],
    'fy': ['NOT fx', None],
    'jw': ['jt AND jv', None],
    'hz': ['hx OR hy', None],
    'kc': ['jp AND ka', None],
    'fe': ['fb AND fd', None],
    'il': ['hz OR ik', None],
    'db': ['ci RSHIFT 1', None],
    'gb': ['fo AND fz', None],
    'ft': ['fq AND fr', None],
    'gk': ['gj RSHIFT 2', None],
    'ci': ['cg OR ch', None],
    'ch': ['cd LSHIFT 15', None],
    'kg': ['jm LSHIFT 1', None],
    'ik': ['ih AND ij', None],
    'fq': ['fo RSHIFT 3', None],
    'fr': ['fo RSHIFT 5', None],
    'fj': ['1 AND fi', None],
    'la': ['1 AND kz', None],
    'jh': ['iu AND jf', None],
    'ct': ['cq AND cs', None],
    'ep': ['dv LSHIFT 1', None],
    'hm': ['hf OR hl', None],
    'kp': ['km AND kn', None],
    'dm': ['de AND dk', None],
    'dg': ['dd RSHIFT 5', None],
    'lp': ['NOT lo', None],
    'jv': ['NOT ju', None],
    'fh': ['NOT fg', None],
    'cp': ['cm AND co', None],
    'ed': ['ea AND eb', None],
    'df': ['dd RSHIFT 3', None],
    'gu': ['gr AND gt', None],
    'eq': ['ep OR eo', None],
    'cr': ['cj AND cp', None],
    'lr': ['lf OR lq', None],
    'ha': ['gg LSHIFT 1', None],
    'eu': ['et RSHIFT 2', None],
    'ji': ['NOT jh', None],
    'en': ['ek AND em', None],
    'jo': ['jk LSHIFT 15', None],
    'ih': ['ia OR ig', None],
    'gy': ['gv AND gx', None],
    'fg': ['et AND fe', None],
    'lk': ['lh AND li', None],
    'ip': ['1 AND io', None],
    'ke': ['kb AND kd', None],
    'kn': ['kk RSHIFT 5', None],
    'ig': ['id AND if', None],
    'lt': ['NOT ls', None],
    'dy': ['dw OR dx', None],
    'dq': ['dd AND do', None],
    'ls': ['lf AND lq', None],
    'kd': ['NOT kc', None],
    'el': ['dy AND ej', None],
    'kf': ['1 AND ke', None],
    'ff': ['et OR fe', None],
    'ic': ['hz RSHIFT 5', None],
    'dp': ['dd OR do', None],
    'cq': ['cj OR cp', None],
    'dr': ['NOT dq', None],
    'ld': ['kk RSHIFT 1', None],
    'jj': ['jg AND ji', None],
    'hq': ['he OR hp', None],
    'hl': ['hi AND hk', None],
    'ds': ['dp AND dr', None],
    'eh': ['dz AND ef', None],
    'ib': ['hz RSHIFT 3', None],
    'dd': ['db OR dc', None],
    'iq': ['hw LSHIFT 1', None],
    'hr': ['he AND hp', None],
    'cs': ['NOT cr', None],
    'lo': ['lg AND lm', None],
    'hw': ['hv OR hu', None],
    'io': ['il AND in', None],
    'ei': ['NOT eh', None],
    'hd': ['gz LSHIFT 15', None],
    'gs': ['gk AND gq', None],
    'eo': ['1 AND en', None],
    'kq': ['NOT kp', None],
    'ew': ['et RSHIFT 5', None],
    'lm': ['lj AND ll', None],
    'hg': ['he RSHIFT 3', None],
    'ev': ['et RSHIFT 3', None],
    'bf': ['as AND bd', None],
    'cx': ['cu AND cw', None],
    'ka': ['jx AND jz', None],
    'o': ['b OR n', None],
    'bh': ['be AND bg', None],
    'hu': ['1 AND ht', None],
    'gz': ['1 AND gy', None],
    'ho': ['NOT hn', None],
    'cm': ['ck OR cl', None],
    'ef': ['ec AND ee', None],
    'lz': ['lv LSHIFT 15', None],
    'kv': ['ks AND ku', None],
    'if': ['NOT ie', None],
    'hn': ['hf AND hl', None],
    's': ['1 AND r', None],
    'ie': ['ib AND ic', None],
    'ht': ['hq AND hs', None],
    'ag': ['y AND ae', None],
    'ee': ['NOT ed', None],
    'bm': ['bi LSHIFT 15', None],
    'dz': ['dy RSHIFT 2', None],
    'cj': ['ci RSHIFT 2', None],
    'bg': ['NOT bf', None],
    'in': ['NOT im', None],
    'ex': ['ev OR ew', None],
    'id': ['ib OR ic', None],
    'bo': ['bn RSHIFT 2', None],
    'de': ['dd RSHIFT 2', None],
    'bn': ['bl OR bm', None],
    'bl': ['as RSHIFT 1', None],
    'ec': ['ea OR eb', None],
    'lq': ['ln AND lp', None],
    'km': ['kk RSHIFT 3', None],
    'iu': ['is OR it', None],
    'iv': ['iu RSHIFT 2', None],
    'be': ['as OR bd', None],
    'it': ['ip LSHIFT 15', None],
    'iy': ['iw OR ix', None],
    'kl': ['kk RSHIFT 2', None],
    'bc': ['NOT bb', None],
    'cl': ['ci RSHIFT 5', None],
    'ma': ['ly OR lz', None],
    'ac': ['z AND aa', None],
    'jn': ['iu RSHIFT 1', None],
    'dc': ['cy LSHIFT 15', None],
    'cz': ['cf LSHIFT 1', None],
    'au': ['as RSHIFT 3', None],
    'da': ['cz OR cy', None],
    'kz': ['kw AND ky', None],
    'a': ['lx', None],
    'iz': ['iw AND ix', None],
    'lu': ['lr AND lt', None],
    'js': ['jp RSHIFT 5', None],
    'az': ['aw AND ay', None],
    'jf': ['jc AND je', None],
    'lc': ['lb OR la', None],
    'co': ['NOT cn', None],
    'lb': ['kh LSHIFT 1', None],
    'jk': ['1 AND jj', None],
    'af': ['y OR ae', None],
    'cn': ['ck AND cl', None],
    'kw': ['kk OR kv', None],
    'cw': ['NOT cv', None],
    'kt': ['kl AND kr', None],
    'jg': ['iu OR jf', None],
    'bb': ['at AND az', None],
    'jq': ['jp RSHIFT 2', None],
    'jd': ['iv AND jb', None],
    'jp': ['jn OR jo', None],
    'aj': ['x OR ai', None],
    'bd': ['ba AND bc', None],
    'jm': ['jl OR jk', None],
    'v': ['b RSHIFT 1', None],
    'r': ['o AND q', None],
    'q': ['NOT p', None],
    'n': ['k AND m', None],
    'at': ['as RSHIFT 2', None]
    }


def _not(i, ps):
    return 0xffff - int(get_value(i, ps))


def _and(i1, i2, ps):
    return int(get_value(i1, ps)) & int(get_value(i2, ps))


def _rshift(i, s, ps):
    return int(get_value(i, ps)) >> int(s)


def _lshift(i, s, ps):
    return int(get_value(i, ps)) << int(s)


def _or(i1, i2, ps):
    return int(get_value(i1, ps)) | int(get_value(i2, ps))


def string_to_result(s, key, ps):

    direct_p = re.match(r'^([a-z]{1,2}|\d+)$', s)
    not_p = re.match(r'^NOT ([a-z]{1,2}|\d+)$', s)
    and_p = re.match(r'^([a-z]{1,2}|\d+) AND ([a-z]{1,2}|\d+)$', s)
    or_p = re.match(r'^([a-z]{1,2}|\d+) OR ([a-z]{1,2}|\d+)$', s)
    rshift_p = re.match(r'^([a-z]{1,2}|\d+) RSHIFT (\d{1,2})$', s)
    lshift_p = re.match(r'^([a-z]{1,2}|\d+) LSHIFT (\d{1,2})$', s)

    if direct_p is not None:
        res = get_value(direct_p.group(1), ps)
    elif not_p is not None:
        res = _not(not_p.group(1), ps)
    elif and_p is not None:
        res = _and(and_p.group(1), and_p.group(2), ps)
    elif or_p is not None:
        res = _or(or_p.group(1), or_p.group(2), ps)
    elif rshift_p is not None:
        res = _rshift(rshift_p.group(1), rshift_p.group(2), ps)
    elif lshift_p is not None:
        res = _lshift(lshift_p.group(1), lshift_p.group(2), ps)
    else:
        raise Exception('Failed to match to function.')

    funcs[key][1] = res
    return res


def get_value(key, ps=[]):

    global TOTAL_LOOKUPS

    print 'Looking up %s (%i lookups so far)' % (key, TOTAL_LOOKUPS)
    TOTAL_LOOKUPS = TOTAL_LOOKUPS + 1

    if TOTAL_LOOKUPS > 10000000:
        print funcs
        raise Exception('Reached max lookups')

    if key in ps:
        pass
        # print 'Circular lookup. Key=%s, Parents=%s' % (key, ps)
    else:
        ps.append(key)

    if re.match(r'^\d+$', key):
        return key
    elif funcs[key][1] is not None:
        return funcs[key][1]
    else:
        return string_to_result(funcs[key][0], key, ps)


print get_value('a')
print funcs
