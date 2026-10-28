# Network Trace — Option A (DevTools / REA)

## Yakalanan Endpointler
- `GET https://rea.tools/examples/notes-web/` (HTML)
- `GET https://rea.tools/examples/notes-web/notes.json` (JSON kaynağı)
- `GET https://www.pixelbin.io/ai-tools/watermark-remover/` (hedef sayfa, DevTools ws: 7DE3A7ACE...)

## notes.json İçeriği (Verified)
```json
{
  "notes": [
    { "id": 1, "title": "First note" },
    { "id": 2, "title": "Follow the export" }
  ]
}
```

## Export Olayı (Client-Side)
- `btn-export-notes` tıklandı.
- `notes.csv` (`/home/rw/Downloads/notes.csv`) yeniden yazıldı.
- Sunucu POST/GET gözlenmedi (`Blob` download).

## Pixelbin Network (Gözlenen ws ID)
- `7DE3A7ACE7232E05AF18DC4DDF21A849` → ana sayfa
- `C6A233D19153586CBF5C3CBC38CE84E0` → reCAPTCHA iframe
- `92A04FCFFE9760A2395B56CAE2DA6A4E` → reCAPTCHA bframe

## Kısıtlama
- 9222 session'da `rea.tools` açık değil (desktop_preview ayrı oturum). Gerçek upload POST'u `pixelbin` için yakalanmalı; bu için görsel yüklenip `Network` domain açılmalı.
