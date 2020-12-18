
import pandas as pd
import numpy as np
def idxp1(i,N):
    return i%N +1
def idxm1(i,N):
    return 1+ (i+N-2)%N
def energy(S,J,N):
    E=0
    for i in np.arange(N)+1:
        for j in np.arange(N)+1:
            ip1=idxp1(i,N)-1
            jp1=idxp1(j,N)-1
            im1=idxm1(i,N)-1
            jm1=idxm1(j,N)-1
            i_idx=i-1
            j_idx=j-1
            e_add=-J*S[i_idx,j_idx]*(S[ip1,j_idx]+ S[im1,j_idx]+S[i_idx,jm1]+S[i_idx,jp1])
            S[i_idx, j_idx] = 0
            E=E+e_add

    return E #factor of two to account for double counting.
def metropolis(E1,E2,beta):
    # walk based off of the metropolis condition
    mf=np.exp((E1-E2)*beta)
    if  mf>1:
        return True
    elif mf > np.random.rand():
        return True
    else:
        return False

def metropolis_temperature(beta1,E1,beta2,E2):
    mf = np.exp((E1 - E2) * (beta1 - beta2))
    if mf > 1:
        return True
    elif mf > np.random.rand():
        return True
    else:
        return False