#!/usr/bin/env python3
"""Interactive manual brush — mouse ile maske çiz. Öğrenme amaçlı (acemi dostu)."""
import cv2, numpy as np, sys
img = cv2.imread('/home/rw/Downloads/IMG_20260909_150859.jpg')
mask = np.zeros(img.shape[:2], np.uint8)

def draw(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(mask, (x,y), 15, (255,255,255), -1)
        cv2.circle(img, (x,y), 15, (0,0,255), -1)
        print(f"Maske noktası: ({x},{y}) — bu 'manual brush' gibi çalışıyor.")

cv2.namedWindow('Manual Brush — mouse ile çiz, ESC çık')
cv2.setMouseCallback('Manual Brush — mouse ile çiz, ESC çık', draw)
print("Başla: mouse sol tıkla maske çiz. ESC = çık.")
while True:
    cv2.imshow('Manual Brush — mouse ile çiz, ESC çık', img)
    if cv2.waitKey(1) == 27:
        break
result = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
cv2.imwrite('/home/rw/Downloads/cleaned/interactive_mask_result.png', result)
print("Kaydedildi: interactive_mask_result.png")
