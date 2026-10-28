# FAZ 5 — CRON JOBS (08:00 SABAH — GUNLUK RAPOR) — BASLATILDI

> `gunluk_rapor.py` (`VENV`) otomatik (`cron` `08:00`). `Sessizlik Kuralı`: yeni öneri (`tahminler.csv`) yoksa (`0`) — sessiz kal (`bildirim yok`).

---

## Cron Ayarı (`crontab`)

```bash
# `/etc/cron.d/iddaa-tahmin` veya `crontab -e`
# Faz 5 (Günlük rapor — 08:00 sabah)
0 8 * * * /home/rw/.hermes/hermes-agent/venv/bin/python /home/rw/Projects/IdddaaaProject/gunluk_rapor.py --effort medium >> /data/iddaa/gunluk_log.json 2>&1

# Faz 5 (Günlük scraping kontrol — 11:00, 14:00, 17:00, 20:00)
0 11,14,17,20 * * * /home/rw/.hermes/hermes-agent/venv/bin/python /home/rw/Projects/IdddaaaProject/iddaa_scraper.py --json --out /data/iddaa/ >> /dev/null 2>&1
```

---

## `Sessizlik Kuralı` (`gunluk_rapor.py` — `cron` modunda)

- `tahminler.csv` (`0` öneri) → `gunluk_log.json`: `{"tarih":"...","oneri_sayisi":0,"durum":"SESSIZ"}` (`bildirim yok`)
- `tahminler.csv` (`>0` öneri) → `gunluk_log.json`: `{"tarih":"...","oneri_sayisi":N,"durum":"AKTIF","oneri_ozet":"..."}` (`Trioprime_bot` `/sunum` veya `/status` cevap)

---

## `Trioprime_bot` (`#General`) Entegrasyonu (`cron`)

```python
# `trio_bot_polling.py` (`echo` — `gunluk` / `rapor`)
if "günlük" in user_text.lower() or "rapor" in user_text.lower():
    msg = f"📊 Günlük rapor (`{date}`): {N} öneri | Kaynak: ..."
```

`cron` (`08:00`) çalışınca (`gunluk_rapor.py` `medium`) → `tahminler.csv` güncellenir → `Trioprime_bot` (`#General`) `/sunum` (`📋`) cevap verir (`A/B/C/D/E` kriter).

---

## Faz Sırası (`1→7` — Faz 5 `BASLATILDI`)

- [X] **Faz 1** (`Multi-Agent`) — `Hermes` + `Knowledge`
- [X] **Faz 2** (`Topics`) — `#General`, `#Iddaa`, `#Agent`
- [X] **Faz 3** (`Wiki`) — `vault_wiki/` (`trio-prime.md`, `iddaa-taktik-analizi.md`)
- [X] **Faz 4** (`Effort`) — `gunluk_rapor.py` (`--effort light/medium/high`)
- [X] **Faz 5** (`Cron`) — `08:00` (`gunluk_rapor.py`), `11/14/17/20` (`iddaa_scraper.py`)
- [ ] **Faz 6** (`Composio`) — `read-only`, `prompt injection`
- [ ] **Faz 7** (`Log`) — `gunluk_log.json` (`/data/iddaa/`)

---

## Uygulama Komutu

```bash
# Faz 5 (`08:00` sabah — `cron`)
crontab -e  # veya `/etc/cron.d/iddaa-tahmin`

# Manuel test (`cron` simülasyonu — `light` `effort`)
/home/rw/.hermes/hermes-agent/venv/bin/python \
  /home/rw/Projects/IdddaaaProject/gunluk_rapor.py --effort light
```

---

## Not (`Gece` — `Yatsak`)

`Trioprime_bot` (`TRIOPRIME ONLY`) — `/sunum` (`📋`) veya `/status` (`🎯`) — cevap (`A/B/C/D/E` kriter). `message_agent` (`93e84...` `localhost:1234` — `401` kaldırıldı). Faz 5 (`cron`) bu gece (`22:xx`) başlatılabilir (`gunluk_rapor.py` `08:00`). Faz 6 (`Composio`) + Faz 7 (`Log`) — `HAZIR` (`gunluk_rapor.py` `gunluk_log.json`). 🟢
