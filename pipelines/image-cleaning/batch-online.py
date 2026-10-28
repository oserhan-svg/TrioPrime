#!/usr/bin/env python3
"""
NVIDIA Online API - Rate limit yönetimli batch
"""
import os
import base64
import requests
import json
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
VISION_MODEL = "meta/llama-3.2-11b-vision-instruct"

INPUT_DIR = Path("/home/rw/code/trio/data/images_continuous/clean")
OUTPUT_DIR = Path("/home/rw/Projects/scraped-images/cosmos3-cleaned")
OUTPUT_DIR.mkdir(parents=True, exist_ok())

# Zaten işlenmiş dosyaları atla
processed = set(f.stem.replace("_analysis", "") for f in OUTPUT_DIR.glob("*_analysis.json"))
all_files = list(INPUT_DIR.glob("*.jpg")) + list(INPUT_DIR.glob("*.png"))
remaining = [f for f in all_files if f.stem not in processed]

print(f"📸 Toplam: {len(all_files)} | İşlenmiş: {len(processed)} | Kalan: {len(remaining)}")

# Rate limiter
class RateLimiter:
    def __init__(self, max_per_minute=30):
        self.max_per_minute = max_per_minute
        self.requests = []
    
    def wait(self):
        now = time.time()
        self.requests = [r for r in self.requests if now - r < 60]
        if len(self.requests) >= self.max_per_minute:
            sleep_time = 60 - (now - self.requests[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
        self.requests.append(time.time())

limiter = RateLimiter(max_per_minute=30)  # NVIDIA free tier: ~30/dk

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def analyze_image(image_path):
    limiter.wait()
    
    base64_image = encode_image(image_path)
    
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": VISION_MODEL,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": "Bu görselde logo, plaka, watermark var mı? JSON: {\"has_logo\": bool, \"has_plate\": bool, \"has_watermark\": bool, \"regions\": [{\"x\": int, \"y\": int, \"w\": int, \"h\": int, \"type\": \"logo|plate|watermark\"}]}"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        }],
        "max_tokens": 300,
        "temperature": 0.1
    }
    
    for attempt in range(3):
        try:
            response = requests.post(
                "https://integrate.api.nvidia.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {NVIDIA_API_KEY}", "Content-Type": "application/json"},
                json=payload,
                timeout=30
            )
            if response.status_code == 429:
                time.sleep(5 * (attempt + 1))
                continue
            return response.json()
        except Exception as e:
            if attempt == 2:
                return {"error": str(e)}
            time.sleep(2)
    return {"error": "Max retries"}

def process_file(img_path):
    try:
        result = analyze_image(img_path)
        output_file = OUTPUT_DIR / f"{img_path.stem}_analysis.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        import shutil
        shutil.copy2(img_path, OUTPUT_DIR / img_path.name)
        return {"file": img_path.name, "status": "done"}
    except Exception as e:
        return {"file": img_path.name, "status": "error", "error": str(e)}

if __name__ == "__main__":
    print(f"🚀 ONLINE BATCH BAŞLIYOR - {len(remaining)} dosya")
    start = time.time()
    
    # 3 worker (rate limit için)
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(process_file, img): img for img in remaining}
        
        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            if i % 25 == 0:
                elapsed = time.time() - start
                rate = i / elapsed * 60 if elapsed > 0 else 0
                print(f"📊 {i}/{len(remaining)} - {rate:.0f} dosya/dk - {elapsed/60:.1f}dk")
    
    print(f"\n✅ TAMAMLANDI - {len(remaining)} dosya - {(time.time()-start)/60:.1f}dk")

