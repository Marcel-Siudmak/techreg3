import os

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

GRAFIKI_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "grafiki")
os.makedirs(GRAFIKI_DIR, exist_ok=True)


def zapisz_wykres_wektorowo(nazwa_pliku: str, fig=None) -> str:
    sciezka = os.path.join(GRAFIKI_DIR, nazwa_pliku)
    if not sciezka.lower().endswith((".svg", ".pdf", ".eps")):
        sciezka += ".svg"
    fmt = sciezka.rsplit(".", 1)[-1]
    (fig or plt.gcf()).savefig(sciezka, format=fmt, bbox_inches="tight")
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

re_p, im_p = np.real(K_otw), np.imag(K_otw)
# Pełny kontur Nyquista: ω>0 oraz odbicie symetryczne względem osi Re (ω<0)
re_all = np.concatenate([re_p, re_p])
im_all = np.concatenate([im_p, -im_p])

fig_n, ax_n = plt.subplots(figsize=(8, 7))
ax_n.plot(re_p, im_p, color="blue", label="K_otw(jω) dla ω > 0")
ax_n.plot(re_p, -im_p, color="blue", linestyle="--", alpha=0.5, label="Odbicie (ω < 0)")
ax_n.plot(-1, 0, marker="+", color="red", markersize=12, mew=2, label="Punkt (-1, j0)")
ax_n.axhline(0, color="black", linewidth=1)
ax_n.axvline(0, color="black", linewidth=1)
ax_n.set_title("Wykres Nyquista układu otwartego")
ax_n.set_xlabel("Re")
ax_n.set_ylabel("Im")
ax_n.grid(True)
ax_n.legend()

rm, rM = float(np.min(re_all)), float(np.max(re_all))
imn, imx = float(np.min(im_all)), float(np.max(im_all))
span = max(rM - rm, imx - imn, 0.25)
pad = 0.12 * span
xmin = min(rm - pad, -1.0 - pad)
xmax = max(rM + pad, -1.0 + pad, 0.08)
ymin = imn - pad
ymax = imx + pad
ax_n.set_xlim(xmin, xmax)
ax_n.set_ylim(ymin, ymax)
ax_n.set_aspect("equal", adjustable="box")

print("Zapis:", zapisz_wykres_wektorowo("ocena5_wykres_nyquista.svg", fig=fig_n))

# ==========================================
# 2. Wykres zmiany argumentu 1 + K_otw(jω)
# ==========================================
# Faza zmienia się tylko o ~0,37 rad — przy „wysokim” oknie wykresu dominuje puste pole.
# Wąski, szeroki rysunek + ciasne ylim + druga oś w stopniach.
w_arg = np.logspace(-1.2, 1.65, 4000)
D_arg = (1j * w_arg) ** 4 + a * (1j * w_arg) ** 3 + b * (1j * w_arg) ** 2 + c * (1j * w_arg) + d
M_zam = 1 + k_nominalne / D_arg
kat_zam = np.unwrap(np.angle(M_zam))

fig_a, ax_a = plt.subplots(figsize=(10, 2.85), layout="constrained")
ax_a.plot(w_arg, kat_zam, color="green", lw=1.4)
ax_a.axhline(0, color="black", linewidth=0.8)
ax_a.axvline(0, color="black", linewidth=0.8)
ax_a.set_xscale("log")
ax_a.set_title("Zmiana argumentu funkcji 1 + K_otw(jω)")
ax_a.set_xlabel("ω [rad/s] (skala log)")
ax_a.set_ylabel("Argument [rad]")
ax_a.grid(True, which="both", ls="-", alpha=0.35)
ax_a.grid(True, which="minor", ls=":", alpha=0.2)
kz0, kz1 = float(np.min(kat_zam)), float(np.max(kat_zam))
marg = 0.035
ax_a.set_ylim(kz0 - marg, kz1 + marg)
ax_a.set_xlim(float(w_arg[0]), float(w_arg[-1]))
ax_deg = ax_a.secondary_yaxis("right", functions=(np.rad2deg, np.deg2rad))
ax_deg.set_ylabel("Argument [°]")

print("Zapis:", zapisz_wykres_wektorowo("ocena5_argument_1_plus_Kotw_jomega.svg", fig=fig_a))

# ==========================================
# 3. Wpływ parametru k na układ zamknięty
# ==========================================
# Mianownik układu zamkniętego: D(s)+k. Z tablicy Routha (wiersz przy s^1) zeruje się przy:
# k_kryt = c*(a*b - c) / a^2 - d  (dla mianownika s^4 + a s^3 + b s^2 + c s + (d+k))
k_kryt = c * (a * b - c) / (a**2) - d

# k nominalne, podwyższone, blisko granicy, na granicy i powyżej (niestabilnie)
wartosci_k_zam = [k_nominalne, 60, 100, k_kryt, k_kryt + 9]
t_zam = np.linspace(0, 20, 2000)

fig_z, ax_z = plt.subplots(figsize=(10, 6))
for k_test in wartosci_k_zam:
    # Mianownik układu zamkniętego to: s^4 + as^3 + bs^2 + cs + (d + k)
    sys_zam = signal.TransferFunction([k_test], [1, a, b, c, d + k_test])
    t_out, y_out = signal.step(sys_zam, T=t_zam)
    ax_z.plot(t_out, y_out, label=f"k = {k_test}")

ax_z.axhline(0, color="black", linewidth=1)
ax_z.axvline(0, color="black", linewidth=1)
ax_z.set_title(f"Wpływ k na układ ZAMKNIĘTY (k krytyczne ≈ {k_kryt:.4g})")
ax_z.set_xlabel("Czas [s]")
ax_z.set_ylabel("Amplituda")
ax_z.set_ylim(-2, 3)
ax_z.legend(loc="upper right")
ax_z.grid(True)

print("Zapis:", zapisz_wykres_wektorowo("ocena5_wplyw_k_odpowiedz_skokowa_zamkniety.svg", fig=fig_z))
plt.show()

p_ol = np.roots([1, a, b, c, d])
P = int(np.sum(np.real(p_ol) > 0))
print("\n[Ocena 5] Nyquist dla k = k_nominalne: P =", P, "(bieguny układu otwartego w prawej półpłaszczyźnie; tu brak).")
print("Locus nie obejmuje (-1, j0) destabilizująco → układ zamknięty stabilny dla k <", f"{k_kryt:.6g}.")
print("k krytyczne (Routh, mianownik zamknięty D(s)+k):", f"{k_kryt:.6g}")
print("Dla k >", f"{k_kryt:.6g}", "układ zamknięty traci stabilność.")