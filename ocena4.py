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

# Zwiększamy wektor częstotliwości omega (w) aż do 200, żeby wykres kąta się wypłaszczył
w = np.linspace(0, 200, 20000)

# Część rzeczywista P(w) i urojona Q(w) ze wzoru M(jw)
P_w = w**4 - b * w**2 + d
Q_w = c * w - a * w**3

# Tworzymy wektor liczb zespolonych, co ułatwi nam policzenie kąta (argumentu)
M_jw = P_w + 1j * Q_w

# Liczymy argument (kąt) i używamy unwrap, żeby gładko rósł, a nie skakał od -pi do pi
kat_rad = np.unwrap(np.angle(M_jw))

# --- Rysowanie WYKRESU 1: Hodograf Mikhajłowa ---
plt.figure(figsize=(8, 6))

# Trik: rysujemy hodograf tylko dla w <= 10, żeby wyglądał identycznie jak wcześniej!
maska = w <= 10 
plt.plot(P_w[maska], Q_w[maska], color='blue', label='M(jω)')
plt.plot(P_w[0], Q_w[0], 'ro', label='ω=0 (Start)') # Zaznaczamy początek
plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)
plt.title("Wykres Mikhajłowa (Hodograf)")
plt.xlabel("Część rzeczywista Re")
plt.ylabel("Część urojona Im")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(folder_name, "mikhajlow_hodograf.pdf"))
plt.show() # Pierwsze okno

# --- Rysowanie WYKRESU 2: Zmiana argumentu (kąta) ---
plt.figure(figsize=(8, 6))
plt.plot(w, kat_rad, color='green', label='arg M(jω)')
plt.axhline(2 * np.pi, color='red', linestyle='--', label='Cel dla 4 rzędu: 2π')
plt.title("Zmiana argumentu funkcji")
plt.xlabel("Częstotliwość ω")
plt.ylabel("Kąt [rad]")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(folder_name, "mikhajlow_argument.pdf"))
plt.show() # Drugie okno


# ==========================================
# 2. WPŁYW PARAMETRU K NA ODPOWIEDŹ SKOKOWĄ (UKŁAD OTWARTY)
# ==========================================

# Zestaw różnych wartości k do pokazania na wykresie
wartosci_k = [-50, 0, 13, 50, 150, 300]

plt.figure(figsize=(10, 6))

# Pętla: dla każdego wybranego k liczymy transmitancję UKŁADU OTWARTEGO
for k_test in wartosci_k:
    licznik = [k_test]
    # W układzie otwartym mianownik to zawsze [1, a, b, c, d] - nie dodajemy tu 'k'!
    mianownik = [1, a, b, c, d] 
    
    system = signal.TransferFunction(licznik, mianownik)
    
    # Skróciliśmy czas do 10s, żeby wykres był bardziej czytelny (jak u kolegów)
    t, y = signal.step(system, T=np.linspace(0, 10, 1000))
    
    plt.plot(t, y, label=f'k = {k_test}')

plt.title("Wpływ parametru k na odpowiedź skokową (układ otwarty)")
plt.xlabel("Czas [s]")
plt.ylabel("Amplituda")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(folder_name, "wplyw_k_uklad_otwarty.pdf"))
plt.show() # Trzecie okno