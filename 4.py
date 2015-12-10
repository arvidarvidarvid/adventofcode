import hashlib

seed = 'yzbqklnj'

i = 0
while True:
    gen_seed = seed + unicode(i)
    m = hashlib.md5()
    m.update(gen_seed)
    if m.hexdigest()[:6] == '000000':
        print gen_seed
        print m.hexdigest()
        break
    else:
        i = i+1
