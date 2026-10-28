#!/usr/bin/env python3
"""
Subagent review script - Kalite kontrol
"""
import os
import json
from pathlib import Path

INPUT_DIR = "/home/rw/Projects/scraped-images/photocraft-final"
REVIEW_DIR = "/home/rw/Projects/scraped-images/reviewed"
APPROVED_DIR = "/home/rw/Projects/scraped-images/approved"

os.makedirs(REVIEW_DIR, exist_ok=True)
os.makedirs(APPROVED_DIR, exist_ok=True)

def review_image(image_path):
    """Subagent ile görsel kalite kontrolü"""
    # Vision model ile analiz
    # Bu kısım Hermes agent ile entegre edilecek
    pass

if __name__ == "__main__":
    images = list(Path(INPUT_DIR).glob("*"))
    print(f"📋 {len(images)} görsel review için hazır")
    
    for img in images:
        print(f"🔍 Review: {img.name}")
        # Subagent çağrısı buraya gelecek
    
    print("✅ Review tamamlandı")
