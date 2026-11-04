# Gerçek Upload POST — Yakalanan Kanıt

## Endpoint (Verified)
- `POST https://www.pixelbin.io/api/upload` → `HTTP/2 500` (sunucu taraflı, endpoint VAR).
- `POST https://api.pixelbin.io/upload` → `404`.

## Yakalanan Response Headers (Verified via curl -v)
```
x-powered-by: Express
access-control-allow-headers: pixb-cl-id, authorization, fynd-affiliate-id,
  fynd-affiliate-token, image_resize, device-width, DNT, X-CustomHeader,
  Keep-Alive, User-Agent, X-Requested-With, If-Modified-Since,
  Cache-Control, Content-Type, Range, uppy-auth-token, x-application-id,
  x-application-token, x-auth-token, x-currency-code, x-device-platform,
  x-force-logout, x-force-reload, x-staff-user, x-company-id, accept-version,
  x-fp-date, x-fp-signature, x-ebg-signature, x-ebg-param, x-ebg-previeww-limit,
  captcha-code, x-bg-session
via: 1.1 google
cf-ray: a50a481e0ffadff3-IST
```

## Çıkarım (Kriss)
- Upload, Pixelbin sunucusunda `Express` ile işleniyor (`x-powered-by: Express`).
- Gerekli token'lar: `authorization`, `x-auth-token`, `uppy-auth-token`, `x-application-token`.
- Bu endpoint'e gerçek görsel yüklemek için bu token'lar gerekir; aksi halde 500.
- `upload-capture.log` — gerçek POST yapısı yakalanamadı (token yok), ama endpoint VAR.
