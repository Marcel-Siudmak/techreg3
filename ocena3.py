import os

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

# Grafika wektorowa (SVG) — wspólny folder dla wszystkich zadań
GRAFIKI_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "grafiki")
os.makedirs(GRAFIKI_DIR, exist_ok=True)


def zapisz_wykres_wektorowo(nazwa_pliku: str, fig=None) -> str:
    """Zapisuje figurę do GRAFIKI_DIR jako SVG (lub inny format z rozszerzenia). fig=None → bieżąca."""
    sciezka = os.path.join(GRAFIKI_DIR, nazwa_pliku)
    if not sciezka.lower().endswith((".svg", ".pdf", ".eps")):
        sciezka += ".svg"
    fmt = sciezka.rsplit(".", 1)[-1]
    (fig or plt.gcf()).savefig(sciezka, format=fmt, bbox_inches="tight")
    return sciezka

# Parametry z tabeli 
a = 10
b = 35
c = 50
d = 24
k = 13

# Stabilność układu otwartego (wszystkie współczynniki są dodatnie)
ao4, ao3, ao2, ao1, ao0 = 1, a, b, c, d

wyznaczniko1 = ao3
wyznaczniko2 = (ao3 * ao2) - (ao4 * ao1)
wyznaczniko3 = ao3 * ((ao2 * ao1) - (ao3 * ao0)) - ao1 * (ao4 * ao1)
wyznaczniko4 = ao0 * wyznaczniko3

if wyznaczniko1 > 0 and wyznaczniko2 > 0 and wyznaczniko3 > 0 and wyznaczniko4 > 0:
    print("Układ otwarty jest stabilny.")
else:
    print("Układ otwarty jest niestabilny.")

# Stabilność układu zamkniętego
az4, az3, az2, az1, az0 = 1, a, b, c, d + k


wyznacznikz1 = az3
wyznacznikz2 = (az3 * az2) - (az4 * az1)
wyznacznikz3 = az3 * ((az2 * az1) - (az3 * az0)) - az1 * (az4 * az1)
wyznacznikz4 = az0 * wyznacznikz3

if wyznacznikz1 > 0 and wyznacznikz2 > 0 and wyznacznikz3 > 0 and wyznacznikz4 > 0:
    print("Układ zamknięty jest stabilny.")
else:
    print("Układ zamknięty jest niestabilny.")


# Wzmocnienie ustalone układu otwartego i zamkniętego (S = 0)

wzmocnienie_otwarte = k / d
wzmocnienie_zamkniete = k / (d + k)

print(f"Wzmocnienie ustalone układu otwartego (S = 0): {wzmocnienie_otwarte:.3f}")
print(f"Wzmocnienie ustalone układu zamkniętego (S = 0): {wzmocnienie_zamkniete:.3f}")

# Definicja transmitancji G_otw(s) = k / (s^4 + … + d)
licznik_otw = [k]
mianownik_otw = [ao4, ao3, ao2, ao1, ao0]
system_otw = signal.TransferFunction(licznik_otw, mianownik_otw)
t_otw, y_otw = signal.step(system_otw)

fig_otw, ax_otw = plt.subplots(figsize=(10, 5))
ax_otw.plot(t_otw, y_otw, label="Odpowiedź układu otwartego", color="red")
ax_otw.axhline(y=wzmocnienie_otwarte, color="blue", linestyle="--", label=f"Wzmocnienie: {wzmocnienie_otwarte:.3f}")
ax_otw.set_title("Odpowiedź skokowa — układ otwarty")
ax_otw.set_xlabel("Czas [s]")
ax_otw.set_ylabel("Amplituda")
ax_otw.grid(True)
ax_otw.legend()
fig_otw.tight_layout()
sciezka_otw = zapisz_wykres_wektorowo("ocena3_odpowiedz_skokowa_ol.svg", fig=fig_otw)
print(f"Wykres (wektorowy) zapisany: {sciezka_otw}")

# Definicja transmitancji układu zamkniętego
licznik_zam = [k]
mianownik_zam = [az4, az3, az2, az1, az0]
system_zam = signal.TransferFunction(licznik_zam, mianownik_zam)
t_zam, y_zam = signal.step(system_zam)

fig_zam, ax_zam = plt.subplots(figsize=(10, 5))
ax_zam.plot(t_zam, y_zam, label="Odpowiedź układu zamkniętego", color="red")
ax_zam.axhline(y=wzmocnienie_zamkniete, color="blue", linestyle="--", label=f"Wzmocnienie: {wzmocnienie_zamkniete:.3f}")
ax_zam.set_title("Odpowiedź skokowa — układ zamknięty")
ax_zam.set_xlabel("Czas [s]")
ax_zam.set_ylabel("Amplituda")
ax_zam.grid(True)
ax_zam.legend()
fig_zam.tight_layout()
sciezka_zam = zapisz_wykres_wektorowo("ocena3_odpowiedz_skokowa_zamkniety.svg", fig=fig_zam)
print(f"Wykres (wektorowy) zapisany: {sciezka_zam}")
plt.show()

