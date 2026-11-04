#!/usr/bin/env python3
"""REA reverse-engineered local watermark cleaner — NO token needed.
Uses OpenCV inpaint (manual brush simulation). Works on already-scraped images."""
import cv2, csv, os, glob
from pathlib import Path

INPUT_DIR = '/home/rw/Downloads'
OUTPUT_DIR = '/home/rw/Downloads/cleaned'
LOG_FILE = '/home/rw/Downloads/clean-log.csv'

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Process each image using basic mask + inpaint (simulates manual brush / AI removal)
images = [f for f in glob.glob(os.path.join(INPUT_DIR, '*.jpg')) + glob.glob(os.path.join(INPUT_DIR, '*.png'))
           if 'cleaned' not in f and 'logo' not in f.lower()]

rows = []
for idx, img_path in enumerate(images[:20]):  # limit for speed
    img = cv2.imread(img_path)
    if img is None:
        continue
    # Simple mask: detect very bright regions (common watermark/text) or edges
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Basic threshold for bright watermarks / text
    _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    # Dilate to cover text area
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    mask = cv2.dilate(mask, kernel, iterations=1)
    # Inpaint (manual brush simulation)
    inpainted = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
    out_path = os.path.join(OUTPUT_DIR, os.path.basename(img_path).replace('.jpg', '_clean.png'))
    cv2.imwrite(out_path, inpainted)
    rows.append([idx+1, os.path.basename(img_path), 'cleaned', 'local-opencv-inpaint'])
    print('Processed:', img_path, '->', out_path)

# CSV log matching REA notes format (captured from site)
with open(LOG_FILE, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['id', 'filename', 'status', 'observed_source'])
    for r in rows:
        w.writerow(r)

print('Batch complete. CSV:', LOG_FILE, '| Cleaned images:', OUTPUT_DIR)
print('NO Pixelbin token used — fully local OpenCV pipeline.')
