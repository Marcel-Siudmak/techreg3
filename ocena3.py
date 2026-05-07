import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

# Parametry z tabeli dla Włodarczyk Siudmak
k = 13

# ==========================================
# 1. Kryterium Hurwitza - obliczenia
# ==========================================
print("--- Układ otwarty ---")
# Mianownik układu otwartego: s^4 + a*s^3 + b*s^2 + c*s + d
a4, a3, a2, a1, a0 = 1, 10, 35, 50, 24

D1_otw = a3
D2_otw = a3*a2 - a4*a1
D3_otw = a3*a2*a1 - a4*(a1**2) - (a3**2)*a0
D4_otw = a0 * D3_otw

print(f"Wyznaczniki Hurwitza: D1={D1_otw}, D2={D2_otw}, D3={D3_otw}, D4={D4_otw}")
if D1_otw > 0 and D2_otw > 0 and D3_otw > 0 and D4_otw > 0:
    print("Układ otwarty jest stabilny.")
else:
    print("Układ otwarty jest niestabilny.")


print("\n--- Układ zamknięty ---")
# Mianownik układu zamkniętego: s^4 + a*s^3 + b*s^2 + c*s + (d + k)
a0_zam = a0 + k

D1_zam = a3
D2_zam = a3*a2 - a4*a1
D3_zam = a3*a2*a1 - a4*(a1**2) - (a3**2)*a0_zam
D4_zam = a0_zam * D3_zam

print(f"Wyznaczniki Hurwitza: D1={D1_zam}, D2={D2_zam}, D3={D3_zam}, D4={D4_zam}")
if D1_zam > 0 and D2_zam > 0 and D3_zam > 0 and D4_zam > 0:
    print("Układ zamknięty jest stabilny.")
else:
    print("Układ zamknięty jest niestabilny.")


# ==========================================
# 2. Wzmocnienie w stanie ustalonym
# ==========================================
# Dla s -> 0 (z twierdzenia o wartości granicznej)
k_ust_otw = k / a0
k_ust_zam = k / (a0 + k)

print(f"\nWzmocnienie w stanie ustalonym (otwarty): {k_ust_otw:.4f}")
print(f"Wzmocnienie w stanie ustalonym (zamknięty): {k_ust_zam:.4f}")


# ==========================================
# 3. Rysowanie odpowiedzi skokowych
# ==========================================
t = np.linspace(0, 15, 1000)

# Definicja transmitancji do symulacji skoku
sys_otw = signal.TransferFunction([k], [1, a3, a2, a1, a0])
sys_zam = signal.TransferFunction([k], [1, a3, a2, a1, a0_zam])

# Obliczenie odpowiedzi skokowych
t_otw, y_otw = signal.step(sys_otw, T=t)
t_zam, y_zam = signal.step(sys_zam, T=t)

# Wykres dla układu otwartego
plt.plot(t_otw, y_otw, label='Układ otwarty', color='blue')
plt.axhline(k_ust_otw, color='blue', linestyle='--', label=f'Stan ustalony otw. = {k_ust_otw:.3f}')

# Wykres dla układu zamkniętego
plt.plot(t_zam, y_zam, label='Układ zamknięty', color='red')
plt.axhline(k_ust_zam, color='red', linestyle='--', label=f'Stan ustalony zam. = {k_ust_zam:.3f}')

# Estetyka wykresu (zgodna z Twoją)
plt.axhline(0, color='black')
plt.axvline(0, color='black')
plt.title('Odpowiedzi skokowe układów - Ocena 3.0')
plt.xlabel('Czas [s]')
plt.ylabel('Amplituda')
plt.grid()
plt.legend()
plt.show()