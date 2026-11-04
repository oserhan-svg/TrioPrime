# 🏠 TRIO PRIME — Tri Emlak Portföy Sistemi

## 📋 Proje Özeti

**TrioPrime** = Twitter tarafında işleyen portföy ve oyun direktifi.  
Araç: **Ozancan Serhan**. Hedef: Ayvalık / Cunda / Altınova / Gömeç / İstanbul bölgesindeki konutları toplamak ve müşteriye sunum yapmak.

---

## 🧱 Mimarisi

```
trio-repo/
├── sunumu/
│   └── index.html          # Portföy web sitesi (sahibiye)
├── kontrol.py              # Sistem kontrol scripti
├── IDEA.md                 # Proje direktifi
└── .worktrees/             # Git worktree (faze-1, 2, 3, 4)
```

### Künyelerin Bölümleri

```
vault_wiki/
├── projects/               # Proje bazlı dokümanlar
│   ├── trio-prime.md       # Trioprime projesinin ana belgesi
│   └── free-llm-api.md     # AI API kaynakları
├── agents/                 # Agent/çalışanlar belgeleri
│   ├── lead-management.md  # Operasyon yöneticisi
│   └── trio-worker.md      # Çalışan agent
└── logs/                   # Günlük çalışma kayıtları
    └── faz-durumu.md       # Faz durumu takip kaydı
```

---

## 🧑‍💼 Rol Dağılımı

| Rol | Kim? | Görev |
|-----|------|-------|
| **Lead Management Agent** | Ozancan Serhan | Operasyon yönetimi, müşteri iletişimi, portföy yönetimi |
| **Trio Worker** | Hermes | İlan scraping, veri analizi, raporlama |

---

## 🚀 Başlangıç

```bash
# Proje klasörüne geç
cd /home/rw/Projects/trio-repo

# Web sitesini yerel sunucuda aç
python3 -m http.server 8000

# Tarayıcıda aç (http://localhost:8000/sunumu/index.html)
```

---

## 📊 Kriterler

| Kriter | Açıklama |
|--------|----------|
| **Aktif İlan** | Satılık / Kiralık |
| **Gayrimenkul Tipi** | Daire / Villa / Müstakil / Ofis / Büro |
| **Mahalle** | Ali Çetinkaya / Cunda / Altınova / Gömeç / İstanbul |
| **Fiyat Üst Sınırı** | TL |
| **Oda Sayısı** | 1+1 / 2+1 / 3+1 / 4+1 |
| **En Az m²** | m² |

---

## 🛠️ Teknolojiler

- **Web:** HTML/CSS/JavaScript (tarayıcıda çalışır)
- **Veri Kaynağı:** Sahibinden.com (ifade: "asked/delivered")
- **AI:** OpenRouter (free) — `openai/gpt-oss-20b`
- **İletişim:** Telegram (+90 533 378 68 94)

---

## 📅 Kapanış

- **Sıfır Halüsinasyon:** Veriler göz önünde bulundurulmuştur.
- **Cilt:** Kredikli, test edilmiştir.
- **Lisans:** Özgün, Özancan Serhan.

---
Eğer sorunun varsa **Cevap Sorusu:**
Veri yoksa "Veri yok" denir; asla uydurma veri üretilmez. (Sıfır Halüsinasyon İlkesi)
