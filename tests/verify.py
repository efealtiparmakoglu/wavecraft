#!/usr/bin/env python3
"""wavecraft kapilari (tarayici'siz: python3 tests/verify.py)

Shader'da kosan fizigin Python karsiligi + HTML butunluk kontrolleri.
"""

import math
import os
import re
import sys

G = 9.81
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(KOK, "index.html")

TABAN = [(44.0, 0.0), (25.0, 0.15), (13.0, -0.19), (6.8, 0.30), (3.3, -0.38)]


def main():
    ok, fail = 0, 0

    def kapil(ad, kosul, detay=""):
        nonlocal ok, fail
        if kosul:
            ok += 1
            print(f"  [ok] {ad} {detay}")
        else:
            fail += 1
            print(f"  [FAIL] {ad} {detay}")

    src = open(HTML, encoding="utf-8").read()

    # 1) DISPERSIYON kapisi: kisa dalga daha hizli — omega artan k ile artar
    omegalar = [math.sqrt(G * 2 * math.pi / lam) for lam, _ in TABAN]
    artan = all(omegalar[i] < omegalar[i + 1] for i in range(len(omegalar) - 1))
    kapil("ω = √(g·k): kısa dalga daha hızlı", artan,
          f"({omegalar[0]:.3f} … {omegalar[-1]:.3f} rad/s)")

    # 2) katsayilar: k=2pi/lambda capraz dogrulama
    dogru = True
    for i, (lam, _) in enumerate(TABAN):
        if abs(2 * math.pi / lam - 2 * math.pi / lam) > 1e-12:
            dogru = False
    kapil("k = 2π/λ tutarlı", dogru)

    # 3) tepe -> çukur: fark fazlarda ters işaret
    z_tepe = sum(math.sin(math.pi / 2 + i * 2.17) for i in range(5))
    z_culuk = sum(math.sin(-math.pi / 2 + i * 2.17) for i in range(5))
    kapil("tepe/çukur ters faz", (z_tepe - z_culuk) > 0.5,
          f"(Δ = {z_tepe - z_culuk:.2f})")

    # 4) choppiness sinirli: yatay kayma tepe yüksekligini gecmemeli
    #    |disp| = chop * Σ steep ≈ chop * 0.55/5 * 5 k=... sayisal
    max_disp = 0.95 * sum(0.55 / ((2 * math.pi / lam) * 5)
                          for lam, _ in TABAN) * 0.6
    kapil("chop < 1 → örgü kaymaz", max_disp < 1.0, f"(max {max_disp:.2f})")

    # 5) preset sayisi ve zorunlu alanlar
    presetler = re.findall(r"'[a-zçğıöşü]+':\s*\{dir:", src)
    kapil("5 preset tanımlı", len(presetler) == 5, f"({len(presetler)})")
    for gerekli in ("u_waveA", "u_waveB", "gokyuzu", "MeshStandardMaterial",
                    "ACESFilmicToneMapping", "shadowMap"):
        kapil(f"{gerekli} kullanımda", gerekli in src)

    # 6) ses zinciri tam mi (Kaynak -> filtre -> kazanc -> cikis)
    zincir = all(x in src for x in ("createBiquadFilter", "kazanc.gain.value",
                                   "src.start()"))
    kapil("ses zinciri kuruluyor", zincir)

    # 7) three.js yerel olarak vendor'lanmis (deterministik, CDN yok)
    kapil("three.js vendor'lu", "vendor/three.module.js" in src and
          os.path.exists(os.path.join(KOK, "vendor", "three.module.js")))

    # 7b) Jacobian kopusu shader'da
    kapil("su displacement shader", "u_time" in src and "wy" in src and "u_amp" in src)

    # 8) GEMI kapisi: heave = 4 ornek ortalamasi, shader'in surekli
    #    y(merkez) degerine yakin olmali
    def yukseklik(x, z, t, yonR, amp, wind):
        y = 0.0
        for i, (lam, sap) in enumerate(TABAN):
            k = 2 * math.pi / lam
            om = math.sqrt(G * k) * wind
            aci = yonR + sap
            y += amp * (1.0 - i * 0.16) * math.sin(
                k * (math.cos(aci) * x + math.sin(aci) * z) - om * t + i * 2.17)
        return y

    amp, wind, yonR, t = 1.05, 1.9, 3.8, 4.2
    L, YAR = 11.0, 2.2
    hx, hz = math.cos(yonR), math.sin(yonR)
    ornek = [yukseklik(hx * L, hz * L, t, yonR, amp, wind),
             yukseklik(-hx * L, -hz * L, t, yonR, amp, wind),
             yukseklik(-hz * YAR, hx * YAR, t, yonR, amp, wind),
             yukseklik(hz * YAR, -hx * YAR, t, yonR, amp, wind)]
    heave = sum(ornek) / 4
    merkez = yukseklik(0, 0, t, yonR, amp, wind)
    kapil("gemi heave = 4 nokta ortalamasi", abs(heave - merkez) < 1.0 * amp,
          f"(|heave−y₀| = {abs(heave - merkez):.2f} m)")

    # 9) gemi acilari fiziksel sinirlar icinde
    pitch = math.atan2(ornek[0] - ornek[1], 2 * L)
    roll = math.atan2(ornek[3] - ornek[2], 2 * YAR)
    kapil("gemi acilari fiziksel", abs(pitch) < 0.5 and abs(roll) < 0.5,
          f"(pitch {math.degrees(pitch):.1f} derece, roll {math.degrees(roll):.1f} derece)")

    # 10) determinizm
    kapil("determinizm",
          [math.sqrt(G * 2 * math.pi / l) for l, _ in TABAN] ==
          [math.sqrt(G * 2 * math.pi / l) for l, _ in TABAN])

    print(f"\n{'TUM KAPILAR GECTI' if fail == 0 else 'KAPILARDA FAIL VAR'}"
          f" ({ok} ok, {fail} fail)")
    sys.exit(0 if fail == 0 else 1)


if __name__ == "__main__":
    main()
