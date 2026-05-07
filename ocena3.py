import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

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

# Tworzymy siatke wykresów
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Definicja transmitancji G_otw(s) = 13 / (s^4 + 10s^3 + 35s^2 + 50s + 24)
licznik_otw = [k]
mianownik_otw = [ao4, ao3, ao2, ao1, ao0]
system_otw = signal.TransferFunction(licznik_otw, mianownik_otw)

# Obliczamy odpowiedź skokową
t_otw, y_otw = signal.step(system_otw)

# Rysowanie na ax1
ax1.plot(t_otw, y_otw, label='Odpowiedź układu otwartego', color='red')

# Pozioma linia oznaczajaca obliczone wzmocnienie
ax1.axhline(y=wzmocnienie_otwarte, color='blue', linestyle='--', label=f'Wzmocnienie: {wzmocnienie_otwarte:.3f}')

# Formatowanie wykresu 1
ax1.set_title('Odpowiedź skokowa - Układ Otwarty')
ax1.set_ylabel('Amplituda')
ax1.grid(True)
ax1.legend()

# Definicja transmitancji G_zam(s) = 13 / (s^4 + 10s^3 + 35s^2 + 50s + 37
licznik_zam = [k]
mianownik_zam = [az4, az3, az2, az1, az0]
system_zam = signal.TransferFunction(licznik_zam, mianownik_zam)

# Obliczamy odpowiedź skokowaą
t_zam, y_zam = signal.step(system_zam)

# Rysowanie na ax2
ax2.plot(t_zam, y_zam, label='Odpowiedź układu zamkniętego', color='red')

# Pozioma linia oznaczająca obliczone wzmocnienie
ax2.axhline(y=wzmocnienie_zamkniete, color='blue', linestyle='--', label=f'Wzmocnienie: {wzmocnienie_zamkniete:.3f}')

# Formatowanie wykresu 2
ax2.set_title('Odpowiedź skokowa - Układ Zamknięty')
ax2.set_ylabel('Amplituda')
ax2.grid(True)
ax2.legend()


# Wyświetlenie
plt.tight_layout()
plt.show()

