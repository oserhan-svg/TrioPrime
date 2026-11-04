# Manual Brush / Manual Erase — Yakalanan Açıklama

## Kaynak: Pixelbin FAQ (Desktop Preview read, 9862 chars)
- Seçenek: "AI Removal" veya "Manual Brush" (metot seçimi).
- Açıklama: "Select the exact areas you want to clean up... manual brush to achieve cleaner and more accurate results."
- Uygulama akışı: Görsel yükle → model seç → Manual Brush → sonuç indir.

## Teknik Not (Kriss — gözleme dayalı)
- Bu özellik sunucu taraflı bir editör gibi çalışıyor (görsel yüklenmeden aktifleşmez).
- Yerel karşılığı: `OpenCV` mask + `inpaint` veya `GIMP` clone/heal benzeri bir işlem.
- `Sıfır Halüsinasyon`: Bu doküman sadece sayfa metnine dayanır; gerçek brush algoritması (canvas, mask, WebGL) incelenmedi.
