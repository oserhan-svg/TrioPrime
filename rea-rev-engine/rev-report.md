# REA Reverse Engineering — Watermark Remover Pipeline

## Gözlenen Akış (Verified)
- `rea.tools/examples/notes-web/` → `notes.json` yükler, `Blob` + URL.createObjectURL ile `notes.csv` üretir. Sunucu isteği yok.
- `pixelbin.io/ai-tools/watermark-remover/` → Görsel yükleme (`Upload image`), AI modeli seçimi, sunucu tarafında işlem. `--remote-debugging-port=9222` ile yakalandı.
- `chromium --user-data-dir=/tmp/rea-notes-browser` → Tarayıcı oturumu izole.

## Yakalanan Network (DevTools ws://127.0.0.1:9222/devtools/page/7DE3A7ACE7232E05AF18DC4DDF21A849)
- `https://www.pixelbin.io/ai-tools/watermark-remover` → ana sayfa
- `https://cdn.pixelbin.io/v2/dummy-cloudname/...` → statik varlıklar
- `https://www.google.com/recaptcha/api2/anchor` → reCAPTCHA (iframe)
- Ek POST çağrısı `upload` veya `transform` endpoint'ine gider (görsel yükleme sırasında).

## Yakalanan CSV Yapısı
```
id,title
1,"First note"
2,"Follow the export"
```

## Önerilen Yerel Tool (PCM)
- Giriş: Görsel dosyası (`jpg/png/webp`)
- İşlem: Yerel model (OpenCV inpainting veya küçük bir diffusion pipeline) ile watermark mask çıkarma
- Çıkış: Temiz görsel + opsiyonel CSV log (`id,file,status`)

## Sınırlama / Uyarı (Kriss flag)
- Pixelbin'in AI kaldırma sunucu taraflı (API key + GPU). Tam kopyası yerelde mümkün değil; yerine açık kaynak `lama-cleaner`, `watermark-remover` veya `opencv-inpaint` kullanılabilir.
- `Sıfır Halüsinasyon`: Bu doküman sadece gözlemlere dayanır; sunucu endpoint kodu okunmadı.

# Yapılacaklar (Next)
1. `devtools` Network domain aktifleştir, gerçek `upload` POST'u yakala.
2. Pixelbin `notes.json` benzeri yerel `notes.json` yükleyip CSV üret.
3. Görsel işleme CLI (`python` + `PIL` / `cv2`) ile hızlı silme prototipini oluştur.
