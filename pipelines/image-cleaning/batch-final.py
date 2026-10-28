#!/usr/bin/env python3
import os, base64, requests, json, time, shutil, sys
from pathlib import Path

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
VISION_MODEL = "meta/llama-3.2-11b-vision-instruct"

INPUT_DIR = Path("/home/rw/code/trio/data/images_continuous/clean")
OUTPUT_DIR = Path("/home/rw/Projects/scraped-images/cosmos3-cleaned")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

processed = set(f.stem.replace("_analysis", "") for f in OUTPUT_DIR.glob("*_analysis.json"))
all_files = list(INPUT_DIR.glob("*.jpg")) + list(INPUT_DIR.glob("*.png"))
remaining = [f for f in all_files if f.stem not in processed]

print(f"📸 Toplam: {len(all_files)} | İşlenmiş: {len(processed)} | Kalan: {len(remaining)}")
print("=" * 60)

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def process_one(img_path, max_retries=3):
    for attempt in range(max_retries):
        try:
            b64 = encode_image(img_path)
            r = requests.post(
                "https://integrate.api.nvidia.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {NVIDIA_API_KEY}", "Content-Type": "application/json"},
                json={"model": VISION_MODEL, "messages": [{"role": "user", "content": [
                    {"type": "text", "text": "Logo/plaka/watermark var mı? JSON: {\"has_logo\": bool, \"has_plate\": bool, \"has_watermark\": bool, \"regions\": [{\"x\": int, \"y\": int, \"w\": int, \"h\": int, \"type\": \"logo|plate|watermark\"}]}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                ]}], "max_tokens": 300, "temperature": 0.1},
                timeout=(10, 60)  # connect timeout 10s, read timeout 60s
            )
            if r.status_code == 429:
                time.sleep(10)
                continue
            result = r.json()
            
            out_file = OUTPUT_DIR / f"{img_path.stem}_analysis.json"
            with open(out_file, 'w') as f:
                json.dump(result, f)
            shutil.copy2(img_path, OUTPUT_DIR / img_path.name)
            return True
        except requests.exceptions.Timeout:
            if attempt == 2:
                print(f"❌ {img_path.name}: Timeout after {max_retries} retries")
                return False
            time.sleep(5 * (attempt + 1))
        except Exception as e:
            print(f"❌ {img_path.name}: {e}")
            return False
    return False

def progress_bar(current, total, start_time):
    percent = current / total * 100
    bar_len = 40
    filled = int(40 * current / total)
    bar = "█" * filled + "░" * (40 - filled)
    elapsed = time.time() - start_time
    rate = current / elapsed * 60 if elapsed > 0 else 0
    eta = (total - current) / (rate / 60) if rate > 0 else 0
    sys.stdout.write(f"\r[{'█' * int(40*current/total)}{'░' * (40-int(40*current/total))}] {current}/{total} ({percent:.1f}%) | {current/elapsed*60:.0f}/dk | ETA: {eta:.0f}dk")
    sys.stdout.flush()

if __name__ == "__main__":
    import sys
    print(f"📸 Toplam: {len(all_files)} | İşlenmiş: {len(processed)} | Kalan: {len(remaining)}")
    print("=" * 60)
    start = time.time()
    
    success = 0
    failed = 0
    
    for i, img in enumerate(remaining, 1):
        if process_one(img):
            success += 1
        else:
            failed += 1
        
        percent = i / len(remaining) * 100
        elapsed = time.time() - start
        rate = i / elapsed * 60 if elapsed > 0 else 0
        eta = (len(remaining) - i) / (rate / 60) if rate > 0 else 0
        sys.stdout.write(f"\r[{'█' * int(40*i/len(remaining))}{'░' * (40-int(40*i/len(remaining)))}] {i}/{len(remaining)} ({i/len(remaining)*100:.1f}%) | {rate:.0f}/dk | ETA: {eta:.0f}dk | ✓{success} ✗{failed}")
        sys.stdout.flush()
        
        # Her 20'de bir küçük bekle
        if i % 20 == 0:
            time.sleep(1)
    
    elapsed = time.time() - start
    print(f"\n\n✅ TAMAMLANDI!")
    print(f"   ✓ Başarılı: {success}")
    print(f"   ✗ Başarısız: {failed}")
    print(f"   ⏱️ Süre: {elapsed/60:.1f} dakika")
    print(f"   🚀 Hız: {success/elapsed*60:.0f} dosya/dk")

