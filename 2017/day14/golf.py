from knothash import input_to_hex
def g_h(seed,n):
    hs = [bin(int(input_to_hex(seed+'-'+str(i)),16))[2:].zfill(128).replace('1','#').replace('0','.') for i in range(0,n)]
    ds = ['.' for i in range(0,len(hs)+2)]
    return [ds]+[['.']+[c for c in hs[i]]+['.'] for i in range(len(hs))]+[ds]
def c_g(hs):
    n = 0
    for y,h in enumerate(hs):
        for x,c in enumerate(h):
            n += e_g(y,x,n,hs)
    return n,hs
def e_g(y,x,ix,hs):
    if hs[y][x] != '#':
        return 0
    hs[y][x] = ix
    for o in [(0,1),(0,-1),(1,0),(-1,0)]:
        _y = y+o[0]
        _x = x+o[1]
        e_g(_y,_x,ix,hs)
    return 1
hs = g_h(open('day.input','r').read(),128)
print(sum([1 for h in hs for c in h if c == '#']))
print(c_g(hs)[0])
