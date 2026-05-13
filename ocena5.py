import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import os

# Włączenie profesjonalnego stylu wykresów 
try:
    plt.style.use("seaborn-v0_8-whitegrid")
except:
    plt.style.use("seaborn-whitegrid") # Fallback dla starszych wersji Matplotlib

# Tworzymy folder na wykresy dla oceny 5.0
folder_name = "wykresy_5_0"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Nasze stałe parametry z tabeli
a = 10.0
b = 35.0
c = 50.0
d = 24.0
k0 = 13.0

# Granica stabilności obliczona wcześniej (126)
k_graniczne = 126.0

print("--- ZADANIE NA OCENĘ 5.0 (KRYTERIUM NYQUISTA) ---")

# ==========================================
# 1. PRZYGOTOWANIE DANYCH MATEMATYCZNYCH
# ==========================================
w = np.linspace(0.0, 60.0, 12000)

P_w = w**4 - b * w**2 + d
Q_w = c * w - a * w**3
M_jw = P_w + 1j * Q_w

# ==========================================
# 2. WYKRES NYQUISTA DLA POJEDYNCZEGO k (k = 13)
# ==========================================
K_otw_jw = k0 / M_jw
status_pojedynczy = "stabilny" if k0 < k_graniczne else "NIEstabilny"

plt.figure(figsize=(8, 6))
plt.plot(K_otw_jw.real, K_otw_jw.imag, color="#2b83ba", linewidth=2, label=f"k={k0:.2f} ({status_pojedynczy})")
plt.axhline(0.0, color="black", linewidth=1)
plt.axvline(0.0, color="black", linewidth=1)

plt.title(f"Wykres Nyquista (k={k0:.2f})")
plt.xlabel("Re")
plt.ylabel("Im")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(folder_name, "nyquist_pojedynczy.pdf"))
plt.show()

# ==========================================
# 3. ZMIANA ARGUMENTU DLA 1 + K_otw(jw)
# ==========================================
funkcja_arg = 1.0 + K_otw_jw
kat_rad = np.unwrap(np.angle(funkcja_arg))

plt.figure(figsize=(8, 6))
plt.plot(w, kat_rad, color="#1a9850", linewidth=2, label=r"$\Delta arg[1 + K_{otw}(j\omega)]$")
plt.axhline(0.0, color="red", linestyle="--", label="Granica stabilnosci (0 rad)")

plt.title("Zmiana argumentu 1 + K_otw(jw)")
plt.xlabel(r"$\omega$")
plt.ylabel("Kąt [rad]")
plt.xlim(left=0.0)
plt.margins(x=0)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(folder_name, "nyquist_argument.pdf"))
plt.show()

# ==========================================
# 4. WYKRES NYQUISTA DLA WIELU WARTOŚCI k
# ==========================================
wartosci_k = [-60.0, 0.0, 13.0, 50.0, 150.0, 300.0]

plt.figure(figsize=(12, 6))

for k_test in wartosci_k:
    K_test_jw = k_test / M_jw
    
    if k_test < k_graniczne:
        plt.plot(K_test_jw.real, K_test_jw.imag, linestyle="-", linewidth=2, label=f"k={k_test:.2f} (stabilny)")
    else:
        plt.plot(K_test_jw.real, K_test_jw.imag, linestyle="--", linewidth=2, label=f"k={k_test:.2f} (NIEstabilny)")

# Dodajemy czerwony krzyżyk ułożony na wierzchu (zorder=5)
plt.scatter([-1.0], [0.0], color="red", marker="x", s=80, zorder=5, label="punkt krytyczny (-1, 0)")
plt.axhline(0.0, color="black", linewidth=1)
plt.axvline(0.0, color="black", linewidth=1)

plt.title("Nyquisty dla k uzytych na wykresie odpowiedzi skokowej")
plt.xlabel("Re")
plt.ylabel("Im")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(folder_name, "nyquist_wiele_k.pdf"))
plt.show()

# ==========================================
# 5. WPŁYW PARAMETRU k NA ODPOWIEDŹ SKOKOWĄ (UKŁAD ZAMKNIĘTY)
# ==========================================

# Najpierw liczymy odpowiedź tylko dla STABILNYCH wartości k, żeby poznać ich max/min
y_stable_all = []
for k_test in wartosci_k:
    if k_test < k_graniczne:
        licznik = [k_test]
        mianownik = [1, a, b, c, d + k_test] 
        sys = signal.TransferFunction(licznik, mianownik)
        _, y = signal.step(sys, T=np.linspace(0, 12, 6000))
        y_stable_all.extend(y)

# Dynamiczne marginesy z proporcjonalnym paddingiem (10% marginesu - precyzyjny wzór)
if y_stable_all:
    y_lo = float(np.min(y_stable_all))
    y_hi = float(np.max(y_stable_all))
    pad = 0.1 * max(1e-9, y_hi - y_lo)
    y_lo -= pad
    y_hi += pad
else:
    y_lo, y_hi = -2.0, 2.0

plt.figure(figsize=(12, 6))

for k_test in wartosci_k:
    licznik = [k_test]
    mianownik = [1, a, b, c, d + k_test] 
    sys = signal.TransferFunction(licznik, mianownik)
    
    t, y = signal.step(sys, T=np.linspace(0, 12, 6000))
    
    if k_test < k_graniczne:
        # STABILNE: Gruba linia (lw=2.5), na samym wierzchu (zorder=10), żeby rzucały się w oczy
        plt.plot(t, y, linestyle="-", linewidth=2.5, zorder=10, label=f"k={k_test:.2f} (stabilny)")
    else:
        # NIESTABILNE: Cienkie, przerywane, PÓŁPRZEZROCZYSTE (alpha=0.35) i pod spodem (zorder=1)
        y_clipped = np.clip(y, y_lo, y_hi)
        plt.plot(t, y_clipped, linestyle="--", linewidth=1.5, alpha=0.35, zorder=1, label=f"k={k_test:.2f} (NIEstabilny, przyciety)")

plt.title("Wpływ parametru k na odpowiedź skokową (układ zamknięty)")
plt.xlabel("t [s]")
plt.ylabel("y(t)")
plt.xlim(0.0, 12.0)
plt.ylim(y_lo, y_hi)
plt.grid(True, linestyle="--", alpha=0.6)

# Dodajemy mocne białe tło pod legendą, żeby z tyłu nie przebijały "poszarpane" linie
plt.legend(frameon=True, framealpha=0.95, zorder=20)
plt.tight_layout()
plt.savefig(os.path.join(folder_name, "wplyw_k_uklad_zamkniety.pdf"))
plt.show()