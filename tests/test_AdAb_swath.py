import numpy as np

PI = np.pi

c = 3e8

H = 793e3
# FPr = 45e3
FPr = 10e3

Fsr = 32.317e+6
Nsr = 9280
Nsr = 2048

Ad = 53.3 * np.pi / 180.0
As = 1.58 * np.pi / 180.0
Ab = 1.0 * np.pi / 180.0  # Nsr = 9280
Ab = 0.7 * np.pi / 180.0  # Nsr = 2048

print(Ad, Ab, As)

Rbc = H / np.sin(Ad)
Rb0 = Rbc * np.cos(As)
Xc = np.sqrt(np.abs(Rb0**2 - H**2))
Yc2 = Rbc**2 - H**2 - Xc**2

Yc = np.sqrt(np.max([Yc2, 0]))

print("Rbc, Rb0: ", Rbc, Rb0)
print("Xc, Yc: ", Xc, Yc)


Rnear = H / np.sin(Ad + Ab / 2.0)
Rfar = H / np.sin(Ad - Ab / 2.0)
print("Ad, Ab, Rnear, Rfar: ", Ad, Ab, Rnear, Rfar)

Xmin = np.sqrt(Rnear**2 - H**2) * np.cos(As) - Xc
Xmax = np.sqrt(Rfar**2 - H**2) * np.cos(As) - Xc
print("Xmin, Xmax: ", Xmin, Xmax)
print("Xmax - Xmin: ", Xmax - Xmin)

FPr = np.sqrt(Rnear**2 + Rfar**2 - 2 * Rnear * Rfar * np.cos(Ab)) * np.cos(As)
print("FPr:       : ", FPr)


print("Rnear, Rfar: ", Rnear, Rfar)
print("t1, t2: ", Rnear / c, Rfar / c)
print("Rfar - Rnear: ", Rfar - Rnear)

Ts = 2 * (Rfar - Rnear) / c
print("Ts: ", Ts)
print("Ts: ", Nsr / Fsr)


print((998219.2919177823 - 980201.9061573319) / c)
print((993597.3447461982 - 984590.0526056099) / c)
