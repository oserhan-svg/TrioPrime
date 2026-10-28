#!/usr/bin/env python3
"""
Async NVIDIA Vision API batch - aiohttp + semaphore + image resize
"""
import os, base64, json, time, shutil, sys, asyncio, aiohttp
from pathlib import Path
from PIL import Image
import io

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
VISION_MODEL = "meta/llama-3.2-11b-vision-instruct"
API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

INPUT_DIR = Path("/home/rw/code/trio/data/images_continuous/clean")
OUTPUT_DIR = Path("/home/rw/Projects/scraped-images/cosmos3-cleaned")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MAX_CONCURRENT = 5      # 5 concurrent requests
MAX_RETRIES = 3
READ_TIMEOUT = 120
CONNECT_TIMEOUT = 10
MAX_IMAGE_SIZE = 512    # Resize to max 512px

processed = set(f.stem.replace("_analysis", "") for f in OUTPUT_DIR.glob("*_analysis.json"))
all_files = list(INPUT_DIR.glob("*.jpg")) + list(INPUT_DIR.glob("*.png"))
remaining = [f for f in all_files if f.stem not in processed]

print(f"📸 Kalan: {len(remaining)} / Toplam: {len(all_files)}")
print(f"⚡ Workers: {MAX_CONCURRENT} | Resize: {MAX_IMAGE_SIZE}px")

semaphore = asyncio.Semaphore(MAX_CONCURRENT)

def resize_image(image_path, max_size=512):
    """Resize image to max dimension"""
    with Image.open(image_path) as img:
        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format='JPEG', quality=85)
        return base64.b64encode(buf.getvalue()).decode("utf-8")

async def process_one(session, img_path, pbar):
    async with semaphore:
        for attempt in range(3):
            try:
                b64 = resize_image(img_path, 512)
                
                payload = {
                    "model": VISION_MODEL,
                    "messages": [{"role": "user", "content": [
                        {"type": "text", "text": "Logo/plaka/watermark var mı? JSON: {\"has_logo\": bool, \"has_plate\": bool, \"has_watermark\": bool, \"regions\": [{\"x\": int, \"y\": int, \"w\": int, \"h\": int, \"type\": \"logo|plate|watermark\"}]}"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                    ]}],
                    "max_tokens": 200,
                    "temperature": 0.1
                }
                
                timeout = aiohttp.ClientTimeout(total=READ_TIMEOUT, connect=CONNECT_TIMEOUT)
                async with session.post(API_URL,
                    headers={"Authorization": f"Bearer {NVIDIA_API_KEY}", "Content-Type": "application/json"},
                    json=payload, timeout=timeout) as resp:
                    
                    if resp.status == 429:
                        await asyncio.sleep(10)
                        continue
                    result = await resp.json()
                    
                    out_file = OUTPUT_DIR / f"{img_path.stem}_analysis.json"
                    with open(out_file, 'w') as f:
                        json.dump(result, f)
                    shutil.copy2(img_path, OUTPUT_DIR / img_path.name)
                    
                    pbar[0] += 1
                    return True
                    
            except asyncio.TimeoutError:
                if attempt == 2:
                    print(f"❌ {img_path.name}: Timeout")
                    return False
                await asyncio.sleep(5 * (attempt + 1))
            except Exception as e:
                if attempt == 2:
                    print(f"❌ {img_path.name}: {e}")
                    return False
                await asyncio.sleep(2)
        return False

async def main():
    connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT, limit_per_host=MAX_CONCURRENT)
    timeout = aiohttp.ClientTimeout(total=None, connect=CONNECT_TIMEOUT, sock_read=READ_TIMEOUT)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = [process_one(session, img, [0]) for img in remaining]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    
    success = sum(1 for r in results if r is True)
    failed = sum(1 for r in results if r is False or isinstance(r, Exception))
    print(f"\n✅ TAMAMLANDI: ✓{success} ✗{failed}")

if __name__ == "__main__":
    import base64
    print(f"🚀 ASYNC BATCH - {len(remaining)} dosya | {MAX_CONCURRENT} workers")
    start = time.time()
    asyncio.run(main())
    elapsed = time.time() - start
    print(f"⏱️ Süre: {elapsed/60:.1f}dk | Hız: {len(remaining)/elapsed*60:.0f} dosya/dk")

