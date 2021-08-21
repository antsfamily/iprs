import numpy as np

PI = 3.1415926535898
EPS = 2.2e-32

c = 3e8

H = 10e3
Fsr = 32.317e+6
Nsr = 256

Ad = 30.0 * np.pi / 180.0
As = 1.58 * np.pi / 180.0
As = 22.8 * np.pi / 180.0
# Ab = 1.0 * np.pi / 180.0  # Nsr =
Ab = 0.89 * np.pi / 180.0  # Nsr =

print(Ad, Ab, As)

Rbc = H / (np.sin(Ad) + EPS)
Rb0 = Rbc * np.cos(As)
Xc = np.sqrt(np.abs(Rb0**2 - H**2))
Yc = Rbc * np.sin(As)

print("Rbc, Rb0: ", Rbc, Rb0)
print("Xc, Yc: ", Xc, Yc)


Rnear = H / np.sin(Ad + Ab / 2.0)
Rfar = H / np.sin(Ad - Ab / 2.0)
print("Ad, Ab, Rnear, Rfar: ", Ad, Ab, Rnear, Rfar)


Ynear = Rnear * np.sin(As)
Yfar = Rfar * np.sin(As)
Xnear = np.sqrt((Rnear * np.cos(As))**2 - H**2)
Xfar = np.sqrt((Rfar * np.cos(As))**2 - H**2)

print("Xnear %f, Xfar %f, Ynear %f, Yfar %f" % (Xnear, Xfar, Ynear, Yfar))

SA = [-100, 100, -100, 100]

SA[0] = Xnear - Xc
SA[1] = Xfar - Xc


print(SA)
