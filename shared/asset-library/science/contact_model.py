"""Ideal contact of two semi-infinite homogeneous media. SI units.
Constant properties, perfect contact, 1-D conduction, no phase change.
Not a model of sensation or skin blood perfusion; material parameters supplied by caller.
"""
import math

def effusivity(k, rho, c):
    if min(k,rho,c)<=0: raise ValueError('Properties must be positive')
    return math.sqrt(k*rho*c)

def interface_temperature(T1,T2,e1,e2):
    if min(e1,e2)<=0: raise ValueError('Effusivities must be positive')
    return (e1*T1+e2*T2)/(e1+e2)

def temperature(x,t,initial,interface,alpha):
    """x>=0 measured into either body, t>0. Same temperature scale on both sides."""
    if x<0 or t<=0 or alpha<=0: raise ValueError('Require x>=0, t>0, alpha>0')
    return initial+(interface-initial)*math.erfc(x/(2*math.sqrt(alpha*t)))

def flux_into_cold(t,T_hot,T_cold,e_hot,e_cold):
    if t<=0 or min(e_hot,e_cold)<=0: raise ValueError('Invalid parameters')
    return (T_hot-T_cold)/(1/e_hot+1/e_cold)/math.sqrt(math.pi*t)

if __name__=='__main__':
    e=effusivity(1,1,1)
    assert interface_temperature(30,20,e,e)==25
    assert temperature(0,1,20,25,1)==25
    assert temperature(100,1,20,25,1)==20
    assert flux_into_cold(1,20,20,e,e)==0
    print('Model limiting-case checks passed')
