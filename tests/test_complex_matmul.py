import numpy as np


def cmplx_matmul(A, B):
    Ar = np.real(A)
    Ai = np.imag(A)
    Br = np.real(B)
    Bi = np.imag(B)

    C = np.matmul(Ar, Br) - np.matmul(Ai, Bi) + 1j * \
        (np.matmul(Ar, Bi) + np.matmul(Ai, Br))
    return C


n = 3
A = np.random.rand(n, n) + 1j * np.random.rand(n, n)

print(A)

x = np.random.rand(n)


y1 = np.matmul(A, x)
y2 = cmplx_matmul(A, x)

print(y1)
print(y2)

print(np.abs(y1 - y2))
