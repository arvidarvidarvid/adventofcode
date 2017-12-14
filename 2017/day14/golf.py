from k import ih
def gh(s,n):
    hs = [bin(int(ih(s+'-'+str(i)),16))[2:].zfill(128).replace('1','#').replace('0','.') for i in range(n)]
    ds = ['.' for i in range(len(hs)+2)]
    return [ds]+[['.']+[c for c in hs[i]]+['.'] for i in range(len(hs))]+[ds]
def cg(hs):
    n=0
    for y,h in enumerate(hs):
        for x,c in enumerate(h):
            n+=eg(y,x,n,hs)
    return n
def eg(y,x,ix,hs):
    if hs[y][x]!='#':
        return 0
    hs[y][x]=ix
    [eg(y+o[0],x+o[1],ix,hs) for o in [(0,1),(0,-1),(1,0),(-1,0)]]
    return 1
hs=gh(open('i').read(),128)
print(sum([1 for h in hs for c in h if c=='#']),cg(hs))
