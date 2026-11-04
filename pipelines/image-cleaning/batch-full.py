#!/usr/bin/env python3
"""
NVIDIA Vision API ile TÜM 990 dosya batch işleme
"""
import os
import base64
import requests
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
VISION_MODEL = "meta/llama-3.2-11b-vision-instruct"

INPUT_DIR = Path("/home/rw/code/trio/data/images_continuous/clean")
OUTPUT_DIR = Path("/home/rw/Projects/scraped-images/cosmos3-cleaned")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

image_files = list(INPUT_DIR.glob("*.jpg")) + list(INPUT_DIR.glob("*.png"))
print(f"📸 Toplam {len(image_files)} dosya işlenecek")

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def analyze_image(image_path):
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
                    {"type": "text", "text": "Bu görselde logo, plaka, watermark var mı? JSON: {\"has_logo\": bool, \"has_plate\": bool, \"has_watermark\": bool, \"regions\": [{\"x\": int, \"y\": int, \"w\": int, \"h\": int, \"type\": \"logo|plate|watermark\"}]}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ],
        "max_tokens": 500,
        "temperature": 0.3
    }
    
    try:
        response = requests.post(
            "https://integrate.api.nvidia.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {NVIDIA_API_KEY}", "Content-Type": "application/json"},
            json=payload,
            timeout=60
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def process_file(img_path):
    try:
        result = analyze_image(img_path)
        
        # Sonucu kaydet
        output_file = OUTPUT_DIR / f"{img_path.stem}_analysis.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        # Görseli kopyala
        import shutil
        shutil.copy2(img_path, OUTPUT_DIR / img_path.name)
        
        return {"file": img_path.name, "status": "done"}
    except Exception as e:
        return {"file": img_path.name, "status": "error", "error": str(e)}

if __name__ == "__main__":
    print(f"🚀 TAM BATCH BAŞLIYOR - {len(image_files)} dosya")
    start = time.time()
    
    # Paralel işleme (5 worker)
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(process_file, img): img for img in image_files}
        
        completed = 0
        for future in as_completed(futures):
            result = future.result()
            completed += 1
            if completed % 50 == 0:
                elapsed = time.time() - start
                rate = completed / elapsed * 60
                print(f"📊 {completed}/{len(image_files)} - {rate:.0f} dosya/dk")
    
    elapsed = time.time() - start
    print(f"\n✅ TAMAMLANDI - {len(image_files)} dosya - {elapsed:.0f}s ({elapsed/60:.1f}dk)")
    print(f"📁 Çıktı: {OUTPUT_DIR}")

