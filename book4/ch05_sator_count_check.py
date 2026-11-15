"""ch05 check (2026-11-14), integers only: letter counts of the Sator square."""
from collections import Counter
w=['SATOR','AREPO','TENET','OPERA','ROTAS']
c=Counter(''.join(w)); print(sum(c.values()),dict(c))
assert sum(c.values())==25 and c['N']==1
assert [k for k,v in c.items() if v%2]==['N']          # only N has an odd count
assert [(i,j) for i in range(5) for j in range(5) if w[i][j]=='N']==[(2,2)]
assert all(w[i][j]==w[j][i] for i in range(5) for j in range(5))              # transpose-symmetric
assert all(w[i][j]==w[4-i][4-j] for i in range(5) for j in range(5))          # 180-degree symmetric
assert not all(c[k]==2 for k in c if k!='N')            # 'every other letter twice' is FALSE
print("OK: A,T,O,R,E occur 4 times, S,P twice, N once")
