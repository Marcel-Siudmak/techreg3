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


# Parametry z tabeli
a, b, c, d = 10, 35, 50, 24
k_nominalne = 13

# ==========================================
# 1. Częstotliwość i wzór wielomianu M(jω) — mianownik K(s), kryterium Michajłowa
# ==========================================
# Analitycznie: M(jω) = (jω)^4 + a(jω)^3 + b(jω)^2 + c(jω) + d
#            = (ω^4 - b ω^2 + d) + j(-a ω^3 + c ω)
# ω do ~2.5 rad/s: dalej |M(jω)| bardzo szybko rośnie i krzywa „ucieka” — wykres byłby nieczytelny
w = np.linspace(0, 2.5, 3000)
M = (1j * w) ** 4 + a * (1j * w) ** 3 + b * (1j * w) ** 2 + c * (1j * w) + d

# ==========================================
# 2. Obliczenie kąta (argumentu w radianach)
# ==========================================
kat = np.unwrap(np.angle(M))

# ==========================================
# 3. Rysowanie - Krzywa Michajłowa (osobna figura — zapis SVG nie miesza wykresów)
# ==========================================
fig_m, ax_m = plt.subplots(figsize=(7, 6))
ax_m.plot(np.real(M), np.imag(M), color="blue")
ax_m.axhline(0, color="black", linewidth=1)
ax_m.axvline(0, color="black", linewidth=1)
ax_m.set_title("Krzywa Michajłowa dla układu otwartego (M(jω)=D(jω), ω∈[0, 2.5])")
ax_m.set_xlabel("Re M(jω)")
ax_m.set_ylabel("Im M(jω)")
ax_m.grid(True)
ax_m.set_aspect("equal", adjustable="box")
rm, rM = np.min(np.real(M)), np.max(np.real(M))
imn, imx = np.min(np.imag(M)), np.max(np.imag(M))
pad = 0.06 * max(rM - rm, imx - imn, 1.0)
ax_m.set_xlim(rm - pad, rM + pad)
ax_m.set_ylim(imn - pad, imx + pad)
print("Zapis:", zapisz_wykres_wektorowo("ocena4_krzywa_michajlowa.svg", fig=fig_m))

# ==========================================
# 4. Wykres zmiany argumentu M(jω)
# ==========================================
fig_a, ax_a = plt.subplots(figsize=(7, 5))
ax_a.plot(w, kat, color="green")
ax_a.axhline(0, color="black", linewidth=1)
ax_a.axvline(0, color="black", linewidth=1)
ax_a.set_title("Zmiana argumentu funkcji M(jω)")
ax_a.set_xlabel("ω [rad/s]")
ax_a.set_ylabel("Argument [rad]")
ax_a.grid(True)
kmin, kmax = np.min(kat), np.max(kat)
ax_a.set_ylim(kmin - 0.15 * max(abs(kmax - kmin), 1.0), kmax + 0.15 * max(abs(kmax - kmin), 1.0))
print("Zapis:", zapisz_wykres_wektorowo("ocena4_argument_M_jomega.svg", fig=fig_a))

# ==========================================
# 5. Wpływ parametru k na odp. skokową (Symulacja)
# ==========================================
t = np.linspace(0, 15, 1000)

# k mniejsze, nominalne (z tabeli), większe
wartosci_k = [1, k_nominalne, 50]

fig_s, ax_s = plt.subplots(figsize=(8, 5))
ymax = 0.0
for k_test in wartosci_k:
    # Transmitancja układu otwartego: K_otw(s) = k / (s^4 + a*s^3 + b*s^2 + c*s + d)
    sys_otw = signal.TransferFunction([k_test], [1, a, b, c, d])
    t_out, y_out = signal.step(sys_otw, T=t)
    ax_s.plot(t_out, y_out, label=f"k = {k_test}")
    ymax = max(ymax, float(np.max(y_out)))

ax_s.axhline(0, color="black", linewidth=1)
ax_s.axvline(0, color="black", linewidth=1)
ax_s.set_title("Wpływ parametru k na odpowiedź układu otwartego")
ax_s.set_xlabel("Czas [s]")
ax_s.set_ylabel("Amplituda")
ax_s.legend()
ax_s.grid(True)
ax_s.set_xlim(0, float(t[-1]))
ax_s.set_ylim(0, ymax * 1.08 + 1e-9)
print("Zapis:", zapisz_wykres_wektorowo("ocena4_wplyw_k_odpowiedz_skokowa_ol.svg", fig=fig_s))
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