Abim (`Ozancan` / `1041604646`) icin rehber (`Kriss` / `TRIO Emlak` / `Gokcan-Ozancan`):

Calisacak sistem (`local`, `token` yok, `OpenCV` + `PhotoCraft`):

1. MANUAL BRUSH (`mouse` maske): `python3 /home/rw/Projects/rea-rev-engine/manual-interactive.py` -> `cleaned/interactive_mask_result.png`
2. BATCH (otomatik): `python3 /home/rw/Projects/rea-rev-engine/full-pipeline.py` -> `cleaned/` (`batch`) + `clean-log.csv` (`id,filename,status`)
3. PROFESYONEL (`auto mask` + `NS`): `python3 /home/rw/code/trio/scripts/professional_watermark_removal.py /home/rw/Downloads/IMG_...jpg --auto-mask --method ns --radius 5 --output /home/rw/Downloads/clean_prof/` -> `clean_...png` + `mask_...png` (`21.9%` beyaz)
4. PHOTOCRAFT (`batch`): `/home/rw/photocraft/apps/photocraft-cli` (`dun` test: `clean_prof/` `1.1MB`)
5. VISUAL (`slideshow` + `resize`): `python3 /home/rw/code/trio/scripts/visual_pipeline.py` -> `PIL LANCZOS` (`1200x1200`) + `WEBP` (`quality 80`) + `ffmpeg slideshow` (`mp4`)
6. SUNUM (`images_branded/`): `clean_...png` -> `sunum/index.html` (`line 411`: `images_branded/` -> `b64arr` birlestirme, `lazy` kaldirildi)

Sonraki adim: `batch` (`full-pipeline`) mi (`cleaned/` `16` dosya), `manual` (`interactive`) mi (`mouse` maske), `PhotoCraft` (`batch`) mi, `visual_pipeline` (`ffmpeg`) mi, `sunum` (`images_branded/`) guncelleme mi?

- `Kriss` (`AI Operator`, `back office`, `otonom`), `Gokcan` (`TRIO Emlak`), `Sifir Halusinasyon` (`verified`: `files`, `vision_analyze`, `curl -v`, `python3`).
