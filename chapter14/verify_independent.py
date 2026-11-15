"""Independent re-derivation of chapter-14 numbers (no book modules)."""
import itertools, json, math
import numpy as np
from scipy.optimize import minimize
C = {('A','B'):5,('A','C'):12,('A','D'):4,('B','C'):7,('B','D'):4,('C','D'):10}
def c(a,b): return C.get((a,b), C.get((b,a)))
cities = 'BCD'
def cost(bits, lam):
    x = np.array(bits).reshape(3,3)          # row city, col step
    pen = sum((x[i].sum()-1)**2 for i in range(3)) + sum((x[:,t].sum()-1)**2 for t in range(3))
    d = 0
    for i in range(3):
        d += c('A',cities[i])*x[i,0] + c(cities[i],'A')*x[i,2]
        for j in range(3):
            if i!=j:
                for t in range(2): d += c(cities[i],cities[j])*x[i,t]*x[j,t+1]
    return d + lam*pen
strs = list(itertools.product([0,1], repeat=9))   # q0 leftmost
def E(lam): return np.array([cost(s,lam) for s in strs], float)
E20 = E(20)
feas = np.array([all(np.array(s).reshape(3,3).sum(0)==1) and all(np.array(s).reshape(3,3).sum(1)==1) for s in strs])
opt = E20 == E20[feas].min()
print('feasible', feas.sum(), 'infeasible', (~feas).sum(), 'opt strings', [''.join(map(str,strs[k])) for k in np.where(opt)[0]])
inf = E20[~feas]
print('cheapest infeas', inf.min(), 'count 48..60', ((inf>=48)&(inf<=60)).sum(), 'max', E20.max(), 'mean', E20.mean())
for lam in (10,40): e=E(lam); print('lam',lam,'mean',e.mean(),'cheapest inf',e[~feas].min())
print('000000000', cost([0]*9,20), '001100010', cost([0,0,1,1,0,0,0,1,0],20), '010000001', cost([0,1,0,0,0,0,0,0,1],20))
# own QAOA statevector: |+>, exp(-i g E), exp(-i b X) per qubit
def probs(e, gs, bs):
    psi = np.full(512, 1/np.sqrt(512), complex)
    for g,b in zip(gs,bs):
        psi = psi*np.exp(-1j*g*e)
        ps = psi.reshape([2]*9)
        cb, sb = np.cos(b), -1j*np.sin(b)
        for q in range(9):
            a0 = np.take(ps,0,axis=q); a1=np.take(ps,1,axis=q)
            ps = np.stack([cb*a0+sb*a1, sb*a0+cb*a1], axis=q)
        psi = ps.reshape(512)
    return np.abs(psi)**2
ang = json.load(open('angles.json'))
for p in '1234':
    P = probs(E20, *ang[p])
    print('p',p,'<H>',round(P@E20,2),'Popt',round(P[opt].sum(),4),'Pfeas',round(P[feas].sum(),4),'cond',round(P[opt].sum()/P[feas].sum(),3))
P1 = probs(E20,*ang['1'])
for k in np.where(feas)[0]: print('  ', ''.join(map(str,strs[k])), E20[k], round(P1[k],4))
r = minimize(lambda t: probs(E20,[t[0]],[t[1]])@E20, [0.015,-0.4363], method='COBYLA', options={'rhobeg':0.2,'tol':1e-4})
print('S=1', r.x.round(4), round(r.fun,2), r.nfev)
E10 = E(10)
r = minimize(lambda t: probs(E10,[t[0]/50],[t[1]])@E10, [0.025*50,-0.4363], method='COBYLA', options={'rhobeg':0.2,'tol':1e-4})
P = probs(E10,[r.x[0]/50],[r.x[1]])
print('lam10', round(r.x[0]/50,4), round(r.x[1],4), round(r.fun,2), round(P[opt].sum(),4), round(P[feas].sum(),4))
for p,Pp in (('2',0.0549),('3',0.1227)): print('shots', p, math.ceil(math.log(0.01)/math.log(1-Pp)))
# growth formula by explicit counting of couplings
for m in range(3,7):
    pairs=set()
    var=lambda i,t:i*m+t
    for i in range(m):
        for t1,t2 in itertools.combinations(range(m),2): pairs.add((var(i,t1),var(i,t2)))
    for t in range(m):
        for i1,i2 in itertools.combinations(range(m),2): pairs.add((var(i1,t),var(i2,t)))
    for t in range(m-1):
        for i in range(m):
            for j in range(m):
                if i!=j: pairs.add(tuple(sorted((var(i,t),var(j,t+1)))))
    print('m',m,'ZZ',len(pairs), m*(m-1)*(2*m-1))
# nearest neighbour with tie report
D={a:{b:c(a,b) for b in 'ABCD' if b!=a} for a in 'ABCD'}
for s in 'ABCD':
    t=[s]; ties=[]
    while len(t)<4:
        cand={j:D[t[-1]][j] for j in 'ABCD' if j not in t}
        mn=min(cand.values()); best=[j for j in cand if cand[j]==mn]
        if len(best)>1: ties.append((t[-1],best))
        t.append(best[0])
    tour=''.join(t)+s; L=sum(c(tour[k],tour[k+1]) for k in range(4))
    print('NN',s,tour,L,'ties',ties)
print('14.12', (0.30-0.01)/(1-0.01-0.04), (0.005-0.01)/0.95)
print('ratios', [round(a/b,2) for a,b in ((0.2022,0.0739),(0.1715,0.0755),(0.1031,0.0726),(0.0719,0.0539))])
print('misc', 0.995**200, math.exp(-1), 0.997**621, 0.2*0.1708+0.8*2/512, math.sqrt(.073*.927/1000), math.sqrt(.073*.927/1e4))
