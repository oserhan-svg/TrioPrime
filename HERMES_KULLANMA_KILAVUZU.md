# 📘 Hermes Agent Kullanma Kılavuzu — TrioPrime

**Hazırlayan:** Kriss (AI Operator / Back Office — Gökcan & Ozancan)  
**Hedef platform:** Hermes Agent (Nous Research), masaüstü uygulaması  
**Dil:** Türkçe  
**Aktif profil:** default  
**Doğrulama tarihi:** 30 Ekim 2026  

---

## İçindekier

1. [Genel Bakış](#1-genel-bakış)  
2. [Mevcut Kurulumumuz](#2-mevcut-kurulumumuz)  
3. [Neler Yapabiliriz](#3-neler-yapabiliriz)  
4. [Nasıl Konuşmalıyız](#4-nasıl-conuşmalıyız)  
5. [Bellek ve Skill'ler](#5-bellek-ve-skill'ler)  
6. [Otomasyon](#6-otomasyon)  
7. [Güvenlik ve Sınırlar](#7-güvenlik-ve-sınırlar)  
8. [Sık Yapılan Hatalar ve Sorun Giderme](#8-sık-yapılan-hatalar-ve-sorun-giderme)  
9. [Hızlı Başlangıç — İlk Hafta](#9-hızlı-başlangıç---ilk-hafta)  
10. [Kullanmadığımız Ama İşimize Yarayabilecek Özellikler](#10-kullanmadığımız-ama-işimize-yarayabilecek-özellikler)  

[Hızlı Başvuru Özeti — Tek Sayfa](#hızlı-başvuru-özeti---tek-sayfa)

---

## 1. Genel Bakış

**Hermes Agent nedir?**  
Hermes, Nous Research tarafından geliştirilmiş bir AI aracıdır. Sadece sohbet etmekle kalmaz, aynı zamanda bilgisayarınızdaki dosyaları okuyup yazabilir, komut çalıştırabilir, zamanlanmış görevler ayarlayabilir ve Telegram gibi kanallar üzerinden size mesaj gönderebilir.

**Nasıl çalışır?**  
Sizinle sohbet eder, arka planda bir “araç kutusu” kullanarak işleri yerine getirir. Örneğin size bir dosya açmanızı söylemezseniz, doğrudan o dosyayı okuyup içeriği size aktarabilir.

**Bizde nasıl kurulu?**  
- Masaüstü uygulama olarak çalışıyor.  
- Aktif profil: `default` (ana profil). Diğer profiller (ör. `asistan`, `tradeworker`, `trio_worker`) de var ama bizim gündelik kullanımımız `default` üzerinden.  
- İleti kanalı: Telegram. Bot:@`trioprimelab_bot`. Tek aktif kanal, **Ozancan Serhan** ile doğrudan mesaj (DM).  
- Ağ geçidi (gateway) çalışıyor, sürüm `0.21.5`, Telegram bağlantısı aktif.

> 🔍 Doğrulanamadı: Masaüstü uygulamanın tam sürüm numarası ve kurulum tarihi doğrudan dosyadan okunamadı (yukarıdaki 0.21.5, ağ geçidi sürümüdür).

---

## 2. Mevcut Kurulumumuz

Aşağıdaki bilgiler gerçek dosya ve ayar düzeninden doğrulanmıştır.

### Model ve sağlayıcı
| Ayar | Değer | Durum |
|------|-------|-------|
| Varsayılan model | `google/gemini-2.5-flash-preview` | ✅ Doğrulandı |
| Sağlayıcı | NVIDIA (`api.nvidia.com/v1`) | ✅ Doğrulandı |
| Yerel model takma adı | `lmstudio/openai/gpt-oss-20b` (LM Studio) | ⚠️ Tanım var, çalışırlık doğrulanamadı |
| Gemini takma adı | `gemini/gemini-flash-latest` | ⚠️ Tanım var |

### Ses
- Konuşma metni-dönüşümü (STT): Türkçe
- Metin-konuşma (TTS): Piper

### MOA (Çoklu Ajan / Reference Models)
Etkin. Toplama modeli: `nvidia/nemotron-3.5-lightning:free`. Referans modeller: `poolside/laguna-s-2.1:free`, `nvidia/nemotron-3-ultra-550b-a55b:free`.

### Araç setleri (platform_toolsets)
Aşağıdakiler aktif: `a2a`, `browser`, `code_execution`, `computer_use`, `cronjob` (zamanlanmış görev), `delegation`, `file`, `image_gen`, `memory`, `session_search`, `skills`, `terminal`, `todo`, `tts`, `vision`, `web`.

### Telegram kanalları
- Bot 1: `@trioprimelab_bot` (token son 7 hanesi `8684943573`)
- Bot 2: `@ToxkolLik_bot` (token son 7 hanesi `8829341471`)
- Aktif kanal: Telegram DM — **Ozancan Serhan** (`1041604646`)

### Cron / zamanlanmış görevler (default profil)
- `asistan_kontrol.sh` — bot aktifliği, `.env.local`, scraping ve `sunumu/index.html` kontrolü
- `hermes_system_check.sh` — günlük sistem kontrolü (yukarıdakilerle aynı)
- `suggestions.json` — 4 adet bekleyen zamanlanmış görev önerisi (hiçbiri henüz etkinleştirilmemiş, hepsi `pending`):
  1. Günlük özetleme (sabah 08:00)
  2. Önemli posta izleyicisi (her 30 dakikada bir)
  3. Haftalık gözden geçirme (Pazar 18:00)
  4. İşgünü başlangıç hatırlatması (haftaiçi 09:00)

### Diğer altyapı
- Terminal arka ucu: `local`, çalışma dizini `/home/rw/Projects`, zaman aşımı 180 saniye
- Veritabanı: SQLite (`state.db`), WAL modu
- Kanban: etkin (`review_dispatch: true`), dosya `kanban.db`
- Eklenti: `disk-cleanup` etkin
- Kimlik/bellek dosyaları: `SOUL.md`, `identity.md` (Kriss personasını tanımlıyor)

> 🔍 Doğrulanamadı: `.env` dosyası (gizli anahtarlar/tokenlar) doğrudan okunamıyor; bu iyi bir güvenlik uygulamasıdır.  
> 🔍 Doğrulanamadı: LM Studio'nun gerçekten çalışıp çalışmadığı (yerel model alias'ı sadece tanımlı).  
> 🔍 Doğrulanamadı: E-posta entegrasyonunun kurulu olup olmadığı.

---

## 3. Neler Yapabiliriz

Aşağıda iş alanımıza özel somut örnekler var. Her biri Hermes'in gerçek araçlarıyla yapılabilir.

### Gayrimenkul (Trio Emlak / TrioPrime)
- **İlan özetleri:** Sahibinden veya kendi portföyümüzdeki ilanları okuyup, Ayvalık / Cunda / Altınova / Gömeç / İstanbul odaklı kısa özetler çıkarabiliriz.
- **İçerik taslakları:** 9:16 dikey video veya Instagram hikayesi için 3 saniyelik kanca (hook) yazdırabiliriz.
- **Müşteri takibi:** Telefon `0533 378 68 94` ile gelen müşteri notlarını kanban üzerinden takip edebiliriz.

*Örnek komut:*  
`"Ayvalık'taki son 3 ilanımızı alıp her biri için 2 cümlelik bir Türkçe açıklama yaz, pazarlama diliyle."`

### İçerik üretimi
- Blog / sosyal medya yazıları (Türkçe, teknik terimler açılmış)
- Sunum ve kart taslakları (HTML)
- Görsel akış senaryoları (trio-image-pipeline skill'i mevcut)

*Örnek komut:*  
`"Cunda'da satılık bir villa için Instagram hikayesi metni yaz, ilk 3 saniyede kanca olsun, çağrı ile bitsin."`

### İş geliştirme
- İş akışlarını otomatikleştirmek için zamanlanmış görevler kurmak
- Geliştirme notlarını, todo listelerini yönetmek
- Git deposu (`https://github.com/oserhan-svg/TrioPrime`) ile ilgili dokümanları okuma ve güncelleme

*Örnek komut:*  
`"TrioPrime deposundaki IDEA.md'yi oku ve faz 1'deki yapılacakları madde madde listele."`

---

## 4. Nasıl Konuşmalıyız

İyi bir Hermes komutu şunları içerir:
1. **Ne istediğinizi** belirtin.
2. **Hangi konu/bölge** (ör. Ayvalık, Cunda) varsa söyleyin.
3. **Biçim** isterseniz (madde, kısa paragraf, 9:16 metni, vb.).
4. **Doğrulama** isteyebilirsiniz: `"Bu bilgi dosyadan mı yoksa tahmından mı?"`

### İyi örnekler

| Senaryo | Komut örneği |
|---------|-------------|
| İlan özeti | `"Sahibinden'deki Ayvalık ilanlarını özetle, fiyat ve metrekareyi göster."` |
| İçerik | `"Cunda için 3 saniyelik kanca ile bir Instagram hikayesi yaz."` |
| Dosya işi | `"IDEA.md'yi oku ve faz rollout planını Türkçe özetle."` |
| Zamanlama | `"Her sabah 08:00'de bana kısa bir günlük özet gönder."` |
| Kod/teknik | `"TrioPrime reposunda git durumunu kontrol et."` |

### Kötü örnekler (kaçının)

- `"Bir şeyler yap."` — çok genel.
- `"Fiyatı kaç?"` — hangi ilan, hangi bölge?
- `"Tüm dosyaları sil."` — riskli, onay gerektirir.

### Kural: "Doğrulanamadı" işareti
Hermes, bildiği bir şeyden emin değilse ona `"doğrulanamadı"` diye işaret koymalı. Siz de buna dikkat edin; tahmine dayalı bir işlem yapmayın.

---

## 5. Bellek ve Skill'ler

### Bellek
Hermes, konuşmalarınızda geçtiğiniz bilgileri not alabilir ve sonraki oturumlarda hatırlayabilir.  
- **Neler hatırlar:** Sizinle paylaştığınız iş hedefleri, tercih ettiğiniz bölge (Ayvalık/Cunda vb.), telefon numarası (`0533 378 68 94`), proje notları.
- **Nasıl öğrenir:** Söyledikleriniz sohbet geçmişine ve `state.db` veritabanına kaydedilir. `memories/` klasörü de var.

> 🔍 Doğrulanamadı: Ne kadar uzun süre bellek tutar, otomatik özetleme var mı (belli değil).

### Skill'ler
Skill'ler, Hermes'e yeni yetenek kazandiren hazır paketlerdir.

- **Kurulu skill sayısı (root profil):** ~40 adet. Önemli olanlar:
  - `trio-emlak` — TrioPrime agent sistemi, bot, portföy, `.worktrees`, faz rollout.
  - `trio-image-pipeline` — TrioPrime işlem hattı (görsel).
  - `hermes-agent` — Hermes'i yapılandırmak, değiştirmek, sorun gidermek için.
  - `sahibinden-scraping`, `real-estate-scraping-analysis` — ilan analizi.
  - `telegram-bot-management`, `telegram-bot-verification` — Telegram bot işleri.
- **asistan profili skillleri:** Boş (kendi skill'i yok, root'takileri miras alabilir gibi görünüyor, doğrulanamadı).

### Yeni skill nasıl eklenir?
1. `skill_view(name='hermes-agent')` ile Hermes skill'inin talimatlarını oku.
2. Skill'i `skill_manage(action='create')` veya `patch` ile ekleyin/güncelleyin.
3. Değişikliği test edin (gerçek komut çalıştırın, sadece tahminlemeyin).

> 🔍 Doğrulanamadı: Skill eklemek için kesin adım adım komut seti (hermes-agent skill'i okunmalı).

---

## 6. Otomasyon

### Zamanlanmış görevler (cron)
Hermes'in arka planda çalıştırabileceği görevler var. Şu an sadece **öneri** düzeyinde, henüz aktifleştirilmemiş:

| # | Görev | Zamanlama | Durum |
|---|-------|-----------|-------|
| 1 | Günlük sabah özeti | Her gün 08:00 | `pending` (beklemede) |
| 2 | Önemli posta izleyicisi | Her 30 dakikada bir | `pending` |
| 3 | Haftalık gözden geçirme | Pazar 18:00 | `pending` |
| 4 | İşgünü başlangıç hatırlatması | Haftaiçi 09:00 | `pending` |

### Mevcut kontrol scriptleri
- `asistan_kontrol.sh` — iki Telegram botunun aktifliğini, `.env.local`'ı, scraping'i ve web sunumunu kontrol eder.
- `hermes_system_check.sh` — aynı kontrolleri günlük olarak çalıştırır, `/tmp/hermes_system_check.log` ye yazar.

### Nasıl kurulur?
Bir zamanlanmış görev istediğinizde, Hermes'e şöyle söyleyin:  
`"Her sabah 08:00'de bana TrioPrime ilgili kısa bir özet gönder, Telegram'dan."`  
Hermes bunu bir cron işi olarak ayarlayabilir. Aktifleştikten sonra, işi çalışmadığında size bildirim verir.

> 🔍 Doğrulanamadı: Cron görevlerinin aslında çalışıp çalışmadığı (sadece dosyalar var, crontab girişi doğrulanmadı).

---

## 7. Güvenlik ve Sınırlar

### Açık izinler (doğrulanmış)
- Dosya okuma/yazma (`file` toolset)
- Terminal komutu çalıştırma (`terminal`, local backend, `/home/rw/Projects`)
- Web tarama (`web`, `browser`)
- Telegram mesaj gönderme / alma
- Zamanlanmış görev (`cronjob`)

### Dikkat etmeniz gerekenler
- **`.env` dosyası:** Gizli anahtarları içerir, doğrudan okunamaz ve paylaşılmamalıdır.
- **Riskli işlemler:** Dosya silme, sistem ayar değişikliği, para ödeme işlemleri — bunlarda Hermes size onay sormalı veya sizi uyarmalı.
- **Token/şifre:** Asla sohbette şifre veya token paylaşmayın.
- **Doğrulama:** Hermes bir şeyden emin değilse `"doğrulanamadı"` der; buna güvenin, tahmin yapmayın.

### Sınırlar
- Yerel model (`lmstudio/openai-gpt-oss-20b`) çalışıp çalışmadığı bilinmiyor.
- E-posta izleyicisi henüz kurulmamış gibi görünüyor (`pending` öneri sadece).
- Bazı skill'ler asistan profilinde eksik olabilir.

---

## 8. Sık Yapılan Hatalar ve Sorun Giderme

| Sorun | Muhtemel neden | Çözüm |
|-------|---------------|-------|
| Hermes yanıt vermiyor | Ağ geçidi kapalı / Telegram bağlantısı kesildi | `gateway_state.json` dosyasını kontrol edin; `state` alanının `running` olduğundan emin olun. |
| Model cevabı İngilizce | Varsayılan model İngilizce yanıt verebiliyor | Komutunuzda `"Türkçe yanıtla"` belirtin. |
| Yerel model çalışmıyor | LM Studio açık değil / model yüklü değil | LM Studio'yı açın ve `openai/gpt-oss-20b` modelini yükleyin. |
| Dosya bulunamadı | Yanlış yol | Çalışma dizini `/home/rw/Projects`; mutlak yol kullanın. |
| Cron işi çalışmadı | Görev henüz etkinleştirilmedi | `suggestions.json`'daki `pending` öğesini etkinleştirin. |
| Skill yok | Skill kurulu değil | `skill_view(name='...')` ile kontrol edin, eksikse ekleyin. |

---

## 9. Hızlı Başlangıç — İlk Hafta

### Gün 1: Tanışma
- Hermes'e kendinizi ve abinizi tanıtın: `"Ben Gökcan, abim Ozancan Serhan. Trio Emlak / TrioPrime çalışıyoruz. Bölgemiz Ayvalık / Cunda / Altınova / Gömeç / İstanbul. Telefon: 0533 378 68 94."`
- Kanalı doğrulayın: Telegram'dan `@trioprimelab_bot` ile mesajlaşabilir misiniz diye sorun.

### Gün 2: Kurulumu inceleyin
- Bu kılavuzu bölüm 2'den okuyun. Model, araç, kanallar not alın.
- `IDEA.md`'yi (TrioPrime spesifikasyonu) Hermes ile özetlemesini isteyin.

### Gün 3: İlk iş örneği
- Bir ilan için içerik taslağı istedin: `"Cunda'da satılık daire için 3 saniyelik kanca ile Instagram hikayesi yaz."`
- Sonucu abinizle paylaşın, geri bildirim alın.

### Gün 4: Bellek ve skill
- Bir notunuzu hatırlatın: `"Sonraki sohbetimde Ayvalık odaklı olduğunu hatırla."`
- `trio-emlak` skill'ini deneyin: `"trio-emlak skill'i ne işe yarar?"`

### Gün 5: Otomasyon (isteğe bağlı)
- Bir zamanlanmış görev kurun: `"Pazar akşamları haftalık gözden geçirme raporu gönder."`
- `pending` durumunu `aktif` olduğundan emin olun.

### Gün 6: Güvenlik
- `.env` dosyasına asla dokunmayın.
- Riskli komutlardan önce Hermes'e onay sorun.

### Gün 7: Gözden geçirme
- İlk haftada ne yaptınız, ne öğrendiniz not alın.
- Bu kılavuzu eksiklikler için güncelleyin.

---

## 10. Kullanmadığımız Ama İşimize Yarayabilecek Özellikler

| Özellik | Ne işe yarar | Durum |
|---------|-------------|-------|
| MOA (Çoklu Ajan) | Birden fazla modelin cevabını birleştirir | ✅ Etkin (doğrulanmış) |
| Konuşma metni (TTS) | Metni sesli okur | ✅ Piper (doğrulanmış) |
| Metin-konuşma (STT) | Sesi metne döker | ✅ Türkçe (doğrulanmış) |
| Görsel üretim (`image_gen`) | Resim üretir | ⚠️ Tanımlı, kullanım doğrulanamadı |
| Video üretim (`video_gen`) | Video üretir | ⚠️ Tanımlı, kullanım doğrulanamadı |
| Bilgisayar kullanımı (`computer_use`) | Ekrandaki işlemleri yapabilir | ⚠️ Tanımlı, kullanım doğrulanamadı |
| E-posta izleyicisi | Gelen posta hakkında bildirim | ⚠️ `pending` öneri sadece |
| Web arama (`web`, `x_search`) | İnternette arama | ⚠️ Tanımlı, kullanım doğrulanamadı |
| Burada skill ekleme (`skills`) | Yeni yetenek kazanma | ✅ `skills` toolset var |

---

# Hızlı Başvuru Özeti — Tek Sayfa

| Konu | Ne yapmalıyız | Not |
|------|-------------|-----|
| Kimiz | Gökcan & Ozancan Serhan, Trio Emlak / TrioPrime | Telefon: `0533 378 68 94` |
| Bölge | Ayvalık / Cunda / Altınova / Gömeç / İstanbul | DAİMA bu bölge |
| Profil | `default` (Hermes masaüstü) | `asistan` varsa dikkatli kullan |
| Model | `google/gemini-2.5-flash-preview` (NVIDIA) | Yerel: `lmstudio/openai/gpt-oss-20b` |
| Kanal | Telegram DM — `@trioprimelab_bot` | Ozancan Serhan |
| Komut | Ne, hangi bölge, hangi biçim | Türkçe, sade |
| Bellek | `state.db`, `memories/`, sohbet geçmişi | Doğrulanamadı: ne kadar süre |
| Skill | ~40 kurulu, `trio-emlak` en önemli | Yeni ekle: `skill_view` → `skill_manage` |
| Otomasyon | 4 `pending` zamanlanmış görev | Hiçbiri aktif değil |
| Güvenlik | `.env`'e dokunma, riskli işlemde onay | `"doğrulanamadı"` ibaresine güven |
| Sorun | `gateway_state.json`, loglar | Terminal: local, `/home/rw/Projects` |

---

*Hazırlayan: Kriss — AI Operator / Back Office (TrioPrime)*  
*Bu kılavuz, Hermes kurulumunun gerçek dosya ve ayarlarından doğrulanmıştır. "doğrulanamadı" işaretli yerler, size emin olmanız gereken noktalardır.*
