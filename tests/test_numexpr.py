import time
import numpy as np
import numexpr as ne

PI = 3.1415926
Fc = 1.27e9
K = -1.03e12
Ns = 4096
t = np.linspace(-1, 1, Ns)

N = 100000

timenp = time.time()
for n in range(N):
    mf1 = np.exp(2j * PI * Fc * t - 1j * PI * K * (t**2))
timenp = time.time() - timenp


timene = time.time()
for n in range(N):
    mf2 = ne.evaluate('exp(2j * PI * Fc * t - 1j * PI * K * (t**2))')
timene = time.time() - timene


print(np.sum(mf1 - mf2))

print(timenp, timene)
