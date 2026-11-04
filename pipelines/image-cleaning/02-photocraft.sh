#!/bin/bash
# Photocraft ile detaylı temizlik

INPUT_DIR="/home/rw/Projects/scraped-images/cosmos3-cleaned"
OUTPUT_DIR="/home/rw/Projects/scraped-images/photocraft-final"
mkdir -p "$OUTPUT_DIR"

echo "🎨 Photocraft detaylı temizlik başlatılıyor..."

for img in "$INPUT_DIR"/*; do
  if [[ -f "$img" ]]; then
    filename=$(basename "$img")
    echo "İşleniyor: $filename"
    
    # Photocraft CLI veya API çağrısı
    photocraft clean \
      --input "$img" \
      --output "$OUTPUT_DIR/$filename" \
      --remove-logo \
      --remove-plate \
      --remove-watermark \
      --quality high
  fi
done

echo "✅ Photocraft tamamlandı: $OUTPUT_DIR"
