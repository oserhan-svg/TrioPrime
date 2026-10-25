# 📚 İDDAA PROJE DETAYLARI — FAZ 1 (MULTI-AGENT CREW) TAMAMLANDI

> Faz 1: Orchestrator (`Hermes`) + Librarian (`Knowledge`) — 5 agent değil, pratik 2 agent. `.worktrees`: DÜZELTİLDİ. `Trioprime_bot`: `/goal` DÜZELTİLDİ.

---

## 📁 FAZ 1 — MULTI-AGENT CREW

> İddaa Taktik Analiz Sistemi - Gelişmiş AI Görevi Takip

---

## 📁 FAZ 2 — TELEGRAM TOPICS (İLETİŞİM VE KONU YAPISI)

> Her ajana özel `Topics` (konular) — bağlam bozulmaması için.

---

## 📁 2. Telegram Konu (Topics) Yapısı

### Grup: `Hermes Workers Group`

| Konu / Topic | Bot / Agent | Görev | Durum |
|--------------|-------------|-------|-------|
| `#General` (`Biten İşler`) | `Trioprime_bot` (`Dude`) | TrioPrime operasyon — `.worktrees`, `sunumu/index.html`, `goal` | ✅ ÇALIŞIYOR |
| `#Iddaa` (İlan / Scraping) | `ToxkolLik_bot` | Iddaa scraping (`iddaa_scraper.py`), tahmin (`tahminler.csv`), rapor (`gunluk_rapor.py`) | ✅ ÇALIŞIYOR |
| `#Agent Durum Pano` | `Hermes` (`@hermes`) | Sistem sağlığı, `status`/`resume` komutları, `cron` durumu | ✅ ÇALIŞIYOR |

### Konu Kuralları

- `#General`: `Trioprime_bot` (`Dude`) — TrioPrime iş yükü. `Trioprime_bot` aktif (`/status`, `/goal`, `/resume`).
- `#Iddaa`: `ToxkolLik_bot` — Iddaa ilan çekme ve tahmin. Günlük (`gunluk_rapor.py`).
- `#Agent Durum Pano`: `Hermes` — sistem sağlığı, `knowledge-base.md` güncelleme, faz durumu.

---

## 📁 FAZ 3 — MARKDOWN WIKI (VAULT) — TAMAMLANDI

> Her ajan kendi `.md` dosyasını okur, günceller. Dış kaynak (`free-llm-api-resources`) benim verimden (`iddaa`) ayrı.

---

### Dizin Yapısı (`vault_wiki/`)

```text
/home/rw/Projects/vault_wiki/
├── projects/
│   ├── trio-prime.md       (TrioPrime: .worktrees DÜZELTİLDİ, sunumu/index.html güncellendi)
│   ├── iddaa-taktik-analizi.md (Iddaa: scraping + tahmin + rapor, /data/iddaa/)
│   └── free-llm-api-resources.md (Dış kaynak: LM Studio, 3 model)
├── agents/
│   ├── hermes.md           (Orchestrator: default, localhost:1234)
│   ├── knowledge.md        (Librarian: skills/knowledge/, knowledge-base.md)
│   └── trioprime_op.md     (TrioPrime_op: lead-management-agent, DÜZELTİLDİ)
└── logs/
    └── faz-durumu.md       (Faz sırası: 1→7, şu an Faz 3)
```

---

### Kurallar (Önemli)

- **Dış kaynak (`free-llm-api-resources`) — benim verimden (`iddaa`/`trio`) ayrı dizin** — karışmaz.
- **Günlük log (`gunluk_rapor.py` → `/data/iddaa/`)** — `bulten.json`, `analiz_raporu.md`, `gunluk_log.json`.

---

## 📁 1. Proje Genel Bakış

Bu proje, İddaa taktik analiz sisteminin kapsamlı bir izlenimi sunar. Her gün, her maç için veri toplar, sonuçları analiz eder ve tahminler üretir.

### 📊 Proje İstatistikleri

| Metrik | Değer |
|--------|-------|
| **Proje Adı** | İddaa Taktik Analiz Sistemi |
| **Proje Kontrolü** | Git (IDEA.md) |
| **Hazırlayan** | Gökcan Serhan |
| **Zaman Dilimi** | Europe/Istanbul |
| **Tarih** | 21 Ekim 2026 |
| **Durum** | Aktif |
| **Yüzleşme** | 10 Safat |
| **Önerilen** | 4 |
| **Sonuçlar** | 7 (2 dolu, 5 boş) |

---

## 📁 2. Dosya Yapısı

### 📂 Ana Klasör

```text
/Projects/IdddaaaProject/
├── ALGORITMA_ENTEGRASYON.md       # Algoritma entegrasyonu dokümanı
├── algoritma_parametreleri.json   # Parametre ayarları
├── analiz_raporu.json             # Rapor JSON
├── analiz_sistemi.py              # Analiz sistemleri scripti
├── bugun_analiz.md                # Bugünün analizi
├── dev_notes/                     # API exploration notları
├── gunluk_rapor.py                # Günlük rapor oluşturma
├── hata_payi_analizi.md           # Hata payı analizi
├── iddaa_scraper.py               # Ana scraper scripti
├── knowledge-base.md              # Bu dosya (proje sumary)
├── oran_kontrol.py                # Oran kontrolü
├── README.md                      # Proje dokümantasyon
├── site_olustur.py                # Site oluşturma scripti
├── sonuclar.csv                   # Sonuçlar
├── tahminler.csv                  # Tahminler
└── static_mirror.html             # Statik aynalı sayfa
```

### 📂 dev_notes Klasörü

API keşif ve keşif scriptleri bulunur:

| Dosya | Açıklama |
|-------|----------|
| `explore_play_8981559.md` | Play API keşfi |
| `explore_soccer_api_data.py` | Soccer API veri keşfi |
| `explore_soccer_api_post.py` | Soccer API POST isteği |
| `explore_soccer_api_request.py` | Soccer API request keşfi |
| `explore_test_a.py` | Test scripti |
| `explore_vk_api_post.py` | VK API keşfi |
| `explore_vk_data_requests.json` | VK data requests |
| `explore_vk_request.py` | VK request keşfi |
| `exploration_1.md` | İlk keşif denemesi |

---

## 📁 3. Ana Scriptler

### 3.1. `iddaa_scraper.py`

**Açıklama:** Ana scraping scripti. Bağımlı kaynaklardan veri çeker.

**Kullanım:**
```bash
cd /home/rw/Projects/IdddaaaProject

VENV=/home/rw/.hermes/hermes-agent/venv/bin/python
$VENV iddaa_scraper.py --json
```

### 3.2. `gunluk_rapor.py`

**Açıklama:** Günlük rapor oluşturucu scripti.

**Kullanım:**
```bash
$VENV gunluk_rapor.py          # Tüm işlemleri çalıştır
$VENV gunluk_rapor.py --skip-scrape  # Sadece analiz
$VENV gunluk_rapor.py --lig 584  # Sadece Süper Lig
```

### 3.3. `oran_kontrol.py`

**Açıklama:** Oran kontrolü ve değiştirme izleme.

**Kullanım:**
```bash
$VENV oran_kontrol.py            # Normal çalışma
$VENV oran_kontrol.py --verbose  # Tüm adımlar
```

### 3.4. `analiz_sistemi.py`

**Açıklama:** Analiz sistemleri ve hata payı hesaplama.

**Kullanım:**
```bash
$VENV analiz_sistemi.py
```

---

## 📁 4. Parametreler

### 4.1. `algoritma_parametreleri.json`

```json
{
  "metric": {
    "irrelevant": 0.0,
    "irrelevant_class": "error"
  },
  "rate_control": {
    "error_threshold": 3,
    "success_threshold": 10,
    "min_gepce": 5
  }
}
```

### 4.2. `analiz_raporu.json`

```json
{
  "result_summary": {
    "success": 7,
    "total": 10
  }
}
```

---

## 📁 5. Çıktı Dosyaları

### 5.1. Output Directory

Proje, verileri `/data/iddaa/` dizinine yazar:

| Dosya | Açıklama |
|-------|----------|
| `bulten.json` | Ham bülten |
| `bulten.csv` | Bülten tablo formatında |
| `bulten.md` | Bülten Markdown formatında |
| `analiz_raporu.md` | Ana analiz raporu |
| `analiz_raporu.json` | Rapor JSON |
| `gunluk_log.json` | Günlük kayıtlar |

### 5.2. CSV Dosyaları

| Dosya | Açıklama |
|-------|----------|
| `sonuclar.csv` | Sonuçlar (7 dolu, 3 boş) |
| `tahminler.csv` | Tahminler |

---

## 📁 6. Metrikler

### 6.1. Hata Payı / Sapma / Başarı Oranı / Güven Korelasyonu

Analiz sistemi ile hesaplanır:

```bash
VENV=/home/rw/.hermes/hermes-agent/venv/bin/python
$VENV analiz_sistemi.py
```

### 6.2. Metrik Tablosu

| Metrik | Mükemmel | İyi | Orta | Kötü |
|--------|----------|------|------|------|
| **MAE** | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| **Std Dev** | < 0.2 | 0.2-0.4 | > 0.4 | — |

---

## 📁 7. Güncelleme Tercihleri

### Q1 2027

- [ ] `iddaa_scraper.py` güncelleme
- [ ] `tahminler.csv` güncelleme
- [ ] `analiz_raporu.md` ekleme
- [ ] `dev_notes/` klasörü içeriklerini ana dokümanlara taşıma

---

## 📊 8. Jurnal

### 21 Ekim 2026 - Tarih

- Yeni proje oluşturuldu
- İddaa scraping scraper tamamlandı
- LM Studio entegrasyonu yapıldı
- Free LLM API repo klonlandı

---

## 🎯 9. SONUÇ

Bu proje, İddaa taktik analiz sisteminin ilk adımdır. Mevcut dosyalar ve dokümantasyon, sistem çalışmasını ve işleyişini tamamlar.

**Hazır Ortam:**
- Python 3.11+
- Venv: `/home/rw/.hermes/hermes-agent/venv`
- LM Studio: `localhost:1234`
- Trioprime Implementasyonu: `feature/trio-directive` branch'de

**Sıradaki Adım:** 
- `iddaa_scraper.py` ile scraping çalıştırma
- `tahminler.csv` güncelleme
- `analiz_raporu.md` oluşturma

---

## 📝 10. GÜNCELLEME TERCİHİ

| Tarih | Geliştirici | Değişiklik |
|------|-------------|------------|
| 21 Ekim 2026 | Gökcan Serhan | İddaa projesi klonlandı ve dokümanlandı |
