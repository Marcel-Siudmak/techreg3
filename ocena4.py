import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

# Parametry z tabeli
a, b, c, d = 10, 35, 50, 24
k_nominalne = 13

# ==========================================
# 1. Częstotliwość i wzór wielomianu M(jω) — mianownik K(s), kryterium Michajłowa
# ==========================================
# Analitycznie: M(jω) = (jω)^4 + a(jω)^3 + b(jω)^2 + c(jω) + d
#            = (ω^4 - b ω^2 + d) + j(-a ω^3 + c ω)
# Dobieramy zakres tak, aby uchwycić przejścia przez osie
w = np.linspace(0, 5, 2000)
M = (1j * w) ** 4 + a * (1j * w) ** 3 + b * (1j * w) ** 2 + c * (1j * w) + d

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

# k mniejsze, nominalne (z tabeli), większe
wartosci_k = [1, k_nominalne, 50]

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

# Wniosek (Michajłow): dla stabilnego wielomianu stopnia n krzywa M(jω)
# obraca się monotonicznie o n·π/2 przy ω: 0→∞ (tu n=4 → 2π).
p_ocw = np.roots([1, a, b, c, d])
print("\n[Ocena 4] Bieguny układu otwartego (pierwiastki D(s)=s^4+as^3+bs^2+cs+d):")
print(p_ocw)
print("Wszystkie Re(p)<0:", np.all(np.real(p_ocw) < 0), "→ Michajłow: układ otwarty stabilny.")
print(
    "Uwaga: k nie występuje w D(s), więc stabilność biegunowa OL nie zależy od k — "
    "odpowiedź na «dla jakich k przestaje być stabilny?»: przy tym D(s) — dla żadnego k>0 "
    "(zmienia się tylko skala odpowiedzi skokowej pętli k/D)."
)