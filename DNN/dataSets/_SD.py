import numpy as np
import math as math
from heapq import nsmallest


def sphereDecoding(m,n,H,s,x,variance,pltBabai = [],pltAlgo = [],QAM = 4) :
    INF = 1000111000111
    alpha = 1.5   
    d = alpha * variance * n
    # print("Algorithm est for radius = ",np.sqrt(d))
    babaiB = np.floor(np.dot(np.linalg.pinv(H),x))
    babaiD = np.linalg.norm(x-np.dot(H,babaiB))
    # print("Babai est for radius =",babaiD)
    pltBabai.append(babaiD)
    
    q1 = np.zeros((n,m),dtype='complex')
    res = np.linalg.qr(H)
    R = res[1]
    q1 = res[0]

    y = np.dot(q1.conj().T,x)
    _y = y.copy()
 
    D = np.zeros(m)
    UB = np.zeros(m)
    k = m - 1
    D[k] = np.sqrt(d)
    setUB = 1
    flopsCount = 0
    ans = INF
    answer = np.zeros(m)
    li = []
    ###Start
    for _ in range(0,10) :
        k = m - 1
        _y = y.copy()
        D = np.zeros(m)
        UB = np.zeros(m)
        D[k] = np.sqrt(d)
        setUB = 1
        while True :
            flopsCount += 1
            if setUB == 1:
                if (D[k] + _y[k]) / R[k][k] > (-D[k] + _y[k]) / R[k][k]  : 
                   
                    UB[k] = np.floor((D[k] + _y[k]) / R[k][k])
                    s[k] = np.ceil((-D[k] + _y[k]) / R[k][k])  - 1  
                else :
                    UB[k] = np.floor((-D[k] + _y[k]) / R[k][k])
                    s[k] = np.ceil((D[k] + _y[k]) / R[k][k])  - 1
                te = s[k] + 1
                for j in range(QAM - 1, -QAM , -2):
                    flopsCount += 1
                    if te > j : 
                        break
                    s[k] = j - 2
            s[k] = s[k] + 2
            # print(k,s[k],UB[k])
            setUB = 0
            if s[k] <= UB[k] and s[k] < QAM:
                if k == 0 :
                    li.append(np.linalg.norm(np.dot(H,s)-x))
                    if ans > np.linalg.norm(np.dot(H,s)-x):
                        ans = np.linalg.norm(np.dot(H,s)-x)
                        answer = s.copy()
                        # print("***",ans,answer)
                    # print(s,np.linalg.norm(np.dot(H,s.T)-x.T) )
                else :
                    k = k - 1
                    _y[k] = y[k]
                    for i in range(k+1,m) :
                        # flopsCount += 1
                        _y[k] -= (R[k][i] * s[i])
                
                    D[k] = np.sqrt(D[k+1]**2 - (_y[k+1] - R[k+1][k+1] * s[k+1])**2)
                    setUB = 1
                continue
            else : 
                k = k + 1
                if k == m :
                    break
                    
        if ans == INF :
            print("The Radius is not big enough")
            d *= alpha
            print(np.sqrt(d))
        else :
            pltAlgo.append(d)
            break
    print(len(li))
    while len(li) < 3 : 
        li.append(np.sqrt(d))
    li = nsmallest(3,li)
    # print(li)
    # return ans,answer,li
    return li