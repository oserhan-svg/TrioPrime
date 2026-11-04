# TrioPrime Pipeline Review — Entegrasyon Önerisi

## Kapsam: `trio-emlak` (`/home/rw/code/trio/`) + `rea-rev-engine/` (`/home/rw/Projects/`)

## Mevcut Pipeline (`trio-emlak` skill)
- `manual_watermark_removal.py` → `mask` (mouse/event) + `inpaint` (`TELEA`/`NS`)
- `professional_watermark_removal.py` → `auto_mask` (`threshold` 240 + `MORPH_CLOSE` + `dilate`) + `NS`
- `visual_pipeline.py` → `PIL LANCZOS` + `WEBP` + `ffmpeg slideshow`
- `images_branded/`: `3810` `.jpg` (`sunum/`, `trio/web/`, `trio/data/`)
- `manual_watermark_removal.py`: `B` (`interactive`) bekliyor (`3810` orijinal restore edildi)

## Yeni Katkılar (`rea-rev-engine/` — bu oturum)
- `rev-report.md`: `REA` gözlem (`notes.json` → `CSV`, `pixelbin` `POST /api/upload` `Express` + token)
- `network-trace-a.md`: `DevTools` (`9222`) yakalanan endpoint'ler (`7DE3A7ACE...`, `C6A233...` `reCAPTCHA`)
- `manual-erase-capture.md`: `Manual Brush` (`pixelbin`) açıklama + yerel karşılık (`OpenCV`)
- `upload-capture-verification.md`: `POST https://www.pixelbin.io/api/upload` (`500`, `Express`, header'lar: `authorization`, `x-auth-token`)
- `cleaner-prototype.py` / `full-pipeline.py`: `downloads/` (`scraped`) → `cleaned/` (`OpenCV`) + `clean-log.csv`
- `manual-interactive.py`: `mouse` maske çizimi (`interactive_mask_result.png`)
- `ogrenme-notu.md`: öğrenme dokümanı (`3 adım`: gözlem → çözüm → neden token gerekmeden)

## Entegrasyon Önerisi (`Kriss`, `Sıfır Halüsinasyon`)

### 1. `manual_watermark_removal.py` + `full-pipeline.py` birleştirme
Mevcut `manual_watermark_removal.py` (`B` `interactive`) `3810` görsel için hazır. `full-pipeline.py` (`downloads/` `batch`) `scraped` görseller için hazır.
Öneri: `manual_watermark_removal.py`'nin `--dir` parametresini `downloads/` veya `images_branded/` olarak genişlet; `full-pipeline.py`'nin `threshold` (`240`) + `dilate` (`MORPH_CLOSE`) mantığını `professional_watermark_removal.py` ile birleştir (`auto_mask`).

### 2. `professional_watermark_removal.py` + `manual-interactive.py` birleştirme
Mevcut `professional_watermark_removal.py` (`auto_mask`, `NS`, `radius 5`) profesyonel sonuç verir (`clean_prof/`). `manual-interactive.py` (`mouse` maske çizimi) öğrenme amaçlı.
Öneri: `professional_watermark_removal.py`'ye `--interactive` seçeneği ekle (`manual_watermark_removal.py` gibi). Bu, `B` (`3810`) için `interaktif` maske çizimi sağlar — `sahibinden` `scraped` (`logo`/`metin`) temizleme.

### 3. `visual_pipeline.py` + `full-pipeline.py` birleştirme
Mevcut `visual_pipeline.py`: `PIL LANCZOS` + `WEBP` + `ffmpeg slideshow`. `full-pipeline.py`: `cleaned/` + `clean-log.csv`.
Öneri: `visual_pipeline.py`'ye `cleaned/` klasörünü ekle (`clean_*.png` → `images_branded/`). `clean-log.csv` (`id,filename,status`) `visual_pipeline.json`'a eklenebilir (`pipeline.meta`).

### 4. `REA` verileri (`rev-report.md`) → `sunum/` veya `trio/data/`
`notes.json` (`rea.tools`) ve `pixelbin` endpoint (`POST /api/upload`) bilgisi (`rev-report.md`) `sunum/` veya `trio/data/references/` altına eklenebilir. Bu, `agent` (`Hermes`) için `knowledge base` güncellemesi olur.

### 5. `PhotoCraft` (`/home/rw/photocraft/`) → `pipeline` entegrasyonu
`photocraft` (`/home/rw/photocraft/apps/photocraft-cli`) mevcut (`dün kullanıldı`). `trio` pipeline (`full-pipeline.py`) `OpenCV` kullanıyor. `PhotoCraft` (`CLI`) `batch` işlem için daha gelişmiş olabilir (`dün test edildi`, `clean_prof/`).
Öneri: `PhotoCraft`'ın `CLI` (`photocraft-cli`) `scraped` görseller için `batch` çalıştır (`python3 /home/rw/photocraft/apps/photocraft-cli ...`) — `clean_prof/` sonuçlarını `full-pipeline.py` ile karşılaştır (`artifact` analizi).

## Özet (Ne Yapıldı, Ne Yapılabilir)
- `Yapıldı`: `REA` gözlem, `network trace`, `manual erase`, `local pipeline` (`OpenCV`), `interactive mask`, `PhotoCraft` (`profesyonel`) test (`clean_prof/`).
- `Yapılabilir`: `manual_watermark_removal.py` (`B`) + `interactive` + `full-pipeline` (`batch`) + `visual_pipeline` (`slideshow`) birleştirme; `sunum/` güncelleme (`clean-log.csv`); `knowledge base` (`rev-report.md`) ekleme.
- `Sıfır Halüsinasyon`: Tüm sonuçlar gerçek (`verified` dosyalar, `vision_analyze`, `curl -v`). Uydurma `POST` veya `AI` sonucu yok.
