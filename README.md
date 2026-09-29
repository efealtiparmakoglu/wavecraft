# 🌊 wavecraft

**EN:** A **real-time Gerstner ocean in your browser** — the same physics the `ocean-cinema`/`ship-cinema` repos render in Cycles, running at 60 fps in a fragment shader: deep-water dispersion **ω = √(g·k)** per wave train, choppiness, analytic normals, fresnel sky reflection and sun glitter. And it **sounds** like the sea it draws: filtered noise whose gain and cutoff follow the live wave-crest amplitude (Web Audio). Drag to turn the swell, wheel/arrows for wind speed, click for sound. Zero dependencies, one HTML file.

**TR:** Tarayıcında **gerçek zamanlı Gerstner denizi** — ocean-cinema/ship-cinema'nın Cycles'te render ettiği fizik şimdi shader'da 60 fps: dalga trenlerine göre derin su dispersiyonu **ω = √(g·k)**, choppiness, analitik normal'ler, fresnel gök yansıması ve güneş glitter'ı. Ve **deniz gibi duyuyor**: kazancı ve filtre kesimi canlı tepe yüksekliğini takip eden filtrelenmiş gürültü (Web Audio). Sürükle: yön · tekerlek/oklar: hız · tık: ses. Sıfır bağımlılık, tek HTML dosyası.

## ✨ Demo

**Canlı: [efealtiparmakoglu.github.io/wavecraft](https://efealtiparmakoglu.github.io/wavecraft)** · yerelde: `open index.html`

## 🎛️ Preset'ler

| preset | ruh hali |
|---|---|
| `sakin` | tropikal sabah, üç nazik dalga |
| `firtina` | beş dalga, koyu su, yüksek choppiness |
| `gunbatimi` | alçak turuncu güneş, uzun glitter yolu |
| `ay` | gece, gümüş tepeler, sönük ışık |
| `cak` | parlak öğle, berrak turkuaz |

## 🧱 Physics / Fizik

| Piece | Detail |
|---|---|
| 🌊 Dalgalar | 5 train: λ 36→2.9 m, her biri kendi ω = √(g·k) ile |
| ↔️ Choppiness | tepe yatay kayması `disp −= chop·steep·cos(f)·d̂` |
| 🧮 Normal | fragment öncesi analitik türevlerden (türev hesabı shader'da) |
| 🔊 Ses | beyaz+kahve gürültü → lowpass + bandpass "sıçrama"; kazanç ∝ tepe genliği |

## ✅ Verification / Doğrulama

```bash
python3 tests/verify.py
node --check <(script bloğu)   # JS sözdizimi
```

- **Dispersion gate**: ω strictly increases as λ shrinks (1.31 → 4.61 rad/s)
- **Wave-number gate**: k = 2π/λ consistent
- **Crest/trough gate**: phase offsets invert the sum
- **Chop gate**: |horizontal shift| < wave height (no mesh fold)
- **Structure gates**: 5 presets, all uniforms present, audio chain wired, WebGL2+VAO
- **Determinism gate**

## 🧪 Why / Neden

**TR:** Serinin 21 reposu hep "bir kare render"di. Bu ilk kez **çalışan bir şey**: fizik bir dosyaya gömülü, saniyede altmış kez ekrana basılıyor, üstelik sesi de aynı matematikten çıkıyor. Render ile arasındaki fark: render bir iddia, çalışan kod bir kanıt.

## 📄 License

MIT
