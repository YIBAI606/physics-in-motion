"""原创学习练习：爱因斯坦固体平衡分布，不是动力学模拟。Python 3 标准库。"""
from math import comb, sqrt
from fractions import Fraction

def omega(n, q):
    return comb(q+n-1,q)

def distribution(na, nb, q):
    weights=[omega(na,k)*omega(nb,q-k) for k in range(q+1)]
    total=omega(na+nb,q)
    assert sum(weights)==total
    return weights,[Fraction(w,total) for w in weights]

def check(na,nb,q):
    weights,p=distribution(na,nb,q)
    m=na+nb
    mean=sum(k*x for k,x in enumerate(p))
    var=sum((k-mean)**2*x for k,x in enumerate(p))
    assert mean==Fraction(q*na,m)
    assert var==Fraction(q*na*nb*(m+q),m*m*(m+1))
    return weights,p,var

if __name__=="__main__":
    for na,nb in [(3,3),(2,4),(1,1)]:
        w,p,v=check(na,nb,6)
        print("\nNA, NB, q =",na,nb,6)
        print("qA   states   probability")
        for k in range(7): print(k,w[k],f"{float(p[k]):.6%}")
    assert check(3,3,6)[0]==[28,63,90,100,90,63,28]
    assert check(2,4,6)[0]==[84,112,105,80,50,24,7]
    print("\nScale comparison: same energy per oscillator")
    for n in [3,30,300]:
        q=2*n
        w,p,v=check(n,n,q)
        near=sum(p[k] for k in range(q+1) if abs(Fraction(k,q)-Fraction(1,2))<=Fraction(1,10))
        print("N =",n,"P(exact half) =",float(p[n]),
              "P(within 10 percentage points) =",float(near),
              "std(qA/q) =",sqrt(float(v))/q)
    print("\nAll normalization and moment checks passed.")
