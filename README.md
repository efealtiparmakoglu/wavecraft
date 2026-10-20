# 🌊 Wavecraft

[![CI](https://github.com/efealtiparmakoglu/wavecraft/actions/workflows/ci.yml/badge.svg)](https://github.com/efealtiparmakoglu/wavecraft/actions/workflows/ci.yml)

**[Open the live ocean →](https://efealtiparmakoglu.github.io/wavecraft/)**

**EN:** An interactive ocean with five Gerstner-style wave trains, floating ships and synthesized sea sound. Three.js renders the scene with shadow maps and ACES tone mapping. The wave field drives ship heave, pitch and roll, as well as the Web Audio gain and filter.

**TR:** Beş Gerstner dalga treni, dalgalarda yüzen gemiler ve sentezlenen deniz sesiyle etkileşimli bir okyanus. Three.js sahneyi gölgeler ve ACES ton eşlemesiyle çizer. Dalga alanı gemilerin yüksekliğini, eğimini ve yalpasını; Web Audio kazanç ve filtre değerlerini besler.

## Run locally / Yerelde çalıştır

Clone the repository, then run this command **from its root**:

```sh
git clone https://github.com/efealtiparmakoglu/wavecraft.git
cd wavecraft
python3 -m http.server 8000
```

Open **[localhost:8000](http://localhost:8000)** in a browser with WebGL support. Stop the server with Ctrl+C.

**TR:** Komutu depo kökünde çalıştır, ardından yukarıdaki yerel adresi aç. Durdurmak için Ctrl+C kullan.

The app uses ES modules and an import map, so serve it over HTTP. Double-clicking `index.html` as a `file://` URL can fail browser module/CORS checks. There is no npm install or build step: Three.js and OrbitControls are included in `vendor/`; keep that folder beside `index.html` and `timing.mjs`.

**TR:** ES modülleri nedeniyle dosyayı çift tıklamak yerine HTTP sunucusuyla aç. npm kurulumu veya build gerekmez; `vendor/` klasöründeki yerel Three.js/OrbitControls dosyaları ve `timing.mjs` uygulamanın parçasıdır.

## Controls / Kontroller

| Action | Result / Sonuç |
| --- | --- |
| Drag / Sürükle | Orbit the camera / Kamerayı döndür |
| Mouse wheel / Tekerlek | Zoom / Yakınlaş-uzaklaş |
| ← / → | Change wave direction / Dalga yönünü değiştir |
| ↑ / ↓ | Change speed / Hızı değiştir |
| Click the sea / Denize tıkla | Start audio / Sesi başlat |
| 📷 gemi takibi | Toggle ship-follow camera / Gemi takibini aç-kapat |

Sound starts after a user gesture, as required by browser autoplay rules. Frame rate depends on the browser, GPU and viewport; the HUD counts actual rendered frames. Ship movement uses per-frame elapsed time, independently of the FPS display interval.

## Presets

| Preset | Scene / Sahne |
| --- | --- |
| `sakin` | Calm daylight / Sakin gündüz |
| `firtina` | Darker sky and larger waves / Koyu gökyüzü ve büyük dalgalar |
| `gunbatimi` | Orange sunset / Turuncu gün batımı |
| `ay` | Moonlit sea / Ay ışığında deniz |
| `cak` | Bright midday / Parlak öğle |

## Check the project / Doğrulama

Python is needed for the existing physics/structure checks. Node.js is needed only for JavaScript checks, not to use the app.

```sh
python3 tests/verify.py
python3 scripts/check_javascript.py
node --test tests/timing.test.mjs
```

CI runs these commands on Python 3.11/3.12 with Node 24. The timing tests compare movement at 60/144 Hz, check measured frame counts and cover returning from a paused tab. The module check parses the shipped JavaScript and verifies local import-map files.

These checks do not certify visual rendering, audio output or a particular FPS on every device. The physics checks include a Python counterpart and HTML structure checks; they are not a full browser simulation.

**TR:** Testler fizik/HTML yapısını, JS sözdizimini ve zaman hesabını kapsar. Her cihazda aynı görüntü, ses veya FPS garantisi vermez.

## Source map / Dosyalar

| File | Purpose |
| --- | --- |
| `index.html` | Scene, controls, wave field, ships and audio |
| `timing.mjs` | Per-frame time delta and measured FPS |
| `vendor/` | Local Three.js and OrbitControls modules |
| `tests/verify.py` | Existing numerical and structure checks |
| `tests/timing.test.mjs` | Timing regression tests |
| `scripts/check_javascript.py` | JavaScript syntax and local import checks |

## License

MIT, as declared by the project. Vendored Three.js code retains its own upstream notices.
