import os

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

GRAFIKI_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "grafiki")
os.makedirs(GRAFIKI_DIR, exist_ok=True)


def zapisz_wykres_wektorowo(nazwa_pliku: str) -> str:
    sciezka = os.path.join(GRAFIKI_DIR, nazwa_pliku)
    if not sciezka.lower().endswith((".svg", ".pdf", ".eps")):
        sciezka += ".svg"
    fmt = sciezka.rsplit(".", 1)[-1]
    plt.savefig(sciezka, format=fmt, bbox_inches="tight")
    return sciezka


# Parametry z tabeli Włodarczyk Siudmak
a, b, c, d = 10, 35, 50, 24
k_nominalne = 13

# ==========================================
# 1. Wykres Nyquista dla K_otw(jω) = G(s)K(s)|_{s=jω} = k / D(jω)
# ==========================================
# Dla Nyquista używamy szerokiego zakresu częstotliwości (skala logarytmiczna)
w = np.logspace(-2, 2, 5000)
D_jw = (1j * w) ** 4 + a * (1j * w) ** 3 + b * (1j * w) ** 2 + c * (1j * w) + d
K_otw = k_nominalne / D_jw

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
# Oś Re musi obejmować punkt (-1, 0); druga granica — locus dla k_nominalne
margin = 0.15
re_min, re_max = np.min(np.real(K_otw)), np.max(np.real(K_otw))
im_min, im_max = np.min(np.imag(K_otw)), np.max(np.imag(K_otw))
plt.xlim(min(-1.2, re_min - margin), max(0.65, re_max + margin))
plt.ylim(im_min - margin, max(0.12, im_max + margin))
print("Zapis:", zapisz_wykres_wektorowo("ocena5_wykres_nyquista.svg"))
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
print("Zapis:", zapisz_wykres_wektorowo("ocena5_argument_1_plus_Kotw_jomega.svg"))
plt.show()

# ==========================================
# 3. Wpływ parametru k na układ zamknięty
# ==========================================
# Mianownik układu zamkniętego: D(s)+k. Z tablicy Routha (wiersz przy s^1) zeruje się przy:
# k_kryt = c*(a*b - c) / a^2 - d  (dla mianownika s^4 + a s^3 + b s^2 + c s + (d+k))
k_kryt = c * (a * b - c) / (a**2) - d

# k nominalne, podwyższone, blisko granicy, na granicy i powyżej (niestabilnie)
wartosci_k_zam = [k_nominalne, 60, 100, k_kryt, k_kryt + 9]
t_zam = np.linspace(0, 20, 2000)

plt.figure(figsize=(10, 6))
for k_test in wartosci_k_zam:
    # Mianownik układu zamkniętego to: s^4 + as^3 + bs^2 + cs + (d + k)
    sys_zam = signal.TransferFunction([k_test], [1, a, b, c, d + k_test])
    t_out, y_out = signal.step(sys_zam, T=t_zam)
    plt.plot(t_out, y_out, label=f'k = {k_test}')

plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)
plt.title(f'Wpływ k na układ ZAMKNIĘTY (k krytyczne ≈ {k_kryt:.4g})')
plt.xlabel('Czas [s]')
plt.ylabel('Amplituda')
# Zawężamy oś Y, bo dla k > k_kryt układ rośnie w nieskończoność i zepsuje widok innych linii
plt.ylim(-2, 3)
plt.legend(loc='upper right')
plt.grid(True)
print("Zapis:", zapisz_wykres_wektorowo("ocena5_wplyw_k_odpowiedz_skokowa_zamkniety.svg"))
plt.show()

p_ol = np.roots([1, a, b, c, d])
P = int(np.sum(np.real(p_ol) > 0))
print("\n[Ocena 5] Nyquist dla k = k_nominalne: P =", P, "(bieguny układu otwartego w prawej półpłaszczyźnie; tu brak).")
print("Locus nie obejmuje (-1, j0) destabilizująco → układ zamknięty stabilny dla k <", f"{k_kryt:.6g}.")
print("k krytyczne (Routh, mianownik zamknięty D(s)+k):", f"{k_kryt:.6g}")
print("Dla k >", f"{k_kryt:.6g}", "układ zamknięty traci stabilność.")