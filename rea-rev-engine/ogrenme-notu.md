# Öğrenme Notu — Ne Yaptık? (Basit Açıklama)

## 1. Gözlem (`rea-rev-engine/`)
- `rea.tools`: `notes.json` yükler → `CSV` üretir (`Blob`). Sunucu isteği yok.
- `pixelbin`: `POST /api/upload` (`Express`, `500`), token (`authorization`, `x-auth-token`) gerekli.
- `manual brush`: görsel yükle → maske çiz → `inpaint`.

## 2. Yerel Çözüm (`full-pipeline.py`)
- `downloads/` içindeki `scraped` fotoğrafları okur (`PIL` / `OpenCV`).
- `threshold` → `mask` → `cv2.inpaint` (`INPAINT_TELEA`). Bu, `manual brush` simülasyonu.
- `cleaned/` klasörüne yeni görseller yazar (`PNG`).
- `clean-log.csv`: `id,filename,status` (yakalanan format).

## 3. Neden Token Gerekmeden?
- `pixelbin` sunucu taraflı AI (`API key`).
- Bizim kod `OpenCV` (`python3`) — bilgisayarda çalışır, internet gerekmeden.
- Hızlı: 13 görsel ~saniyede.
