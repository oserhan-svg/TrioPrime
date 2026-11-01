#!/bin/bash
# Cosmos3 Pipeline — Quick Start Guide (Turkish)

set -e

echo "🚀 COSMOS3 PIPELINE — HIZLI BAŞLANGIÇ"
echo "======================================"
echo ""

# 1. NVIDIA API Key Ayarla
echo "1️⃣  NVIDIA API Key Ayarlama..."
ENV_FILE="cosmos3-pipeline/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo "   .env dosyası yok, şablonu kopyalıyoruz..."
    cp cosmos3-pipeline/.env.example cosmos3-pipeline/.env
fi

echo ""
echo "   📝 Şimdi .env dosyasını düzenle:"
echo "      nano $ENV_FILE"
echo ""
echo "   🔑 NVIDIA_API_KEY satırına kendi API key'ini ekle:"
echo "      NVIDIA_API_KEY=your_nvidia_api_key_here"
echo ""

# 2. Data Klasörleri Oluştur
echo "2️⃣  Data Klasörlerini Oluşturma..."
mkdir -p cosmos3-pipeline/data/input
mkdir -p cosmos3-pipeline/output
mkdir -p cosmos3-pipeline/logs
echo "   ✅ Klasörler hazır:"
ls -la cosmos3-pipeline/data/
echo ""

# 3. Docker Compose ile Başlat
echo "3️⃣  Docker Container'ları Başlatma..."
cd /home/rw/Projects/cosmos3-pipeline
docker-compose up -d --build
echo "   ✅ Container'lar başlatıldı!"
echo ""

# 4. Logları İncele
echo "4️⃣  İlk Logları İnceleme..."
sleep 5
docker-compose logs cosmos3-validator | tail -20
echo ""

# 5. Test Fotoğrafı Ekle (Opsiyonel)
echo "5️⃣  Test İçin Örnek Fotoğraf Ekleme..."
echo "   📸 Örnek fotoğraf ekle:"
echo "      cp /path/to/sample.jpg cosmos3-pipeline/data/input/"
echo ""

# 6. Sample Validation Çalıştır (Opsiyonel)
echo "6️⃣  Sample Validation Testi (Opsiyonel)..."
echo "   🧪 Orchestrator'u çalıştır:"
echo "      docker-compose exec quality-gate python scripts/quality_gate_orchestrator.py"
echo ""

# 7. Fast Pipeline ile Hızlı Test (Opsiyonel)
echo "7️⃣  Fast Pipeline ile Hızlı Test (Opsiyonel)..."
export NVIDIA_API_KEY="your_nvidia_api_key_here"
cd /home/rw/Projects/cosmos3-pipeline/scripts
python fast_pipeline.py || echo "   ⚠️  API key kontrol et!"
echo ""

# 8. Docker Compose Durdur (İstendiğinde)
echo "8️⃣  Durdurma Komutu:"
echo "      docker-compose down"
echo ""

echo "======================================"
echo "✅ COSMOS3 PIPELINE HAZIR!"
echo "======================================"
echo ""
echo "📚 Daha fazla bilgi için README.md'yi oku:"
cat /home/rw/Projects/cosmos3-pipeline/README.md | head -50
echo ""
