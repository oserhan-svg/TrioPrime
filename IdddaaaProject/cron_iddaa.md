# Iddaa Tahmin Motoru — Faz 5 (Cron — 08:00)
# /etc/cron.d/iddaa-tahmin veya crontab -e

# Faz 5: Günlük rapor (gunluk_rapor.py) — 08:00 sabah (Sessizlik Kuralı: 0 öneri -> sessiz)
0 8 * * * root /home/rw/.hermes/hermes-agent/venv/bin/python /home/rw/Projects/IdddaaaProject/gunluk_rapor.py --effort medium >> /data/iddaa/gunluk_log.json 2>&1

# Faz 5: Günlük scraping (iddaa_scraper.py) — 11:00, 14:00, 17:00, 20:00 (belirli aralık)
0 11,14,17,20 * * * root /home/rw/.hermes/hermes-agent/venv/bin/python /home/rw/Projects/IdddaaaProject/iddaa_scraper.py --json --out /data/iddaa/ >> /dev/null 2>&1

# Faz 5: Oran izleyici (oran_kontrol.py) — sessiz (değişiklik yoksa çıktı yok)
30 9,12,15,18 * * * root /home/rw/.hermes/hermes-agent/venv/bin/python /home/rw/Projects/IdddaaaProject/oran_kontrol.py >> /dev/null 2>&1
