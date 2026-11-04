# 🎯 İddaa Taktik Analiz Sistemi

iddaa.com bültenini **sportsbook API** üzerinden çeker, oranlardan implied probability hesaplar,
Mackolik + Transfermarkt verileriyle çapraz doğrular ve güven skoru üretir.

> **Sıfır halüsinasyon ilkesi:** veri yoksa "veri yok" denir; asla uydurma veri üretilmez.
> **hata_payi** asla negatiftir (0 = doğru, 1 = yanlış).

---

## 📁 Mimari

```
┌─────────────────────────────────────────────────────────────┐
│  CRON 1: İddaa Taktik Analizi                                │
│  0 8,11,14,17,20 * * *  (gece 23:00-08:00 duraklatılır)     │
│  → bülten çek → tahmin motoru → Mackolik/TM araştır → rapor │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│  CRON 2: Oran-Yok İzleyicisi                                 │
│  */30 8-21 * * *  (no_agent, sessiz watchdog)                │
│  → oransız maçları yeniden kontrol et → bülteni güncelle     │
└─────────────────────────────────────────────────────────────┘
```

### Veri akışı

```
iddaa API ──▶ bulten.json ──▶ tahmin motoru ──▶ analiz_raporu.md
                  ▲                                  (Mackolik + TM)
                  │
          oran_kontrol.py (oransız maçları izler)
```

---

## 🗂 Dosyalar

| Dosya | Görev |
|---|---|
| `iddaa_scraper.py` | Bülteni sportsbook API'den çeker → `bulten.json` / `.csv` / `.md` |
| `gunluk_rapor.py` | Tahmin motoru: odds → implied prob → A/B/C filtre → güven skoru |
| `oran_kontrol.py` | Oransız maç izleyicisi (cron script) |
| `analiz_sistemi.py` | Hata payı / sapma / başarı oranı analizi |
| `tahminler.csv` | Tüm tahminler (`dogru_mu` sütunu doğruluk kaynağı) |
| `sonuclar.csv` | Gerçek maç sonuçları |
| `algoritma_parametreleri.json` | Parametreler + güncelleme önerileri |
| `dev_notes/` | API tersine mühendislik notları (keşif script'leri) |
| `hata_payi_analizi.md` | Hata payı & sapma değerlendirmesi |

### Çıktı dizini: `/data/iddaa/`

| Dosya | İçerik |
|---|---|
| `bulten.json` | Ham bülten (tüm pazarlar) |
| `bulten.csv` | Bülten tablo hali |
| `bulten.md` | Bülten Markdown |
| `analiz_raporu.md` | **Ana rapor** (öneriler) |
| `analiz_raporu.json` | Rapor JSON |
| `gunluk_log.json` | Oran-yok izleyici kayıtları |

---

## 🚀 Kullanım

```bash
cd /home/rw/Projects/IdddaaaProject
VENV=/home/rw/.hermes/hermes-agent/venv/bin/python

# Bülteni çek
$VENV iddaa_scraper.py --json

# Tam akış (çek + analiz)
$VENV gunluk_rapor.py

# Sadece analiz (bülteni yeniden çekme)
$VENV gunluk_rapor.py --skip-scrape

# Sadece Süper Lig
$VENV gunluk_rapor.py --lig 584

# Oran-yok izleyicisi
$VENV oran_kontrol.py            # sessiz (değişiklik yoksa çıktı yok)
$VENV oran_kontrol.py --verbose  # tüm adımları yazdır

# Hata payı analizi (sonuçlar girildikten sonra)
$VENV analiz_sistemi.py
```

---

## 📊 Tahmin Motoru

### Odds → implied probability

```
raw_p = 1 / odds        (her seçenek için)
p     = raw_p / Σraw_p  (marjin normalize edilir)
```

### Skorlama (0-10)

| Filtre | Birincil sinyal | Ağırlık | İkincil sinyaller |
|---|---|---|---|
| 🅰️ İY KG Var | KG Var oranı (düşük = olası) | 0.55 | A/Ü 2.5 Üst 0.20 · İY X 0.15 · İY 1/2 0.10 |
| 🅱️ Her İki Yarıda Gol | A/Ü 2.5 + 3.5 Üst | 0.60 | KG Var 0.25 · İY 1/2 0.15 |
| 🅲 İY Sonucu | İY oran lehimi | 0.70 | MS (kadro proxy) 0.30 |

Kalibrasyon: `_inv(odds, lo, hi)` — düşük odds yüksek skor; `_norm(x, lo, hi)` — yüksek değer yüksek skor.
Ağırlıklı ortalama alınır, eksik veri 0.0 sayılır.

**Öneri eşiği: 7.5** — altındakiler rapora girmez.

### Örnek çıktı (21 Ekim 2026)

| Maç | Öneri | Güven |
|---|---|---|
| Inter vs Shakhtar Donetsk | İY 1 | 9.9 |
| Real Madrid vs Leipzig | İY 1 | 9.6 |
| Aston Villa vs Viking | İY 1 | 9.6 |
| Sporting Lizbon vs LASK | İY 1 | 9.4 |

---

## ⏰ Cron Job'lar

| Job | ID | Schedule | Mod |
|---|---|---|---|
| İddaa Taktik Analizi | `7c474e7c382f` | `0 8,11,14,17,20 * * *` | agent |
| İddaa Oran-Yok İzleyicisi | `2bed7064c60c` | `*/30 8-21 * * *` | script (no_agent) |

Yönetim:
```bash
hermes cron list
hermes cron run <job_id>
hermes cron pause <job_id>
```

---

## 🔑 İddaa Sportsbook API

```
https://sportsbookv2.iddaa.com/sportsbook/events?st=1&type=0&version=0&live=false
```

| Param | Anlamı |
|---|---|
| `st=1` | futbol |
| `type=0` | bülten (oranlar **dolu**) |
| `type=1` | geniş liste (oransız maçlar) |
| `live=true` | canlı — **market'lar boş gelir** |

**Pazar kodları:** MS `t=1,st=1` · İY `t=2,st=88` · Handikap `t=2,st=100` · A/Ü `t=2,st=101` · KG `t=2,st=89`

**Lig kodları:** Süper Lig `ci=584` · Şampiyonlar Ligi `ci=46194`

Gerekli: `curl_cffi` (0.16.3) + chrome impersonation. Dökümantasyon: `sports-betting-analysis` skill.

---

## 📈 Sonuç Takibi

1. Maç sonuçlarını `sonuclar.csv`'ye gir (İY skorunu **kesin** yaz — İY KG Var ilk yarıya bağlıdır)
2. `tahminler.csv`'ye `dogru_mu` (Evet/Hayır) ve `hata_payi` (0/1) ekle
3. `python3 analiz_sistemi.py` → MAE, sapma, başarı oranı, güven korelasyonu

### Metrik hedefleri

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Mevcut durum (21 Ekim 2026)

| Metrik | Değer |
|---|---|
| Değerlendirilebilir tahmin | 2 |
| Doğru | 1 |
| Başarı oranı | %50 |
| MAE | 0.5 |
| Sapma | 0.7071 |

---

## ⚠️ Bilinen Kısıtlamalar

- **Süper Lig oranları gecikir:** Süper Lig maçları maç gününe yaklaşana kadar `type=0` bültenine oransız girer. `oran_kontrol.py` bunları izler.
- **`/data/` dizini:** `pkexec` (PolicyKit GUI şifre diyaloğu) ile oluşturuldu → `/data/iddaa` (`rw:users`). Root-owned klasör için `pkexec` kullan; `sudo` şifresiz çalışmaz.
- **Cron çıktısı bu oturuma teslim edilmiyor:** CLI/HTTP oturumlarında canlı delivery kanalı yok; çıktılar dosyada saklanır (`cronjob list` ile görülebilir).
- **Mackolik scraping gerektirir:** Herkese açık API yok; hız sınırı ~2s/request.
- **`markets_by_id` endpoint'i kullanılamıyor:** POST ama body formatı bilinmiyor (500 dönüyor); market'lar `events`'ten geliyor.

---

## 📜 Güncelleme Geçmişi

- **2026-10-21:** Sistem kuruldu. Sportsbook API tersine mühendislikle çözüldü, scraper + tahmin motoru + oran-yok izleyicisi yazıldı, 2 cron job kuruldu.
