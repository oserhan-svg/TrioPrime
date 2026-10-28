#!/bin/bash
# Photocraft CLI ile batch detaylı temizlik

INPUT_DIR="/home/rw/Projects/scraped-images/cosmos3-cleaned"
OUTPUT_DIR="/home/rw/Projects/scraped-images/photocraft-final"
mkdir -p "$OUTPUT_DIR"

# Photocraft CLI yolu
PHOTOCRAFT_CLI="/home/rw/photocraft/target/release/photocraft-cli"

echo "🎨 Photocraft batch başlıyor..."
echo "Input: $INPUT_DIR"
echo "Output: $OUTPUT_DIR"

# Batch işlem - photocraft-cli batch komutu kullan
# Actions JSON oluştur (temizlik işlemleri)

cat > /tmp/clean_actions.json << 'ACTIONS_EOF'
{
  "actions": [
    {"command": "denoise", "params": {"strength": 0.3}},
    {"command": "sharpen", "params": {"amount": 0.2}},
    {"command": "auto_levels", "params": {}},
    {"command": "remove_watermark", "params": {"strength": 0.8}},
    {"command": "inpaint", "params": {"mode": "content_aware"}}
  ]
}
ACTIONS_EOF

# Batch işle
$PHOTOCRAFT_CLI batch \
  --actions /tmp/clean_actions.json \
  --in "$INPUT_DIR" \
  --out "$OUTPUT_DIR" \
  --format jpg \
  --quality 95

echo "✅ Photocraft batch tamamlandı: $OUTPUT_DIR"
