#!/bin/bash
# Ana Pipeline Orchestrator

set -e

echo "🔄 RESİM TEMİZLEME PIPELINE BAŞLATILIYOR"
echo "========================================="

# 1. Cosmos3 AI
echo ""
echo "📍 AŞAMA 1/3: Cosmos3 AI (Docker)"
./01-cosmos3-docker.sh

# 2. Photocraft
echo ""
echo "📍 AŞAMA 2/3: Photocraft Detaylı Temizlik"
./02-photocraft.sh

# 3. Subagent Review
echo ""
echo "📍 AŞAMA 3/3: Subagent Review"
python3 03-subagent-review.py

# 4. Telegram onayı için örnek gönder
echo ""
echo "📍 ÖRNEK GÖRSEL TELEGRAM'A GÖNDERİLİYOR"
# İlk onaylanmış görseli bul ve gönder
FIRST_APPROVED=$(ls /home/rw/Projects/scraped-images/approved/ | head -1)
if [ -n "$FIRST_APPROVED" ]; then
  hermes send -t telegram:-1004421698510 "📸 PIPELINE TAMAMLANDI - ÖRNEK GÖRSEL

✅ Cosmos3 AI (Logo/Plaka/Watermark)
✅ Photocraft (Detaylı Temizlik)  
✅ Subagent Review (Kalite Kontrol)

Dosya: $FIRST_APPROVED
Onay bekliyoruz... (Evet/Hayır)"
  
  # Görseli gönder
  hermes send -t telegram:-1004421698510 "MEDIA:/home/rw/Projects/scraped-images/approved/$FIRST_APPROVED"
else
  echo "⚠️ Henüz onaylanmış görsel yok"
fi

echo ""
echo "🎉 PIPELINE TAMAMLANDI!"
echo "Telegram grubundan onay bekliyoruz..."
