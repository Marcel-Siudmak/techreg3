import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

# Parametry z tabeli
a, b, c, d = 10, 35, 50, 24
k_nominalne = 13

# ==========================================
# 1. Częstotliwość i wzór wielomianu M(jw)
# ==========================================
# Dobieramy zakres tak, aby ładnie uchwycić przejścia przez osie
w = np.linspace(0, 5, 2000) 
M = (1j*w)**4 + a*(1j*w)**3 + b*(1j*w)**2 + c*(1j*w) + d

# ==========================================
# 2. Obliczenie kąta (argumentu w radianach)
# ==========================================
kat = np.unwrap(np.angle(M))

# ==========================================
# 3. Rysowanie - Krzywa Michajłowa
# ==========================================
plt.plot(np.real(M), np.imag(M), color='blue')
plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)
plt.title('Krzywa Michajłowa dla układu otwartego')
plt.xlabel('Re')
plt.ylabel('Im')
plt.grid(True)
plt.show()

# ==========================================
# 4. Wyświetlenie wykresu zmiany kąta
# ==========================================
plt.plot(w, kat, color='green')
plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)
plt.title('Zmiana argumentu funkcji M(jω)')
plt.xlabel('ω [rad/s]')
plt.ylabel('Argument [rad]')
plt.grid(True)
plt.show()

# ==========================================
# 5. Wpływ parametru k na odp. skokową (Symulacja)
# ==========================================
t = np.linspace(0, 15, 1000)

# Testujemy dla k mniejszego, nominalnego i znacznie większego
wartosci_k = [1, 13, 50]

for k_test in wartosci_k:
    # Transmitancja układu otwartego: K_otw(s) = k / (s^4 + a*s^3 + b*s^2 + c*s + d)
    sys_otw = signal.TransferFunction([k_test], [1, a, b, c, d])
    t_out, y_out = signal.step(sys_otw, T=t)
    plt.plot(t_out, y_out, label=f'k = {k_test}')

plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)
plt.title('Wpływ parametru k na odpowiedź układu otwartego')
plt.xlabel('Czas [s]')
plt.ylabel('Amplituda')
plt.legend()
plt.grid(True)
plt.show()