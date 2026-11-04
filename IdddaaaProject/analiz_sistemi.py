"""
İddaa Taktik Analiz - Hata Payı ve Sapma Değerlendirme Sistemi
Bu script, tahmin sonuçlarını takip eder ve hata payı/sapma hesaplaması yapar.
"""

import csv
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

# Dosya yolları
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TAHMINLER_CSV = os.path.join(BASE_DIR, "tahminler.csv")
SONUCLAR_CSV = os.path.join(BASE_DIR, "sonuclar.csv")
RAPOR_JSON = os.path.join(BASE_DIR, "analiz_raporu.json")
ALGORITMA_JSON = os.path.join(BASE_DIR, "algoritma_parametreleri.json")

# Algoritma parametreleri (güncellenebilir)
ALGORITMA_PARAMS = {
    "kadro_deger_orani_esigi": 0.40,  # Transfermarkt: %40+ değer farkı
    "baski_orani_esigi": 0.60,  # Mackolik: %60+ baskı oranı
    "xg_esigi": 2.75,  # Her İki Yarıda Gol Var: xG > 2.75
    "iy_kg_var_son_mac_esigi": 0.65,  # Son 6 maçta %65+ İY gol
    "guven_skoru_min": 7.5,
    "iy_kg_var_hucum_deger_esigi": "lig_ortalamasi",  # Hücum hattı Transfermarkt değeri
    "her_iki_yari_fiziksel_esigi": 0.60,  # Fiziksel dayanıklılık > %60
    "iy_kg_var_tempo_esigi": 0.65,  # Tempoyu maç başında yüksek tutma
    "guncelleme_tarihi": None,
    "versiyon": "1.0"
}

def baslangic_dosyalarini_olustur():
    """İlk kurulum: gerekli dosyaları oluşturur."""
    # tahminler.csv
    if not os.path.exists(TAHMINLER_CSV):
        with open(TAHMINLER_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'tarih', 'mac_kodu', 'lig', 'ev_sahibi', 'deplasman',
                'onerilen_bahis', 'guven_skoru', 'transfermarkt_ev',
                'transfermarkt_dep', 'mackolik_baski_notu', 'tahmin_sonucu',
                'gercek_sonuc', 'dogru_mu', 'hata_payi'
            ])
    
    # sonuclar.csv (gerçek sonuçlar için ayrı dosya)
    if not os.path.exists(SONUCLAR_CSV):
        with open(SONUCLAR_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'tarih', 'mac_kodu', 'lig', 'ev_sahibi', 'deplasman',
                'gercek_iy_sonuc', 'gercek_iy_kg_var', 'gercek_her_iki_yari_gol',
                'gercek_toplam_gol', 'gercek_korner', 'gercek_sut', 'notlar'
            ])
    
    # algoritma parametreleri
    if not os.path.exists(ALGORITMA_JSON):
        ALGORITMA_PARAMS['guncelleme_tarihi'] = datetime.now().isoformat()
        with open(ALGORITMA_JSON, 'w', encoding='utf-8') as f:
            json.dump(ALGORITMA_PARAMS, f, indent=2, ensure_ascii=False)

def tahmin_ekle(tarih, mac_kodu, lig, ev_sahibi, deplasman, onerilen_bahis,
                guven_skoru, transfermarkt_ev, transfermarkt_dep, mackolik_baski_notu,
                tahmin_sonucu):
    """Yeni bir tahmin kaydı ekler."""
    with open(TAHMINLER_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            tarih, mac_kodu, lig, ev_sahibi, deplasman, onerilen_bahis,
            guven_skoru, transfermarkt_ev, transfermarkt_dep, mackolik_baski_notu,
            tahmin_sonucu, '', '', ''  # gerçek sonuç, doğru_mu, hata_payi boş
        ])

def sonuc_ekle(tarih, mac_kodu, lig, ev_sahibi, deplasman, gercek_iy_sonuc,
               gercek_iy_kg_var, gercek_her_iki_yari_gol, gercek_toplam_gol,
               gercek_korner, gercek_sut, notlar=''):
    """Gerçek maç sonuçlarını kaydeder."""
    with open(SONUCLAR_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            tarih, mac_kodu, lig, ev_sahibi, deplasman, gercek_iy_sonuc,
            gercek_iy_kg_var, gercek_her_iki_yari_gol, gercek_toplam_gol,
            gercek_korner, gercek_sut, notlar
        ])

def hata_payi_hesapla(tahmin, gercek):
    """İki tahmin arasındaki hata payını hesaplar (0 veya 1)."""
    return 0 if tahmin == gercek else 1

def sapma_hesapla(hata_listesi):
    """Hata listesinden standart sapma hesaplar."""
    if len(hata_listesi) < 2:
        return 0.0
    n = len(hata_listesi)
    ortalama = sum(hata_listesi) / n
    varyans = sum((x - ortalama) ** 2 for x in hata_listesi) / (n - 1)
    return varyans ** 0.5

def analiz_raporu_olustur():
    """Tüm tahminleri analiz eder ve rapor oluşturur."""
    rapor = {
        'toplam_tahmin': 0,
        'dogru_tahmin': 0,
        'basari_orani': 0.0,
        'ortalama_guven_skoru': 0.0,
        'hata_payi_mae': 0.0,
        'sapma': 0.0,
        'bahis_turu_basari': defaultdict(lambda: {'toplam': 0, 'dogru': 0}),
        'guven_skoru_analizi': defaultdict(lambda: {'toplam': 0, 'dogru': 0}),
        'tarih_bazli': defaultdict(lambda: {'toplam': 0, 'dogru': 0}),
        'lig_bazli': defaultdict(lambda: {'toplam': 0, 'dogru': 0}),
        'oneriler': []
    }
    
    try:
        with open(TAHMINLER_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            tahminler = list(reader)
    except FileNotFoundError:
        return rapor
    
    hata_listesi = []
    guven_skorlari = []
    
    for t in tahminler:
        if not t.get('gercek_sonuc') or not t.get('dogru_mu'):
            continue  # Sonuç girilmemiş
        
        rapor['toplam_tahmin'] += 1
        dogru_str = t['dogru_mu'].strip().lower()
        dogru = dogru_str in ('evet', 'true', '1', 'yes')
        hata = 0 if dogru else 1
        hata_listesi.append(hata)
        
        if dogru:
            rapor['dogru_tahmin'] += 1
        
        # Bahis türü bazlı
        bahis = t['onerilen_bahis']
        rapor['bahis_turu_basari'][bahis]['toplam'] += 1
        if dogru:
            rapor['bahis_turu_basari'][bahis]['dogru'] += 1
        
        # Güven skoru analizi
        try:
            gs = float(t['guven_skoru'])
            guven_skorlari.append(gs)
            gs_bucket = f"{int(gs)}-{int(gs)+1}"
            rapor['guven_skoru_analizi'][gs_bucket]['toplam'] += 1
            if dogru:
                rapor['guven_skoru_analizi'][gs_bucket]['dogru'] += 1
        except (ValueError, TypeError):
            pass
        
        # Tarih bazlı
        rapor['tarih_bazli'][t['tarih']]['toplam'] += 1
        if dogru:
            rapor['tarih_bazli'][t['tarih']]['dogru'] += 1
        
        # Lig bazlı
        rapor['lig_bazli'][t['lig']]['toplam'] += 1
        if dogru:
            rapor['lig_bazli'][t['lig']]['dogru'] += 1
    
    if rapor['toplam_tahmin'] > 0:
        rapor['basari_orani'] = round(rapor['dogru_tahmin'] / rapor['toplam_tahmin'] * 100, 2)
        rapor['hata_payi_mae'] = round(sum(hata_listesi) / len(hata_listesi), 4)
        rapor['sapma'] = round(sapma_hesapla(hata_listesi), 4)
    
    if guven_skorlari:
        rapor['ortalama_guven_skoru'] = round(sum(guven_skorlari) / len(guven_skorlari), 2)
    
    # Öneriler oluştur
    rapor['oneriler'] = algoritma_onerileri_olustur(rapor)
    
    # defaultdict'ları normal dict'e çevir (JSON serialization)
    rapor['bahis_turu_basari'] = dict(rapor['bahis_turu_basari'])
    rapor['guven_skoru_analizi'] = dict(rapor['guven_skoru_analizi'])
    rapor['tarih_bazli'] = dict(rapor['tarih_bazli'])
    rapor['lig_bazli'] = dict(rapor['lig_bazli'])
    
    with open(RAPOR_JSON, 'w', encoding='utf-8') as f:
        json.dump(rapor, f, indent=2, ensure_ascii=False)
    
    return rapor

def algoritma_onerileri_olustur(rapor):
    """Analiz sonuçlarına göre algoritma güncelleme önerileri oluşturur."""
    oneriler = []
    
    # Bahis türü bazlı analiz
    for bahis, stats in rapor['bahis_turu_basari'].items():
        if stats['toplam'] >= 5:
            basari = stats['dogru'] / stats['toplam'] * 100
            if basari < 50:
                oneriler.append({
                    'bahis_turu': bahis,
                    'basari_orani': round(basari, 1),
                    'oneri': f"{bahis} seçiminde başarı oranı %{basari:.1f} - eşikler gözden geçirilmeli",
                    'oncelik': 'YÜKSEK'
                })
            elif basari >= 70:
                oneriler.append({
                    'bahis_turu': bahis,
                    'basari_orani': round(basari, 1),
                    'oneri': f"{bahis} seçiminde başarı oranı %{basari:.1f} - mevcut parametreler korunabilir",
                    'oncelik': 'DÜŞÜK'
                })
    
    # Güven skoru vs başarı analizi
    for bucket, stats in rapor['guven_skoru_analizi'].items():
        if stats['toplam'] >= 3:
            basari = stats['dogru'] / stats['toplam'] * 100
            if basari < 60 and int(bucket.split('-')[0]) >= 9:
                oneriler.append({
                    'bahis_turu': 'Güven Skoru',
                    'basari_orani': round(basari, 1),
                    'oneri': f"Güven skoru {bucket} aralığında başarı %{basari:.1f} - aşırı güven (overconfidence) tespit edildi",
                    'oncelik': 'ORTA'
                })
    
    # Genel başarı oranı
    if rapor['toplam_tahmin'] >= 10:
        if rapor['basari_orani'] < 55:
            oneriler.append({
                'bahis_turu': 'GENEL',
                'basari_orani': rapor['basari_orani'],
                'oneri': f"Genel başarı oranı %{rapor['basari_orani']} - algoritma parametreleri gözden geçirilmeli",
                'oncelik': 'YÜKSEK'
            })
        elif rapor['basari_orani'] >= 70:
            oneriler.append({
                'bahis_turu': 'GENEL',
                'basari_orani': rapor['basari_orani'],
                'oneri': f"Genel başarı oranı %{rapor['basari_orani']} - mevcut parametreler korunabilir",
                'oncelik': 'DÜŞÜK'
            })
    
    # Hata payı analizi
    if rapor['hata_payi_mae'] > 0.5:
        oneriler.append({
            'bahis_turu': 'HATA PAYI',
            'basari_orani': round((1 - rapor['hata_payi_mae']) * 100, 1),
            'oneri': f"MAE (Mean Absolute Error) = {rapor['hata_payi_mae']} - hata payı yüksek, eşikler gözden geçirilmeli",
            'oncelik': 'YÜKSEK'
        })
    
    # Sapma analizi
    if rapor['sapma'] > 0.4:
        oneriler.append({
            'bahis_turu': 'SAPMA',
            'basari_orani': round((1 - rapor['sapma']) * 100, 1),
            'oneri': f"Standart sapma = {rapor['sapma']} - tutarsızlık tespit edildi, parametre stabilitesi gözden geçirilmeli",
            'oncelik': 'ORTA'
        })
    
    return oneriler

def algoritma_guncelle(oneriler):
    """Önerilere göre algoritma parametrelerini günceller."""
    global ALGORITMA_PARAMS
    
    with open(ALGORITMA_JSON, 'r', encoding='utf-8') as f:
        params = json.load(f)
    
    for oneri in oneriler:
        if oneri['oncelik'] == 'YÜKSEK':
            # Parametre güncellemesi önerisi
            params['guncelleme_tarihi'] = datetime.now().isoformat()
            params['versiyon'] = f"{float(params['versiyon']) + 0.1:.1f}"
    
    with open(ALGORITMA_JSON, 'w', encoding='utf-8') as f:
        json.dump(params, f, indent=2, ensure_ascii=False)
    
    return params

def rapor_yazdir(rapor):
    """Raporu konsola yazdırır."""
    print("=" * 60)
    print("İDDAA TAKTİK ANALİZ - HATA PAYI VE SAPMA RAPORU")
    print("=" * 60)
    print(f"Toplam Tahmin: {rapor['toplam_tahmin']}")
    print(f"Doğru Tahmin: {rapor['dogru_tahmin']}")
    print(f"Başarı Oranı: %{rapor['basari_orani']}")
    print(f"Ortalama Güven Skoru: {rapor['ortalama_guven_skoru']}")
    print(f"Hata Payı (MAE): {rapor['hata_payi_mae']}")
    print(f"Sapma (Std Dev): {rapor['sapma']}")
    print()
    
    print("--- Bahis Türü Bazlı Başarı ---")
    for bahis, stats in rapor['bahis_turu_basari'].items():
        if stats['toplam'] > 0:
            basari = stats['dogru'] / stats['toplam'] * 100
            print(f"  {bahis}: {stats['dogru']}/{stats['toplam']} (%{basari:.1f})")
    
    print()
    print("--- Güven Skoru vs Başarı ---")
    for bucket, stats in rapor['guven_skoru_analizi'].items():
        if stats['toplam'] > 0:
            basari = stats['dogru'] / stats['toplam'] * 100
            print(f"  Güven {bucket}: {stats['dogru']}/{stats['toplam']} (%{basari:.1f})")
    
    print()
    print("--- Öneriler ---")
    for oneri in rapor['oneriler']:
        print(f"  [{oneri['oncelik']}] {oneri['oneri']}")
    
    print("=" * 60)

if __name__ == "__main__":
    baslangic_dosyalarini_olustur()
    rapor = analiz_raporu_olustur()
    rapor_yazdir(rapor)
    print("\nRapor JSON dosyasına kaydedildi:", RAPOR_JSON)
    print("Algoritma parametreleri:", ALGORITMA_JSON)