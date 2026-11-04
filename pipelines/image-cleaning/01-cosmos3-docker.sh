#!/bin/bash
# Cosmos3 AI ile batch logo/plaka/watermark temizleme

INPUT_DIR="/home/rw/Projects/scraped-images/raw"
OUTPUT_DIR="/home/rw/Projects/scraped-images/cosmos3-cleaned"
mkdir -p "$OUTPUT_DIR"

echo "🚀 Cosmos3 AI Docker başlatılıyor..."

docker run --rm \
  -v "$INPUT_DIR:/input" \
  -v "$OUTPUT_DIR:/output" \
  -e COSMOS3_API_KEY="$COSMOS3_API_KEY" \
  -e MODE="batch_clean" \
  -e TARGETS="logo,plate,watermark" \
  cosmos3/ai:latest

echo "✅ Cosmos3 temizleme tamamlandı: $OUTPUT_DIR"
