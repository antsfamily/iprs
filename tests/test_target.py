import numpy as np


PI = np.pi
C = 3e8

H = 10e3
V = 150

Ad = 15 * PI / 180
As = 0 * PI / 180
Ab = 0.3 * PI / 180


Rbc = H / np.sin(Ad)

R0 = Rbc * np.cos(As)


Xc = np.sqrt(np.abs(R0**2 - H**2))
Yc2 = Rbc**2 - H**2 - Xc**2
Yc = np.sqrt(np.max([Yc2, 0]))


print("Rbc, R0: ", Rbc, R0)
print("Xc, Yc: ", Xc, Yc)


targets = [
    # [0, 0, 0, 0, 0, 0, 1],
    # [0, 30, 0, 0, 0, 0, 1],
    [100, 60, 0, 0, 0, 0, 1],

]


targets = np.array(targets)
targets = targets.astype('float')
targets[:, 0] = targets[:, 0] + Xc
targets[:, 1] = targets[:, 1] + Yc

print(targets)
