# 🎯 İddaa Taktik Analiz Sistemi
> Advanced AI Agent System for Iddaa Betting & Analytics

## 📁 Directory Structure

```text
/Projects/IdddaaaProject/
├── ALGORITMA_ENTEGRASYON.md
├── algoritma_parametreleri.json
├── analiz_raporu.json
├── analiz_sistemi.py
├── bugun_analiz.md
├── dev_notes/
├── gunluk_rapor.py
├── hata_payi_analizi.md
├── iddaa_scraper.py
├── oran_kontrol.py
├── README.md
├── site_olustur.py
├── sonuclar.csv
├── tahminler.csv
└── static_mirror.html
```

## 📊 Project Overview

This project is focused on creating a comprehensive system for analyzing betting odds and making predictions for football matches. It leverages various APIs and data sources to provide insights and predictions.

### Key Features

1. **Data Collection**: Automated scraping of betting data from multiple sources
2. **Prediction Analysis**: Advanced analysis of betting data with statistical methods
3. **Reporting**: Automated generation of reports and analysis
4. **Integration**: Seamless integration with various APIs

### Files

- `iddaa_scraper.py`: Main script for scraping betting data
- `gunluk_rapor.py`: Daily report generator
- `oran_kontrol.py`: Odds control script
- `analiz_sistemi.py`: Analysis system
- `tahminler.csv`: Predictions
- `sonuclar.csv`: Results
- `algoritma_parametreleri.json`: Parameters and update recommendations
- `dev_notes/`: API reverse engineering notes (exploration scripts)
- `hata_payi_analizi.md`: Error payout analysis
- `README.md`: Project documentation
- `site_olustur.py`: Site creation script

### Output Directory: `/data/iddaa/`

- `bulten.json`: Raw bulletin
- `bulten.csv`: Bulletin table
- `bulten.md`: Bulletin Markdown
- `analiz_raporu.md`: **Main report** (offers)
- `analiz_raporu.json`: Report JSON
- `gunluk_log.json`: Odds tracker records

### Usage

```bash
cd /home/rw/Projects/IdddaaaProject
VENV=/home/rw/.hermes/hermes-agent/venv/bin/python

# Bülteni çek
$ VENV iddaa_scraper.py --json

# Tam akış (çek + analiz)
$ VENV gunluk_rapor.py

# Sadece analiz (bülteni yeniden çekme)
$ VENV gunluk_rapor.py --skip-scrape

# Sadece Süper Lig
$ VENV gunluk_rapor.py --lig 584

# Oran-yok izleyicisi
$ VENV oran_kontrol.py            # sessiz (değişiklik yoksa çıktı yok)
$ VENV oran_kontrol.py --verbose  # tüm adımları yazdır

# Hata payı analizi (sonuçlar girildikten sonra)
$ VENV analiz_sistemi.py
```

### Metrics

```bash
# Hata payı / sapma / başarı oranı / güven korelasyonu
$ VENV analiz_sistemi.py
```

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Existing Status (21 October 2026)

| Metric | Value |
|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### Known Limitations

- **Super League odds delayed**: Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory**: Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session**: CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires**: No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable**: POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21**: System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metric | Value |
|---|---|
| Evaluable predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:**Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.

### 📈 Results

1. Write match results to `sonuclar.csv` (İY score **must** be written — İY KG Var is tied in the first half)
2. Add `dogru_mu` (Yes/No) and `hata_payi` (0/1) to `tahminler.csv`
3. `python3 analiz_sistemi.py` → MAE, sapma, success rate, security correlation

### Metrics

| Metrik | Mükemmel | İyi | Orta | Kötü |
|---|---|---|---|---|
| MAE | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| Std Dev | < 0.2 | 0.2-0.4 | > 0.4 | — |

### Current Status (21 October 2026)

| Metrik | Value |
|---|---|---|---|
| Eligible predictions | 2 |
| Correct | 1 |
| Success rate | %50 |
| MAE | 0.5 |
| Std Dev | 0.7071 |

### ⚠️ Known Limitations

- **Süper Lig oranları gecikir:** Super League matches go unbet until match day, `type=0` bulletin catches them late. `oran_kontrol.py` tracks these.
- **`/data/` directory:** Created with `pkexec` (PolicyKit GUI password dialog) → `/data/iddaa` (`rw:users`). Use `pkexec` for root-owned folders; `sudo` won't work without a password.
- **Cron output not delivered to this session:** CLI/HTTP sessions have no live delivery channel; outputs are saved to files (`cronjob list` shows them).
- **Mackolik scraping requires:** No public API; speed limit ~2s/request.
- **`markets_by_id` endpoint not usable:** POST but body format unknown (returns 500); markets come from `events`.

### 📜 Update History

- **2026-10-21:** System installed. Sportsbook API reverse-engineered, scraper + prediction motor + odds watcher written, 2 cron jobs created.
