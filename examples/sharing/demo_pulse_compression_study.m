
% ===Generate tansmitted and recieved signals
% ---Setting parameters
R = [1.e3, 2.e3, 3.e3]
A = [0.5, 1.0, 0.8]

Kr = 4.1e+11
Tp = 37.0e-06
Br = abs(Kr) * Tp

alp = 1.24588  % 1.1-1.4
Fsr = alp * Br
Fc = 5.3e9
Fc = 0.

Tsr = 5.1 * Tp
Nsr = int(Fsr * Tsr)
t = linspace(-Tsr / 2., Tsr / 2, Nsr)
f = linspace(-Fsr / 2., Fsr / 2, Nsr)
fr = linspace(-Fsr / 2., Fsr / 2, Nsr)

% ---Transmitted signal
St = rect(t / Tp) * exp(2j * PI * Fc * t + 1j * PI * Kr * t ** 2)

% ---Recieved signal
Sr = 0.
for r, a in zip(R, A):
    tau = 2. * r / C
    ttau = t - tau
    Sr += a * rect(ttau / Tp) * exp(2j * PI * Fc * ttau + 1j * PI * Kr * ttau ** 2)


% ---Frequency domain
Yt = fftshift(fft(St), 0)
Yr = fftshift(fft(Sr), 0)

% ---Plot signals
plt.figure(figsize=(10, 8))
plt.subplot(221)
plt.plot(t * 1000, real(St))
plt.grid()
plt.title('Real part')
plt.xlabel('Time/ms')
plt.ylabel('Amplitude')
plt.subplot(222)
plt.plot(t * 1000, imag(St))
plt.grid()
plt.title('Imaginary part')
plt.xlabel('Time/ms')
plt.ylabel('Amplitude')
plt.subplot(223)
plt.plot(f, abs(Yt))
plt.grid()
plt.title('Spectrum')
plt.xlabel('Frequency/Hz')
plt.ylabel('Amplitude')
plt.subplot(224)
plt.plot(f, angle(Yt))
plt.grid()
plt.title('Spectrum')
plt.xlabel('Frequency/Hz')
plt.ylabel('Phase')
plt.subplots_adjust(left=0.08, bottom=0.06, right=0.98, top=0.96, wspace=0.19, hspace=0.25)

plt.show()


plt.figure(figsize=(10, 8))
plt.subplot(221)
plt.plot(t * 1000, real(Sr))
plt.grid()
plt.title('Real part')
plt.xlabel('Time/ms')
plt.ylabel('Amplitude')
plt.subplot(222)
plt.plot(t * 1000, imag(Sr))
plt.grid()
plt.title('Imaginary part')
plt.xlabel('Time/ms')
plt.ylabel('Amplitude')
plt.subplot(223)
plt.plot(f, abs(Yr))
plt.grid()
plt.title('Spectrum')
plt.xlabel('Frequency/Hz')
plt.ylabel('Amplitude')
plt.subplot(224)
plt.plot(f, angle(Yr))
plt.grid()
plt.title('Spectrum')
plt.xlabel('Frequency/Hz')
plt.ylabel('Phase')
plt.subplots_adjust(left=0.08, bottom=0.06, right=0.98, top=0.96, wspace=0.19, hspace=0.25)

plt.show()

% ===Matched filtering/Pulse compression in time domain

% ---Matched filtering signal
tm = t
Sm = rect(-tm / Tp) * exp(-2j * PI * Fc * tm - 1j * PI * Kr * tm ** 2)
% Sm = rect(t / Tp) * exp(-2j * PI * Fc * t - 1j * PI * Kr * t ** 2)
S1 = zeros(Nsr, dtype='complex')
ZB = zeros(Nsr - 1, dtype='complex')
ZA = zeros(Nsr - 1, dtype='complex')
Sp = hstack((ZB, St, ZA))
for n in range(Nsr):

    S1[n] = dot(Sp[n:n + Nsr], Sm[::-1])


% ===Matched filtering/Pulse compression in frequency domain
% ---Tansform the recieved signal to frequency domain
Yr = fftshift(fft(Sr), 0)
% ---Matched filter in frequency domain
H = iprs.rect(fr / (abs(Kr) * Tp)) * exp(1j * PI * fr**2 / Kr)
% ---Matched filtering/Pulse compression
Y = Yr * H
% ---Tansform back to time domain
S2 = ifftshift(ifft(Y), 0)

plt.figure(2)
plt.subplot(221)
plt.plot(t, abs(S1))
plt.grid()
plt.subplot(222)
plt.plot(t, abs(S2))
plt.grid()
plt.subplot(223)
plt.plot(f, abs(S1))
plt.grid()
plt.subplot(224)
plt.plot(f, abs(S2))
plt.grid()
plt.show()
