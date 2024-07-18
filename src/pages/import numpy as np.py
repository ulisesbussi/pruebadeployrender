import numpy as np
from time import time,perf_counter
import matplotlib.pyplot as plt
#precise time measurement
from time import time


def fibbo(n):
    if n <=2:
        return 1
    else:
        return fibbo(n-1) + fibbo(n-2)

def fibbo2(n):
    a = 0
    b = 1
    for i in range(n):
        a, b = b, a+b
    return a

nemo = {}
def fibbo_memo(n):
    if n in nemo:
        return nemo[n]
    
    if n <=2:
        return 1
    else:
        res = fibbo_memo(n-1) + fibbo_memo(n-2)
    
    nemo[n] = res
    return res

t= []
tt = []
tn = []
for i in range(35):
    t0 = perf_counter()
    q=fibbo(i)
    t1 = perf_counter()
    w=fibbo2(i)
    t2 = perf_counter()
    e= fibbo_memo(i)
    t3 = perf_counter()
    t.append(t1-t0)
    tt.append(t2-t1)
    tn.append(t3-t2)


plt.plot(t)
plt.plot(tt)
plt.plot(tn)