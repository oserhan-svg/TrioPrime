#!/usr/bin/env python3
"""
PaddleOCR + YOLOv8 ile watermark/logo/plaka tespiti test scripti
"""
import os
import cv2
import json
import numpy as np
from pathlib import Path
from paddleocr import PaddleOCR
from ultralytics import YOLO

# Modelleri yükle
print("🔄 Modeller yükleniyor...")

# PaddleOCR - Yeni API
ocr = PaddleOCR(
    use_textline_orientation=True,  # use_angle_cls yerine
    lang='en',
    device='cpu',  # use_gpu yerine device
    show_log=False
)

# YOLOv8 - Pretrained COCO model
yolo = YOLO('yolov8n.pt')  # nano model - hızlı

print("✅ Modeller yüklendi")

def detect_with_yolo(image_path):
    """YOLOv8 ile nesne tespiti"""
    results = yolo(image_path, verbose=False)
    detections = []
    
    for r in results:
        boxes = r.boxes
        if boxes is not None:
            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].tolist()
                
                class_name = yolo.names[cls_id]
                
                detections.append({
                    "class": class_name,
                    "confidence": round(conf, 3),
                    "bbox": [round(x, 1) for x in xyxy]
                })
    
    return detections

def detect_text_with_paddle(image_path):
    """PaddleOCR ile metin/plaka tespiti"""
    try:
        result = ocr.ocr(image_path, cls=True)
        texts = []
        
        if result and result[0]:
            for line in result[0]:
                bbox = line[0]
                text = line[1][0]
                conf = line[1][1]
                
                # Plaka benzeri pattern
                if any(c.isdigit() for c in text) and any(c.isalpha() for c in text):
                    if len(text) >= 5:
                        texts.append({
                            "text": text,
                            "confidence": round(conf, 3),
                            "bbox": [[round(x) for x in pt] for pt in bbox],
                            "type": "potential_plate"
                        })
                    else:
                        texts.append({
                            "text": text,
                            "confidence": round(conf, 3),
                            "bbox": [[round(x) for x in pt] for pt in bbox],
                            "type": "text"
                        })
                    else:
                        texts.append({
                            "text": text,
                            "confidence": round(conf, 3),
                            "bbox": [[round(x) for x in pt] for pt in bbox],
                            "type": "text"
                        })
        
        return texts
    except Exception as e:
        return [{"error": str(e)}]

def detect_watermark_pattern(image_path):
    """Basit watermark pattern tespiti (DCT domain)"""
    try:
        img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
        if img is None:
            return {"error": "Image load failed"}
        
        # DCT transform
        dct = cv2.dct(np.float32(img) / 255.0)
        
        h, w = dct.shape
        high_freq = dct[h//2:, w//2:]
        
        mean_val = np.mean(np.abs(high_freq))
        std_val = np.std(high_freq)
        
        suspicious = std_val > 0.02 and mean_val > 0.01
        
        return {
            "suspicious": bool(suspicious),
            "mean_high_freq": round(float(mean_val), 4),
            "std_high_freq": round(float(std_val), 4)
        }
    except Exception as e:
        return {"error": str(e)}

def process_image(image_path):
    """Tek görseli işle"""
    print(f"\n🔍 İşleniyor: {Path(image_path).name}")
    
    yolo_results = detect_with_yolo(image_path)
    ocr_results = detect_text_with_paddle(image_path)
    wm_results = detect_watermark_pattern(image_path)
    
    return {
        "file": Path(image_path).name,
        "yolo_detections": yolo_results,
        "ocr_texts": ocr_results,
        "watermark_check": wm_results
    }

if __name__ == "__main__":
    from pathlib import Path
    import cv2
    
    INPUT_DIR = Path("/home/rw/code/trio/data/images_continuous/clean")
    images = list(INPUT_DIR.glob("*.jpg"))[:5]  # İlk 5 test
    
    print(f"🔍 {len(images)} görsel test ediliyor...\n")
    
    all_results = []
    
    for img_path in images:
        result = process_image(img_path)
        
        print(f"\n📸 {result['file']}:")
        
        if result['yolo_detections']:
            print(f"  🎯 YOLO: {len(result['yolo_detections'])} nesne")
            for d in result['yolo_detections']:
                print(f"    - {d['class']}: %{d['confidence']*100:.0f} @ {d['bbox']}")
        else:
            print("  🎯 YOLO: Nesne bulunamadı")
        
        if result['ocr_texts'] and 'error' not in result['ocr_texts'][0]:
            print(f"  📝 OCR: {len(result['ocr_texts'])} metin")
            for t in result['ocr_texts'][:3]:
                if 'error' not in t:
                    print(f"    - '{t['text']}' (%{t['confidence']*100:.0f}) [{t['type']}]")
        else:
            print("  📝 OCR: Metin bulunamadı")
        
        wm = result['watermark_check']
        if 'error' not in wm:
            print(f"  💧 Watermark: {'ŞÜPHELİ!' if wm['suspicious'] else 'Temiz'} (mean={wm['mean_high_freq']}, std={wm['std_high_freq']})")
        else:
            print(f"  💧 Watermark: Hata - {wm['error']}")

