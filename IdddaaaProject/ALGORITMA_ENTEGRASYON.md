# Iddaa Taktik Analiz - Algoritma Geliştirme ve Entegrasyon Rehberi

## 1. Mevcut Algoritma Parametreleri

### Transfermarkt Katmanı (Kadro & Piyasa Değeri)
- Kadro Değer Oranı Eşiği: %40 (favori takım rakibinden en az %40 daha değerli)
- Eksik/Sakatlık Değer Kaybı: Saha içi aktif kadro değeri hesaplaması
- Kilit Player Skoru: Değeri yüksek hücum/orta saha oyuncularının ilk 11'de başlaması

### Mackolik & Taktiksel Katman (Diziliş, Baskı & Form)
- Diziliş & Stil: 4-3-3, 3-4-3, hücum yönlü 4-2-3-1
- İlk Yarı İstatistikleri: Son 10 maçlık periyotta İY gol atma/yeme, korner, isabetli şut
- Geçiş Savunması Zaafları: Yüksek savunma çizgisiyle oynayan takımlar

### İddaa Bülten Filtresi (Hedef Seçenek Matrisi)

#### 🅰️ İY KG Var Seçimi İçin:
- İki takımın da son 6 maçının en az %65'inde ilk yarı gol atılmış/yenmiş
- İki takımın da hücum hattı Transfermarkt değeri lig ortalamasının üzerinde
- İki takımın da tempoyu maç başında yüksek tutan baskılı dizilişle (4-3-3 vs 4-2-3-1) sahaya çıkması

#### 🅱️ 1. Yarı ve 2. Yarı Gol Olur Seçimi İçin:
- Toplam Maç Başı Gol Beklentisi (xG) 2.75 üzeri
- Takımların fiziksel dayanıklılık/ikinci yarı skor üretme oranı %60 üzeri
- İki takımın da 90 dakikaya yayılan yüksek şut ve korner temposu

#### 🅲️ 1. Yarı Sonucu (İY 1 / İY 2) Seçimi İçin:
- Favori takımın Transfermarkt kadro değeri rakibinden en az %40 daha fazla
- İç sahada/deplasmanda ilk 30 dakikada en çok gol atan takımlar
- Ön alan presi yüksek (High Press) takımlar

## 2. Bulunan Algoritma Repo'ları

### 2.1 ProphitBet - Machine Learning Soccer Bet Prediction
- **URL:** https://github.com/kochlisGit/ProphitBet-Soccer-Bets-Predictor
- **Açıklama:** Takım form analizi, maç istatistikleri hesaplama, ML yöntemleriyle maç sonucu tahmini
- **Kullanım:** Form analizi ve maç istatistikleri hesaplama modülü
- **Entegrasyon:** `form_analizi()` fonksiyonu olarak eklenebilir

### 2.2 Dixon-Coles Football Match Predictor
- **URL:** https://github.com/Mintahandrews/football-predictor
- **Açıklama:** Dixon-Coles Poisson modeli ile maç sonucu tahmini (EPL, La Liga, Bundesliga)
- **Kullanım:** Poisson dağılımı ile gol beklentisi (xG) hesaplama
- **Entegrasyon:** `xg_hesapla()` fonksiyonu olarak eklenebilir

### 2.3 Football Corners Forecast
- **URL:** https://github.com/danielsaed/futbol_corners_forecast
- **Açıklama:** XGBoost regresyon modeli ile korner tahmini
- **Kullanım:** Korner tahmini ve over/under olasılık hesaplama
- **Entegrasyon:** `korner_tahmini()` fonksiyonu olarak eklenebilir

### 2.4 Elite Football Predictor
- **URL:** https://nation99.github.io/
- **Açıklama:** Form gücü, xG, xGA, sakatlık, taktik, piyasa hareketi, risk filtreleme
- **Kullanım:** Çok faktörlü analiz motoru (form + xG + xGA + sakatlık + taktik + piyasa)
- **Entegrasyon:** `cok_faktorlu_analiz()` fonksiyonu olarak eklenebilir

### 2.5 Football Prediction (Multiplicative Rating Model)
- **URL:** https://github.com/tanjt107/football-prediction
- **Açıklama:** Çarpımsal rating modeli ile gol beklentisi hesaplama
- **Kullanım:** Takım rating hesaplama ve gol beklentisi
- **Entegrasyon:** `rating_hesapla()` fonksiyonu olarak eklenebilir

## 3. Algoritma Güncellemesi Önerileri

### 3.1 Transfermarkt Değer Farkı Eşiği
- **Mevcut:** %40
- **Öneri:** %35'e düşürülebilir (daha fazla maç dahil edilir)
- **Gerekçe:** %40 eşiği çok katı, bazı değerli maçlar kaçırılıyor

### 3.2 Mackolik Baskı Oranı Eşiği
- **Mevcut:** %60
- **Öneri:** %55'e düşürülebilir
- **Gerekçe:** Baskı oranı %55-60 aralığındaki takımlar da yüksek tempolu oynuyor

### 3.3 xG Eşiği (Her İki Yarıda Gol Var)
- **Mevcut:** 2.75
- **Öneri:** 2.5'e düşürülebilir
- **Gerekçe:** 2.5-2.75 aralığındaki maçlar da yeterli gol potansiyeline sahip

### 3.4 İY KG Var İçin Son Maç Eşiği
- **Mevcut:** Son 6 maçta %65+
- **Öneri:** Son 8 maçta %60+
- **Gerekçe:** Daha geniş örneklem, daha stabil sonuç

### 3.5 Güven Skoru Minimum
- **Mevcut:** 7.5
- **Öneri:** 7.0'a düşürülebilir (riskli maçlar dahil)
- **Gerekçe:** 7.0-7.5 aralığındaki maçlar da değerli olabilir

## 4. Yeni Algoritma Modülleri

### 4.1 Form Analizi (ProphitBet'den)
```python
def form_analizi(takim, son_mac_sayisi=5):
    """
    Takımın son maçlarındaki performansını analiz eder.
    Gol atma, gol yeme, puan ortalaması hesaplar.
    """
    # ProphitBet algoritması
    form_skoru = (gol_atma_ort + puan_ort * 0.5 - gol_yeme_ort * 0.3)
    return form_skoru
```

### 4.2 xG Hesaplama (Dixon-Coles'den)
```python
def xg_hesapla(takim_ev, takim_dep, lig_ort_gol):
    """
    Dixon-Coles Poisson modeli ile xG hesaplar.
    """
    import numpy as np
    from scipy.stats import poisson
    
    # Rating hesaplama
    home_rating = takim_ev['rating']
    away_rating = takim_dep['rating']
    
    # Gol beklentisi
    home_xg = (home_rating / away_rating) * lig_ort_gol
    away_xg = (away_rating / home_rating) * lig_ort_gol
    
    return home_xg, away_xg
```

### 4.3 Çok Faktörlü Analiz (Elite Football Predictor'den)
```python
def cok_faktorlu_analiz(mac_data):
    """
    Form, xG, xGA, sakatlık, taktik, piyasa hareketi
    faktörlerini birleştirerek analiz yapar.
    """
    faktorler = {
        'form': mac_data['form_gucu'] * 0.25,
        'xg': mac_data['xg'] * 0.20,
        'xga': (1 - mac_data['xga']) * 0.15,
        'sakatlik': (1 - mac_data['sakatlik_orani']) * 0.15,
        'taktik': mac_data['taktik_stabilite'] * 0.15,
        'piyasa': mac_data['piyasa_hareketi'] * 0.10
    }
    
    toplam_skor = sum(faktorler.values())
    return toplam_skor, faktorler
```

### 4.4 Korner Tahmini (Football Corners Forecast'dan)
```python
def korner_tahmini(takim_ev, takim_dep):
    """
    XGBoost regresyon modeli ile korner tahmini.
    """
    # XGBoost modeli ile korner tahmini
    ev_korner = takim_ev['avg_corners'] * takim_ev['corner_rate']
    dep_korner = takim_dep['avg_corners'] * takim_dep['corner_rate']
    toplam = ev_korner + dep_korner
    
    # Over/Under olasılıkları
    over_8_5 = 1 if toplam > 8.5 else 0
    over_9_5 = 1 if toplam > 9.5 else 0
    over_10_5 = 1 if toplam > 10.5 else 0
    
    return toplam, over_8_5, over_9_5, over_10_5
```

## 5. Hata Payı ve Sapma Değerlendirme

### 5.1 Metrikler
- **MAE (Mean Absolute Error):** Ortalama mutlak hata
- **RMSE (Root Mean Square Error):** Kök ortalama kare hatası
- **Başarı Oranı:** Doğru tahmin / Toplam tahmin
- **Güven Skoru Korelasyonu:** Güven skoru vs başarı oranı

### 5.2 Değerlendirme Kriterleri
- MAE < 0.3: Mükemmel
- MAE 0.3-0.5: İyi
- MAE 0.5-0.7: Orta
- MAE > 0.7: Kötü

### 5.3 Sapma (Standart Sapma)
- Sapma < 0.2: Stabil
- Sapma 0.2-0.4: Orta tutarsızlık
- Sapma > 0.4: Yüksek tutarsızlık

## 6. Veri Kaynakları

### 6.1 iddaa.com
- URL: https://www.iddaa.com/program/futbol
- Veri: Bülten, maç kodları, oranlar, tarih/saat
- Çekim: curl_cffi 0.16.3

### 6.2 Mackolik.com
- URL: https://www.mackolik.com
- Veri: Diziliş, baskı istatistikleri, korner, şut, xG
- Çekim: Web scraping

### 6.3 Transfermarkt
- URL: https://www.transfermarkt.com
- Veri: Kadro değeri, sakatlık, piyasa değeri
- Çekim: Web scraping / API

### 6.4 here.now (Yayınlanan Site)
- URL: https://awake-essence-t5cn.here.now
- Veri: Günlük analiz sonuçları, SMA/EMA/Bollinger metrikleri
- Durum: Veri tabanı boş ("No data yet")

## 7. Entegrasyon Planı

### Adım 1: Veri Toplama
1. iddaa.com bültenini çek (curl_cffi)
2. Mackolik.com'dan baskı istatistikleri çek
3. Transfermarkt'tan kadro değerlerini çek

### Adım 2: Analiz
1. Transfermarkt kadro değeri analizi
2. Mackolik baskı istatistikleri analizi
3. Çok faktörlü analiz (form + xG + xGA + sakatlık + taktik + piyasa)
4. A/B/C pazar filtresi (Güven ≥ 7.5)

### Adım 3: Tahmin
1. İY 1 / İY X / İY 2
2. İY KG Var
3. Her İki Yarıda Gol Var

### Adım 4: Takip ve Değerlendirme
1. Tahminleri CSV'ye kaydet
2. Sonuçları CSV'ye kaydet
3. Hata payı ve sapma hesapla
4. Algoritma parametrelerini güncelle

### Adım 5: Yayın
1. here.now'a güncelle
2. Telegram Toxkolikk grubuna gönder
3. Analiz raporu oluştur

## 8. Cron Job Önerisi

```
# Her 3 saatte bir çalıştır
*/180 * * * * python3 /home/rw/Projects/IdddaaaProject/analiz_sistemi.py

# Günlük analiz (sabah 09:00)
0 9 * * * python3 /home/rw/Projects/IdddaaaProject/gunluk_analiz.py
```

## 9. LM Studio Entegrasyonu

- **Model:** openai/gpt-oss-20b (LM Studio localhost:1234)
- **Context:** 65536
- **Kullanım:** Tahmin tablosu oluşturma, analiz raporu yazma
- **Performans:** İlk yanıt ~1.5-2 dk, sonrası ~15-45 sn

## 10. Gelecek Adımlar

1. [ ] Transfermarkt API entegrasyonu (Docker)
2. [ ] Mackolik scraping otomasyonu
3. [ ] Qwen3-Coder-30B ile kodlama görevleri
4. [ ] here.now veri tabanına veri yükleme
5. [ ] Telegram bot entegrasyonu (Toxkolikk)
6. [ ] Günlük sonuç takibi ve hata payı hesaplama
7. [ ] Algoritma parametre güncellemesi (MAE < 0.3 hedefi)
EOF