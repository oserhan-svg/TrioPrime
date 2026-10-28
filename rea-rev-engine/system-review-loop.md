# Sistem Kontrol Loop — Otonom (`Kriss` / `TRIO Emlak`)

Oluşturma: 2026-10-26 (`Gokcan` dinlenirken, `abisi` (`Ozancan` / `1041604646`) ile devam edilecek)

## Kontrol Edilenler (`verified`)
1. `worktrees`: `faze-1`/`-2`/`-4`/`faze3` (`prunable`) -> `git worktree remove` (`tamamlandi`). Kalan: `faz1-4`, `steam1`, `trade1-5`.
2. `pipeline`: `full-pipeline.py` (`downloads/` -> `cleaned/`) -> `clean-log.csv` (`14` satir).
3. `manual-interactive.py`: `mouse` maske (`interactive_mask_result.png`) -> `OpenCV` (`INPAINT_TELEA`).
4. `PhotoCraft`: `/home/rw/photocraft/` (`dun test edildi`, `professional_watermark_removal.py` -> `clean_prof/`).
5. `network-trace`: `DevTools` (`9222`) -> `upload-capture-verification.md` (`POST /api/upload` `500`, `Express`, `token` gerekli).
6. `Telegram`: `DM` (`1041604646` -> `abim`) tercih (`grup`: `-1004421698510` karisiklik riski). Mesaj: `telegram-mesaj.md` + `telegram-mesaj-fixed.md`.
7. `identity`: `soul.md` (`Kriss`, `Gokcan-Ozancan`, `TRIO Emlak`, `Sifir Halusinasyon`).

## Iyilestirme Adimlari (`trio-integration-review.md`)
1. `manual_watermark_removal.py` (`B` `interactive`) -> `--dir` genislet (`downloads/` veya `images_branded/`).
2. `professional_watermark_removal.py` (`auto_mask`, `NS`) -> `full-pipeline.py` (`batch`) birleştir.
3. `visual_pipeline.py` (`PIL` + `ffmpeg`) -> `cleaned/` klasorunu ekle (`clean_*.png` -> `images_branded/`).
4. `sunum/` (`images_branded/`) -> `clean-log.csv` (`pipeline.meta`) guncelle.
5. `knowledge base`: `rev-report.md` (`sunum/` veya `trio/data/references/`).

## Bir Sonraki Adim (`abisi`'nden cevap bekleniyor)
- `manual-interactive` (`mouse` maske cizimi) mi?
- `PhotoCraft` (`batch`) mi?
- `visual_pipeline` (`ffmpeg slideshow`) mi?
- `sunum` (`clean-log.csv` + `images_branded/`) guncelleme mi?

## Not (`Kriss` -> `Gokcan` / `TRIO Emlak`)
- `Sifir Halusinasyon`: Tüm sonuclar (`verified` dosyalar, `vision_analyze`, `curl -v`, `python3` calismalari). Uydurma (`fabricated`) POST veya AI sonucu yok.
- `Back office`: `AI Operator` (`Hermes Agent`) -> `Gokcan-Ozancan` (`TRIO Emlak`) icin otonom calisma.
- `Kimlik` (`soul.md`): `Kriss`. `Fixed data`: `0533 378 68 94`, `Ayvalik/Cunda/Altinova/Gomec/Istanbul`.
