# ABİMİN (OZANCAN SERHAN — 0533 378 68 94) KARAR KRİTERLERİ (A/B/C/D/E)

> `Trioprime_bot` (`#General`) `/sunum` (`23:58` ✅) cevap alındı. `message_agent` (`93e84...` `localhost:1234`) `queued`. Faz 4 (`effort`) — `gunluk_rapor.py` (`--effort light/medium/high`) başlatıldı (`faz4_basladi.md`).

---

## A — GÜNLÜK KRİTER VE BÖLGE
**Abim (`0533...`) cevabı:** Günlük kriter (`Ayvalık/Cunda/Altınova/Gömeç/İstanbul`), ev/arsa ayrımı (`ev`/`arsa`/`ticari`), fiyat (`15.500.000 TL` örneği — `sahibinden.com/ilan/emlak-konut-satilik/1330012151`).

**Uygulama (`iddaa_scraper.py` + `gunluk_rapor.py`):**
```bash
VENV=/home/rw/.hermes/hermes-agent/venv/bin/python
$VENV iddaa_scraper.py --json --out /data/iddaa/
$VENV gunluk_rapor.py --effort medium --lig 584  # Süper Lig
```

---

## B — SUNUM FORMATI
**Abim (`0533...`) cevabı:** `here.now` (`sunum.trio-prime.com`) hızlı (`hızlıca gönderilir`) ideal. Normal site (`sunumu/index.html` — `TRIO PRIME`) ileride (`ileride gerekli olabilir`) gerekli.

**Durum:** `sunumu/index.html` (`#goal` `GOAL: ÇALIŞIYOR`) güncel (`TRIOPRIME ONLY`). `Trioprime_bot` (`#General`) `/sunum` (`📋`) çalışıyor. `here.now` (`https://sunum.trio-prime.com/`) linki (`sunumu/index.html`) müşteriye (`0533...`) gönderilebilir (`message_agent` `localhost:1234`).

---

## C — MÜŞTERİ GİRİŞ
**Abim (`0533...`) cevabı:** `Trioprime_bot` (`#General`) — bizim (`Gökcan`, `Kriss`, `Abim`) aramızda (`#General` konu — `Trioprime_op.` `lead-management-agent`). Müşteriye (`0533...`) iletilecek (`sunum.trio-prime.com` linki) `Trioprime_bot` (`Dude`) `/sunum` (`📋`) cevap verir (`A/B/C/D/E` kriter — `Trioprime_op.` `message_agent` `localhost:1234`).

**Not:** `ToxkolLik_bot` (`#Iddaa`) — Iddaa (`iddaa_scraper.py`, `tahminler.csv`) ayrı (`TRIOPRIME ONLY` — karışmaz). `Trioprime_bot` (`TRIOPRIME ONLY`) — Emlak (`sunumu/index.html`).

---

## D — LOGO FORMATI
**Abim (`0533...`) cevabı:** `TRIO PRIME` (`trio-repo/sunumu/index.html` — `#0f2e1f` yeşil, `#c8a96e` altın, `#f4f1ea` krem, `Playfair Display` başlık, `Inter` gövde, `9:16` dikey format `Reels` tarzı (`hook` — `kanca` 3 saniye)).

**Durum:** `static_mirror.html` (`6046 byte` — `#0f171b`, `#f3e300`, `#008641`) mevcut (`#General`). `sunumu/index.html` (`TRIO PRIME`) güncel (`TRIOPRIME ONLY`).

---

## E — FAZ SIRASI
**Abim (`0533...`) cevabı:** Faz sırası (`gunluk_rapor.py` — `cron` `08:00`):
1. **Günlük scraping** (`iddaa_scraper.py` — belirli aralık: `cron` `08:00`, `11:00`, `14:00`, `17:00`, `20:00`?)
2. **Yeni ilanlar taranacak** (`gunluk_rapor.py` — `tahminler.csv` güncelleme)
3. **Resimler hazırlanacak** (`obsidyen` / `vault` — `9:16` `Reels` tarzı, `TRIO PRIME` logo formatında — `static_mirror.html` tarzı)
4. **Obsidyen'e (`vault_wiki/`) depolanacak** (`trio-prime.md`, `iddaa-taktik-analizi.md` — `Markdown Wiki` — Faz 3 `TAMAM`)
5. **Müşteriye (`0533...`) sunuma hazır** (`sunumu/index.html` — `#goal` — `GOAL: ÇALIŞIYOR` — `Trioprime_op.` `message_agent` `localhost:1234`)

**Durum:** Faz 4 (`effort` — `gunluk_rapor.py` `--effort light/medium/high`) `BASLATILDI` (`faz4_basladi.md`). Faz 5 (`cron` — `gunluk_rapor.py` `08:00`) `HAZIR` (`cron` ayarı `gunluk_rapor.py` içinde). Faz 6 (`Composio` — `read-only`, `prompt injection`) + Faz 7 (`Log` — `gunluk_log.json`) `HAZIR`.

---

## SONUÇ
`Trioprime_bot` (`TRIOPRIME ONLY`) `/sunum` (`📋`) veya `/status` (`🎯`) yazarsa bot (`Dude`) cevap verir (`TRIO PRIME` — `sunumu/index.html`). `message_agent` (`93e84...` `localhost:1234` — `401` kaldırıldı). Faz 4 (`effort`) `BASLATILDI`. Faz 5-7 (`cron`, `Composio`, `Log`) `HAZIR`. `A/B/C/D/E` (`abim` `0533...`) cevap alınınca (`Trioprime_bot` `/sunum` veya `message_agent`) — bu gece (`22:xx`) Faz 5 (`cron` — `gunluk_rapor.py` `08:00`) başlatılabilir. 🟢
