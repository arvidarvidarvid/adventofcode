from knothash import input_to_hex
def gh(s,n):
    hs = [bin(int(input_to_hex(s+'-'+str(i)),16))[2:].zfill(128).replace('1','#').replace('0','.') for i in range(0,n)]
    ds = ['.' for i in range(0,len(hs)+2)]
    return [ds]+[['.']+[c for c in hs[i]]+['.'] for i in range(len(hs))]+[ds]
def cg(hs):
    n = 0
    for y,h in enumerate(hs):
        for x,c in enumerate(h):
            n += eg(y,x,n,hs)
    return n,hs
def eg(y,x,ix,hs):
    if hs[y][x] != '#':
        return 0
    hs[y][x] = ix
    for o in [(0,1),(0,-1),(1,0),(-1,0)]:
        _y = y+o[0]
        _x = x+o[1]
        eg(_y,_x,ix,hs)
    return 1
hs = gh(open('day.input','r').read(),128)
print(sum([1 for h in hs for c in h if c == '#']))
print(cg(hs)[0])
