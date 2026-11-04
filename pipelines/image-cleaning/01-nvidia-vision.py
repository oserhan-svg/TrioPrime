#!/usr/bin/env python3
"""
NVIDIA Vision API ile logo/plaka/watermark temizleme
"""
import os
import base64
import requests
from pathlib import Path

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
VISION_MODEL = "meta/llama-3.2-11b-vision-instruct"

INPUT_DIR = Path("/home/rw/Projects/scraped-images/raw")
OUTPUT_DIR = Path("/home/rw/Projects/scraped-images/cosmos3-cleaned")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def clean_image_with_vision(image_path):
    """Vision model ile görsel analizi ve temizlik talimatı"""
    base64_image = encode_image(image_path)
    
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": VISION_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Bu görselde logo, plaka, watermark varsa bunları tespit et ve temizleme için hangi alanların düzenlenmesi gerektiğini belirt. JSON formatında cevap ver: {\"has_logo\": bool, \"has_plate\": bool, \"has_watermark\": bool, \"regions\": [{\"x\": int, \"y\": int, \"w\": int, \"h\": int, \"type\": \"logo|plate|watermark\"}]}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ],
        "max_tokens": 500,
        "temperature": 0.3
    }
    
    response = requests.post(NVIDIA_API_URL, headers=headers, json=payload)
    return response.json()

def process_batch():
    images = list(INPUT_DIR.glob("*.jpg")) + list(INPUT_DIR.glob("*.png")) + list(INPUT_DIR.glob("*.jpeg"))
    print(f"📸 {len(images)} görsel işlenecek")
    
    for img in images:
        print(f"🔍 İşleniyor: {img.name}")
        try:
            result = clean_image_with_vision(img)
            print(f"   Sonuç: {result}")
            # Burada gerçek temizlik (inpainting) yapılacak
            # Şimdilik kopyala
            import shutil
            shutil.copy2(img, OUTPUT_DIR / img.name)
            print(f"   ✅ Kopyalandı: {img.name}")
        except Exception as e:
            print(f"   ❌ Hata: {e}")

if __name__ == "__main__":
    process_batch()
