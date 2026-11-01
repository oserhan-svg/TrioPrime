# Cosmos3 Pipeline — Quick Reference Card (Turkish)

## 🚀 En Hızlı Başlangıç (2 dakika)

```bash
cd /home/rw/Projects/cosmos3-pipeline

# 1. API Key ayarla
cp .env.example .env
nano .env  # NVIDIA_API_KEY satırını düzenle

# 2. Container'ları başlat
docker-compose up -d --build

# 3. Test et
mkdir -p data/input output logs
cp /path/to/sample.jpg data/input/
docker-compose exec quality-gate python scripts/quality_gate_orchestrator.py
```

---

## 📊 Pipeline Durumunu Kontrol Et

```bash
# Logları izle
docker-compose logs -f

# Container durumu
docker-compose ps

# Redis queue kontrolü (opsiyonel)
docker-compose exec redis redis-cli LLEN "pipeline:queue"
```

---

## 🔍 Sample Validation Testi

```bash
# Tek bir fotoğraf test et
cp /path/to/test.jpg data/input/
docker-compose exec quality-gate python scripts/quality_gate_orchestrator.py

# Sonuçları kontrol et
cat logs/*.log | grep -A 20 "Validation Result"
```

---

## 🧪 Fast Pipeline (Cosmos3 olmadan)

```bash
export NVIDIA_API_KEY="your_key_here"
cd /home/rw/Projects/cosmos3-pipeline/scripts
python fast_pipeline.py
```

**Kullanım:** Hızlı test, batch processing öncesi ön kontrol.

---

## 📁 Dosya Yapısı (Özet)

| Dosya | Açıklama |
|-------|----------|
| `docker-compose.yml` | Tüm servisleri tanımlar |
| `.env.example` | NVIDIA API key şablonu |
| `scripts/quality_gate_orchestrator.py` | Full pipeline orchestrator |
| `scripts/fast_pipeline.py` | Hızlı test (Llama-only) |
| `agents/suggestion/agent.py` | Suggestion logic |
| `agents/review/agent.py` | Review decision logic |

---

## 🎯 Karar Matrisi (Quick View)

| Cosmos3 Score | Issues | Decision |
|---------------|--------|----------|
| ≥ 70 + no screenshot | minor | ✅ APPROVE |
| < 50 or screenshot | any | ❌ REJECT |
| 50-70 with issues | medium | 🔄 RETRY |

---

## 🔧 Sık Kullanılan Komutlar

```bash
# Container'ları yeniden başlat
docker-compose restart quality-gate

# Logları temizle
docker-compose logs > /tmp/cosmos3_logs_$(date +%Y%m%d).log

# Redis queue sıfırla (opsiyonel)
docker-compose exec redis redis-cli FLUSHALL

# Container'ları durdur
docker-compose down
```

---

## 📈 Performance Monitoring

```bash
# GPU kullanımı
nvidia-smi dmon -s um,us,mg,pq

# API response time (test için)
time curl -X POST https://integrate.api.nvidia.com/v1/chat/completions \
  -H "Authorization: Bearer $NVIDIA_API_KEY" \
  -d '{"model":"meta/llama-3.2-90b-vision-instruct","messages":[...]}

# Redis queue depth
docker-compose exec redis redis-cli LLEN "pipeline:queue"
```

---

## 🐛 Troubleshooting (Hızlı Çözümler)

### "NVIDIA_API_KEY not set"
```bash
cat .env | grep NVIDIA_API_KEY
export NVIDIA_API_KEY=$(cat .env | grep NVIDIA_API_KEY | cut -d= -f2)
```

### "Container won't start"
```bash
docker-compose down
rm -rf data/ output/ logs/  # Temizle
docker-compose up -d --build
```

### "Slow response times"
```bash
# GPU memory kontrolü
nvidia-smi --query-gpu=memory.used,memory.total --format=csv

# API rate limit kontrolü
curl -v https://integrate.api.nvidia.com/v1/health
```

---

## 📊 Batch Processing (Bulk Upload)

```bash
# Bulk upload script (opsiyonel)
cat > /tmp/bulk_upload.sh << 'EOF'
#!/bin/bash
cd /home/rw/Projects/cosmos3-pipeline/data/input
for f in *.jpg; do
  cp "$f" "output/$f"  # Basit kopyalama test için
done
echo "Bulk upload complete: $(ls output/*.jpg | wc -l) images"
EOF

chmod +x /tmp/bulk_upload.sh
/tmp/bulk_upload.sh
```

---

## 🎯 Next Steps (Öneriler)

1. **Sample Validation** → Batch Processing pipeline'ını test et
2. **Photocraft Integration** → Content-aware inpainting ekle
3. **Redis Queue Optimization** → Bulk processing için optimize et
4. **Monitoring Dashboard** → Grafana + Prometheus ekle

---

## 📚 Daha Fazla Bilgi

- [README.md](../README.md) — Detaylı kılavuz
- [ARCHITECTURE.md](../ARCHITECTURE.md) — Mimari diyagramları
- [scripts/quality_gate_orchestrator.py](../scripts/quality_gate_orchestrator.py) — Full orchestrator code

---

## 📍 Session Checkpoint

**Last Modified:** Sunday, November 01, 2026 (+03)  
**Session ID:** `20261101_075332_xxxx`  

### ✅ Completed
- Git commit — 9 files (`0df683f5`)
- Second Brain / Vault — PARA structure ready
- HERMES_KULLANMA_KILAVUZU — 310-line guide
- **Cosmos3 Pipeline** — Docker Compose + Llama 3.2 Vision + Photocraft

### 🔴 Pending: trio-app Live Deployment
See `telegram_msg.txt` for 3-step checklist.

---

**Created:** Sunday, November 01, 2026 (+03)  
**Last Modified:** Session ID `20261101_075332_xxxx`  
**Next Session Start:** Read this file to resume.