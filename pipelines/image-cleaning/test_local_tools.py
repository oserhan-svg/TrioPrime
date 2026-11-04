#!/usr/bin/env python3
import cv2
import json
import numpy as np
from pathlib import Path
from paddleocr import PaddleOCR
from ultralytics import YOLO

print("🔄 Modeller yükleniyor...")
ocr = PaddleOCR(use_textline_orientation=True, lang='en', device='cpu', show_log=False)
yolo = YOLO('yolov8n.pt')
print("✅ Modeller yüklendi")

def detect_yolo(img_path):
    results = yolo(img_path, verbose=False)
    detections = []
    for r in results:
        boxes = r.boxes
        if boxes is not None:
            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].tolist()
                class_name = yolo.names[cls_id]
                detections.append({"class": class_name, "confidence": round(conf,3), "bbox": [round(x,1) for x in xyxy]})
    return detections

def detect_ocr(img_path):
    try:
        result = ocr.ocr(img_path, cls=True)
        texts = []
        if result and result[0]:
            for line in result[0]:
                bbox = line[0]
                text = line[1][0]
                conf = line[1][1]
                texts.append({"text": text, "confidence": round(conf,3), "bbox": [[round(x) for x in pt] for pt in bbox], "type": "text"})
        return texts
    except Exception as e:
        return [{"error": str(e)}]

def detect_watermark(img_path):
    try:
        img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
        if img is None: return {"error": "load failed"}
        dct = cv2.dct(np.float32(img)/255.0)
        h,w = dct.shape
        high = dct[h//2:, w//2:]
        mean_val = float(np.mean(np.abs(high)))
        std_val = float(np.std(high))
        suspicious = std_val > 0.02 and mean_val > 0.01
        return {"suspicious": bool(suspicious), "mean": round(mean_val,4), "std": round(std_val,4)}
    except Exception as e:
        return {"error": str(e)}

import cv2
import json
from pathlib import Path
import sys

INPUT_DIR = Path("/home/rw/code/trio/data/images_continuous/clean")
images = list(INPUT_DIR.glob("*.jpg"))[:5]

print(f"🔍 {len(images)} görsel test ediliyor...")

for img_path in images:
    print(f"\n📸 {img_path.name}:")
    
    # YOLO
    yolo_res = []
    results = yolo(img_path, verbose=False)
    for r in results:
        if r.boxes is not None:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].tolist()
                cls_name = yolo.names[int(box.cls[0])]
                print(f"  🎯 YOLO: {cls_name} %{float(box.conf[0])*100:.0f} @ {[round(x,1) for x in box.xyxy[0].tolist()]}")
    
    # OCR
    try:
        ocr = PaddleOCR(use_textline_orientation=True, lang='en', device='cpu', show_log=False)
        result = ocr.ocr(str(img_path), cls=True)
        if result and result[0]:
            for line in result[0]:
                text = line[1][0]
                conf = line[1][1]
                print(f"  📝 OCR: '{text}' (%{conf*100:.0f})")
                if len(text) >= 5 and any(c.isdigit() for c in text) and any(c.isalpha() for c in text):
                    print(f"    → Potential PLATE!")
    except Exception as e:
        print(f"  📝 OCR Error: {e}")
    
    # Watermark check
    img = cv2.imread(str(Path("/home/rw/code/trio/data/images_continuous/clean") / img_path.name), cv2.IMREAD_GRAYSCALE)
    if img is not None:
        dct = cv2.dct(np.float32(img)/255.0)
        h,w = dct.shape
        high = dct[h//2:, w//2:]
        mean_val = float(np.mean(np.abs(high)))
        std_val = float(np.std(high))
        suspicious = std_val > 0.02 and mean_val > 0.01
        print(f"  💧 Watermark: {'ŞÜPHELİ!' if suspicious else 'Temiz'} (mean={mean_val:.4f}, std={std_val:.4f})")

print("\n✅ Test tamamlandı")
