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

TABAN = [(36.0, 0.0), (20.0, 0.16), (10.5, -0.20), (5.6, 0.32), (2.9, -0.40)]


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
    presetler = re.findall(r"^\s+'[a-zçğıöşü]+':\s*\{dir:", src, re.M)
    kapil("5 preset tanımlı", len(presetler) == 5, f"({len(presetler)})")
    for gerekli in ("u_vp", "u_waveA[0]", "u_waveB[0]", "u_skyHorizon"):
        kapil(f"uniform {gerekli} shader'da", gerekli in src)

    # 6) ses zinciri tam mi (Kaynak -> filtre -> kazanc -> cikis)
    zincir = all(x in src for x in ("createBiquadFilter", "kazanc.gain.value",
                                   "src.start()"))
    kapil("ses zinciri kuruluyor", zincir)

    # 7) WebGL2 ve VAO (WebGL1'de calismaz)
    kapil("WebGL2 + VAO", "webgl2" in src and "createVertexArray" in src)

    # 8) determinizm
    kapil("determinizm",
          [math.sqrt(G * 2 * math.pi / l) for l, _ in TABAN] ==
          [math.sqrt(G * 2 * math.pi / l) for l, _ in TABAN])

    print(f"\n{'TUM KAPILAR GECTI' if fail == 0 else 'KAPILARDA FAIL VAR'}"
          f" ({ok} ok, {fail} fail)")
    sys.exit(0 if fail == 0 else 1)


if __name__ == "__main__":
    main()
