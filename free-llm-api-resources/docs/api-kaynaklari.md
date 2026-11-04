# 📚 FREE LLM API RESOURCES - KNOWLEDGE BASE

> Bu repoda ücretsiz LLM API kaynakları, kullanım kılavuzları ve integrasyon örnekleri bulunur.

---

## 📁 1. Klasör Yapısı

```text
/free-llm-api-resources/
├── README.md
├── docs/
│   ├── api-kaynaklari.md
│   ├── integration-guide.md
│   └── usage-examples.md
├── repo/
│   ├── src/
│   │   ├── 1-second-of-silence.mp3
│   │   ├── README_template.md
│   │   ├── data.py
│   │   ├── pull_available_models.py
│   │   └── requirements.txt
│   ├── .git/
│   ├── .github/
│   └── .gitignore
```

---

## 📁 2. README.md - Ana Dokümantasyon

### Proje Adı

**Free LLM API Resources**

### Açıklama

Ücretsiz LLM (Large Language Model) API kaynaklarını toplayan ve yöneten bir repoda.
LM Studio, Hugging Face, OpenRouter gibi platformlardan ücretsiz API erişimi sağlar.

### Özellikler

- ✅ Ücretsiz LLM API kaynakları koleksiyonu
- ✅ LM Studio yerel kurulumu için örnekler
- ✅ OpenRouter geçici blok durumunda alternatif çözüm
- ✅ Model yönetimi ve çekme scriptleri
- ✅ Tüm işlemler yerel ortamda

### Kullanım Alanları

- 🎯 Lokal AI işleri için modeller
- 🎯 Ethik hacking ve güvenlik testleri
- 🎯 Öğrenme ve araştırma
- 🎯 Prototip geliştirme

---

## 📁 3. docs/api-kaynaklari.md

### Mevcut API Kaynakları

| API | Tip | Durum | Erişim |
|-----|------|-------|--------|
| **LM Studio** | Yerel | ✅ Aktif | `localhost:1234` |
| OpenRouter | Bulut | ⏸️ Geçici blok | API Key gerektirir |
| Hugging Face | Bulut | ✅ Aktif | Token gerekir |

### LM Studio Konfigürasyonu

```yaml
# .continue/config.yaml örneği
provider: openai
base_url: http://localhost:1234/v1
model: qwen/qwen3.5-397b-a17b
api_mode: chat_completions
```

### Mevcut Modeller

| Model | Boyut | Kullanım | Status |
|-------|-------|----------|--------|
| **openhermes-2.5** | 4.14 GB | Chat completions | ✅ Aktif |
| qwen3.5-9b | 6.55 GB | Yerel işler | ✅ Aktif |
| granite-4-h | 4.23 GB | Hazır modeller | ✅ Aktif |

---

## 📁 4. docs/integration-guide.md

### LM Studio Entegrasyonu

#### Qadımcı Kurulumu

1. **LM Studio'yu kurun:**
   ```bash
   # Linux (CachyOS)
   sudo pacman -S lmstudio
   ```

2. **Model yükleyin:**
   - `openhermes-2.5-strix-philosophy-mistral-7b-lora` (4.14 GB)
   - `qwen3.5-9b-uncensored-hauhaus-aggressive` (6.55 GB)
   - `ibm/granite-4-h-tiny` (4.23 GB)

3. **Port ayarlayın:** `localhost:1234`

4. **Auth kontrolü:**
   - `Require Authentication`: OFF
   - `Custom Headers`: Boş

#### VS Code + Continue Entegrasyonu

1. **VS Code Kurulumu:**
   ```bash
   # Örnek kurulum komutu
   sudo pacman -S code
   ```

2. **Continue Extension Kurulumu:**
   - VS Code Extensions panelinden "Continue" arayın
   - `v2.0.0` sürümünü deneyin

3. **Konfigürasyon:**
   ```yaml
   # ~/.continue/config.yaml
   model: qwen/qwen3.5-397b-a17b
   provider: openrouter
   base_url: http://localhost:1234/v1
   api_mode: chat_completions
   ```

### Hata Çözümü

#### 401 Unauthorized

**Neden:** LM Studio auth açık

**Çözüm:**
1. LM Studio'u açın
2. `Require Authentication` seçeneğini OFF yapın
3. Port `localhost:1234` kontrolü

#### Connection Refused

**Neden:** Port tükenmiş veya blok

**Çözüm:** 
- `lsof -i :1234` ile kontrol
- Uygulamayı yeniden başlatın

---

## 📁 5. docs/usage-examples.md

### Başlangıç Örneği

```python
import requests

# LM Studio'ya istek gönder
url = "http://localhost:1234/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": ""  # Auth açıksa gerekiyor
}

payload = {
    "model": "openhermes-2.5",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Merhaba, nasıl yardımcı olabilirim?"}
    ],
    "temperature": 0.7,
    "max_tokens": 150
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

### Free API Kaynakları Kullanımı

```bash
# LM Studio model listesini kontrol et
curl http://localhost:1234/v1/models

# Eğer auth açıksa token ile
curl -H "Authorization: Bearer sk_xxx" \
     http://localhost:1234/v1/models
```

---

## 📁 6. repo/src/ Klasörü

### src/1-second-of-silence.mp3

Birkaç saniyelik sessizlik içerikli örnek audio dosyası (test amaçlı).

### src/README_template.md

Bir README.md şablonu. Her projeye kendi README.md oluşturulması önerilir.

### src/data.py

Mevcut model verilerini yöneten örnek script.

### src/pull_available_models.py

LM Studio'dan mevcut modelleri çeken script.

### src/requirements.txt

Gereksinim dosyası (kernel modülleri listesi).

---

## 📁 7. Kullanım Talimatları

### 1. LM Studio Kurulumu

```bash
# CachyOS (Arch-based)
sudo pacman -S lmstudio

# Debian/Ubuntu
wget https://lmstudio.ai/linux-amd64.tar.gz
tar -xzf linux-amd64.tar.gz
sudo mv lmstudio /usr/local/bin/
```

### 2. Model Yükleme

- LM Studio'tan → "Download" kısmına gidin
- Model adını seçin ve indirin
- `models/` dizinine yükleyin

### 3. Nötr Entegrasyon

- VS Code + Continue extension kurun
- Config dosyasını yapılandırın
- Test isteği gönderin

---

## 📁 8. GELİŞİM KURUMU

### Q1 2027

- [ ] LM Studio model listesi güncelleme
- [ ] docs/api-kaynaklari.md tamamlama
- [ ] docs/integration-guide.md detaylandırma
- [ ] repo/src/ pull_available_models.py işlevselliği ekle

### Q2 2027

- [ ] Free LLM API kaynakları ekleme
- [ ] Integration örnekleri ekle
- [ ] .github/workflows için CI/CD dokümanları ekle

---

## 📁 9. GÜNCELLEME TERCİHİ

| Tarih | Geliştirici | Değişiklik |
|------|-------------|------------|
| 20 Ekim 2026 | Gökcan Serhan | Repo klonlandı ve structur eklendi |

---

## 📁 10. SONUÇ

Bu repo, ücretsiz LLM API kaynaklarını toplayan ve yöneten merkezi bir kayıttır.
LM Studio entegrasyonu, model yönetimi ve dokümantasyon çalışmaları devam etmektedir.

**Son Güncelleme:** 20 Ekim 2026
**Durum:** PROTOTİP
