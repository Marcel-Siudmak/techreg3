import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

# Parametry z tabeli Włodarczyk Siudmak
a, b, c, d = 10, 35, 50, 24
k_nominalne = 13

# ==========================================
# 1. Wykres Nyquista dla K_otw(jw)
# ==========================================
# Dla Nyquista używamy szerokiego zakresu częstotliwości (skala logarytmiczna)
w = np.logspace(-2, 2, 5000) 
K_otw = k_nominalne / ((1j*w)**4 + a*(1j*w)**3 + b*(1j*w)**2 + c*(1j*w) + d)

plt.figure(figsize=(8, 6))
# Rysujemy główny wykres (dla w > 0)
plt.plot(np.real(K_otw), np.imag(K_otw), color='blue', label='K_otw(jω) dla ω > 0')
# Rysujemy odbicie lustrzane (dla w < 0) - często wymagane na labach z TR
plt.plot(np.real(K_otw), -np.imag(K_otw), color='blue', linestyle='--', alpha=0.5, label='Odbicie lustrzane')

# Zaznaczamy kluczowy punkt krytyczny (-1, j0)
plt.plot(-1, 0, marker='+', color='red', markersize=12, mew=2, label='Punkt (-1, j0)')

plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)
plt.title('Wykres Nyquista układu otwartego')
plt.xlabel('Re')
plt.ylabel('Im')
plt.grid(True)
plt.legend()
plt.xlim(-1.5, 1.0)
plt.ylim(-1.0, 1.0)
plt.show()

# ==========================================
# 2. Wykres zmiany argumentu 1 + K_otw(jw)
# ==========================================
# Tworzymy wektor 1 + K_otw
M_zam = 1 + K_otw
kat_zam = np.unwrap(np.angle(M_zam))

plt.figure(figsize=(8, 6))
plt.plot(w, kat_zam, color='green')
plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)
plt.xscale('log') # Skala logarytmiczna osi X, bo zakres w jest ogromny
plt.title('Zmiana argumentu funkcji 1 + K_otw(jω)')
plt.xlabel('ω [rad/s] (skala log)')
plt.ylabel('Argument [rad]')
plt.grid(True)
plt.show()

# ==========================================
# 3. Wpływ parametru k na układ zamknięty
# ==========================================
# Wiemy ze wzorów z punktu 3.0, że przy k=126 wyznacznik D3 wynosi 0
k_kryt = 126

# Testujemy k nominalne, lekko podniesione, graniczne i za duże
wartosci_k_zam = [13, 60, 100, 126, 135]
t_zam = np.linspace(0, 20, 2000)

plt.figure(figsize=(10, 6))
for k_test in wartosci_k_zam:
    # Mianownik układu zamkniętego to: s^4 + as^3 + bs^2 + cs + (d + k)
    sys_zam = signal.TransferFunction([k_test], [1, a, b, c, d + k_test])
    t_out, y_out = signal.step(sys_zam, T=t_zam)
    plt.plot(t_out, y_out, label=f'k = {k_test}')

plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)
plt.title('Wpływ k na układ ZAMKNIĘTY (Krytyczne k = 126)')
plt.xlabel('Czas [s]')
plt.ylabel('Amplituda')
# Zawężamy oś Y, bo dla k > 126 układ rośnie w nieskończoność i zepsuje widok innych linii
plt.ylim(-2, 3) 
plt.legend(loc='upper right')
plt.grid(True)
plt.show()