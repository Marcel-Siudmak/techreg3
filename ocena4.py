import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import os

# Tworzymy folder na wykresy dla oceny 4.0
folder_name = "wykresy_4_0"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Twoje parametry z tabeli (Włodarczyk Siudmak)
a = 10
b = 35
c = 50
d = 24
k0 = 13

print("--- ZADANIE NA OCENĘ 4.0 ---")

# ==========================================
# 1. KRYTERIUM MIKHAJŁOWA DLA UKŁADU OTWARTEGO
# ==========================================

# Tworzymy wektor częstotliwości omega (w). Od 0 do 10 wystarczy, by zobaczyć przecięcia osi.
w = np.linspace(0, 10, 5000)

# Część rzeczywista P(w) i urojona Q(w) ze wzoru M(jw)
P_w = w**4 - b * w**2 + d
Q_w = c * w - a * w**3

# Tworzymy wektor liczb zespolonych, co ułatwi nam policzenie kąta (argumentu)
M_jw = P_w + 1j * Q_w

# Liczymy argument (kąt) i używamy unwrap, żeby gładko rósł, a nie skakał od -pi do pi
kat_rad = np.unwrap(np.angle(M_jw))

# --- Rysowanie wykresów Mikhajłowa ---
fig_mikh, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Wykres 1: Hodograf Mikhajłowa (Re vs Im)
ax1.plot(P_w, Q_w, color='blue', label='M(jω)')
ax1.plot(P_w[0], Q_w[0], 'ro', label='ω=0 (Start)') # Zaznaczamy początek
ax1.axhline(0, color='black', linewidth=1)
ax1.axvline(0, color='black', linewidth=1)
ax1.set_title("Wykres Mikhajłowa (Hodograf)")
ax1.set_xlabel("Część rzeczywista Re")
ax1.set_ylabel("Część urojona Im")
ax1.grid(True)
ax1.legend()

# Wykres 2: Zmiana argumentu (kąta)
ax2.plot(w, kat_rad, color='green', label='arg M(jω)')
ax2.axhline(2 * np.pi, color='red', linestyle='--', label='Cel dla 4 rzędu: 2π')
ax2.set_title("Zmiana argumentu funkcji")
ax2.set_xlabel("Częstotliwość ω")
ax2.set_ylabel("Kąt [rad]")
ax2.grid(True)
ax2.legend()

plt.tight_layout()
plt.savefig(os.path.join(folder_name, "mikhajlow_otwarty.pdf"))
plt.show()


# ==========================================
# 2. WPŁYW PARAMETRU K NA ODPOWIEDŹ SKOKOWĄ I STABILNOŚĆ
# ==========================================

# Z kryterium Hurwitza obliczyliśmy analitycznie granicę:
k_graniczne = (a * b * c - (a**2) * d - c**2) / (a**2)
print(f"Obliczona analitycznie granica stabilności k: {k_graniczne}")

# Sprawdzimy to symulacyjnie na wykresie.
# Bierzemy k = 13 (Twoje bazowe), potem rosnące, i w końcu 127 (które powinno wybuchnąć)
wartosci_k = [13, 50, 100, 125, 127]

plt.figure(figsize=(10, 6))

# Pętla: dla każdego wybranego k liczymy transmitancję ZAMKNIĘTĄ i rysujemy jej wykres
for k_test in wartosci_k:
    licznik = [k_test]
    # Pamiętamy o d + k w wyrazie wolnym mianownika układu zamkniętego!
    mianownik = [1, a, b, c, d + k_test] 
    
    system = signal.TransferFunction(licznik, mianownik)
    # T=np.linspace wymusza obliczenia do 15 sekundy, żeby ładnie było widać wykresy
    t, y = signal.step(system, T=np.linspace(0, 15, 1000))
    
    plt.plot(t, y, label=f'k = {k_test}')

plt.title("Wpływ parametru k na odpowiedź skokową układu zamkniętego")
plt.xlabel("Czas [s]")
plt.ylabel("Amplituda")
plt.ylim(-1, 3) # Ograniczamy oś Y, żeby "wybuchający" wykres nie zepsuł widoczności innych
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig(os.path.join(folder_name, "wplyw_k_na_stabilnosc.pdf"))
plt.show()