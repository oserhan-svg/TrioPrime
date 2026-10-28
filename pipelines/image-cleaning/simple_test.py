#!/usr/bin/env python3
"""
YOLOv8 + OpenCV ile watermark/logo/plaka tespiti - Basit ve çalışan versiyon
"""
import cv2
import numpy as np
import json
from pathlib import Path
from ultralytics import YOLO

print("🔄 YOLOv8 yükleniyor...")
yolo = YOLO('yolov8n.pt')  # nano model
print("✅ YOLOv8 yüklendi")

def detect_yolo(img_path):
    """YOLOv8 ile nesne tespiti"""
    results = yolo(img_path, verbose=False)
    detections = []
    for r in results:
        if r.boxes is not None:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].tolist()
                cls_name = yolo.names[int(box.cls[0])]
                if conf > 0.3:  # Minimum confidence
                    print(f"  🎯 YOLO: {cls_name} %{conf*100:.0f} @ {[round(x,1) for x in xyxy]}")

def detect_watermark_dct(img_path):
    """DCT domain watermark tespiti"""
    try:
        img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
        if img is None:
            return {"error": "load failed"}
        
        # Resize for speed
        h, w = img.shape
        if max(h, w) > 1024:
            scale = 1024 / max(h, w)
            img = cv2.resize(img, (int(w*scale), int(h*scale)))
        
        # DCT
        dct = cv2.dct(np.float32(img) / 255.0)
        h, w = dct.shape
        high_freq = dct[h//2:, w//2:]
        
        mean_val = float(np.mean(np.abs(high_freq)))
        std_val = float(np.std(high_freq))
        suspicious = std_val > 0.02 and mean_val > 0.01
        
        return {
            "suspicious": bool(suspicious),
            "mean": round(float(np.mean(np.abs(high_freq))), 4),
            "std": round(float(np.std(high_freq)), 4)
        }
    except Exception as e:
        return {"error": str(e)}

def detect_text_regions(img_path):
    """Basit metin bölgesi tespiti (MSER + kontur)"""
    try:
        img = cv2.imread(str(img_path))
        if img is None:
            return {"error": "load failed"}
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # MSER detector
        mser = cv2.MSER_create()
        regions, _ = mser.detectRegions(gray)
        
        text_regions = []
        for region in regions:
            x, y, w, h = cv2.boundingRect(region.reshape(-1, 1, 2))
            area = w * h
            aspect = w / h if h > 0 else 0
            
            # Metin benzeri bölgeler: belirli boyut ve aspect ratio
            if 20 < area < 5000 and 0.2 < aspect < 10:
                text_regions.append({
                    "bbox": [int(x), int(y), int(w), int(h)],
                    "area": area,
                    "aspect": round(aspect, 2)
                })
        
        return {"regions_found": len(text_regions), "regions": text_regions[:10]}
    except Exception as e:
        return {"error": str(e)}

def detect_edges_patterns(img_path):
    """Kenar desenleri - watermark için"""
    try:
        img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
        if img is None:
            return {"error": "load failed"}
        
        # Sobel edges
        sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
        edges = np.sqrt(sobelx**2 + sobely**2)
        
        # Yüksek kenar yoğunluğu = olası watermark/text
        edge_density = np.mean(edges > 50)
        
        # Laplacian variance (blur/sharpness)
        lap_var = cv2.Laplacian(img, cv2.CV_64F).var()
        
        return {
            "edge_density": round(float(edge_density), 4),
            "laplacian_var": round(float(lap_var), 2),
            "sharp": lap_var > 100
        }
    except Exception as e:
        return {"error": str(e)}

import cv2
import numpy as np
from pathlib import Path

print("🔄 OpenCV + YOLOv8 yükleniyor...")
yolo = YOLO('yolov8n.pt')
print("✅ YOLOv8 yüklendi")

INPUT_DIR = Path("/home/rw/code/trio/data/images_continuous/clean")
images = list(INPUT_DIR.glob("*.jpg"))[:10]

print(f"🔍 {len(images)} görsel test ediliyor...\n")

for img_path in images:
    print(f"\n📸 {img_path.name}:")
    
    # YOLO detection
    results = yolo(img_path, verbose=False)
    for r in results:
        if r.boxes is not None:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                if conf > 0.3:
                    xyxy = box.xyxy[0].tolist()
                    cls_name = yolo.names[int(box.cls[0])]
                    print(f"  🎯 YOLO: {cls_name} %{conf*100:.0f} @ {[round(x,1) for x in xyxy]}")
    
    # Text regions (MSER)
    text_reg = detect_text_regions(img_path)
    if 'error' not in text_reg:
        print(f"  📝 Text regions: {text_reg['regions_found']} found")
    
    # Edge patterns
    edges = detect_edges_patterns(img_path)
    if 'error' not in edges:
        print(f"  🔍 Edges: density={edges['edge_density']:.4f}, sharp={edges['sharp']}")
    
    # Watermark DCT
    wm = detect_watermark_dct(str(Path("/home/rw/code/trio/data/images_continuous/clean") / img_path.name))
    if 'error' not in wm:
        status = 'ŞÜPHELİ!' if wm['suspicious'] else 'Temiz'
        print(f"  💧 Watermark DCT: {status} (mean={wm['mean']}, std={wm['std']})")

print("\n✅ Test tamamlandı")