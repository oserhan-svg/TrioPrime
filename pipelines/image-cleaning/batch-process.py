#!/usr/bin/env python3
"""
NVIDIA Vision API ile batch logo/plaka/watermark temizleme
"""
import os
import base64
import requests
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
VISION_MODEL = "meta/llama-3.2-11b-vision-instruct"

INPUT_DIR = Path("/home/rw/code/trio/data/images_continuous/clean")
OUTPUT_DIR = Path("/home/rw/Projects/scraped-images/cosmos3-cleaned")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# İşlenecek dosyaları al (ilk 10 test için, sonra 990)
image_files = list(INPUT_DIR.glob("*.jpg")) + list(INPUT_DIR.glob("*.png"))
print(f"📸 Toplam {len(image_files)} dosya bulundu")

# Test için ilk 5 dosya
test_files = image_files[:5]
print(f"🧪 Test: İlk {len(test_files)} dosya işlenecek")

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def analyze_image(image_path):
    """Vision model ile görsel analizi"""
    base64_image = encode_image(image_path)
    
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "meta/llama-3.2-11b-vision-instruct",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Bu görselde logo, plaka, watermark var mı? Varsa konumlarını ve türlerini JSON ver: {\"has_logo\": bool, \"has_plate\": bool, \"has_watermark\": bool, \"regions\": [{\"x\": int, \"y\": int, \"w\": int, \"h\": int, \"type\": \"logo|plate|watermark\"}]}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_image(image_path)}"}}
                ]
            }
        ],
        "max_tokens": 500,
        "temperature": 0.3
    }
    
    try:
        response = requests.post(
            "https://integrate.api.nvidia.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {os.getenv('NVIDIA_API_KEY')}", "Content-Type": "application/json"},
            json=payload,
            timeout=60
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def process_file(img_path):
    print(f"🔍 İşleniyor: {img_path.name}")
    result = analyze_image(img_path)
    
    # Sonucu kaydet
    output_file = OUTPUT_DIR / f"{img_path.stem}_analysis.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    # Görseli kopyala (şimdilik)
    import shutil
    shutil.copy2(img_path, OUTPUT_DIR / img_path.name)
    
    return {"file": img_path.name, "status": "done", "result": result}

if __name__ == "__main__":
    print(f"🚀 Batch işleme başlıyor...")
    start = time.time()
    
    for img in test_files:
        result = process_file(img)
        print(f"   ✅ {result['file']}")
    
    print(f"\n✅ Test tamamlandı - Süre: {time.time() - start:.1f}s")
    print(f"📁 Çıktı: {OUTPUT_DIR}")
