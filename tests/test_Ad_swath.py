import numpy as np

c = 3e8

H = 793e3
# FPr = 45e3
FPr = 10e3
X = 2600e3

Fsr = 32.317e+6
Nsr = 9280
Nsr = 2048


Rmin = np.sqrt(H**2 + X**2)
Rmax = np.sqrt(H**2 + (X + FPr)**2)
print("Rmin, Rmax: ", Rmin, Rmax)
print("t1, t2: ", Rmin / c, Rmax / c)
print("Rmax - Rmin: ", Rmax - Rmin)

Ts = 2 * (Rmax - Rmin) / c
print("Ts: ", Ts)
print("Ts: ", Nsr / Fsr)


theta1 = np.arctan(X / H) * 180 / np.pi
theta2 = np.arctan((X + FPr) / H) * 180 / np.pi
print("theta1: ", theta1)
print("theta2: ", theta2)

thetaBW = theta2 - theta1
print("thetaBW: ", thetaBW)

FPr = Rmin**2 + Rmax**2 - 2 * Rmin * Rmax * np.cos(thetaBW * np.pi / 180)
FPr = np.sqrt(FPr)

print("FPr: ", FPr)
