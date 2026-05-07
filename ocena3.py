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
az4, az3, az2, az1, az0 = 1, a, b, c, d +k


wyznacznikz1 = az3
wyznacznikz2 = (az3 * az2) - (az4 * az1)
wyznacznikz3 = az3 * ((az2 * az1) - (az3 * az0)) - az1 * (az4 * az1)
wyznacznikz4 = az0 * wyznacznikz3

if wyznacznikz1 > 0 and wyznacznikz2 > 0 and wyznacznikz3 > 0 and wyznacznikz4 > 0:
    print("Układ zamknięty jest stabilny.")
else:
    print("Układ zamknięty jest niestabilny.")