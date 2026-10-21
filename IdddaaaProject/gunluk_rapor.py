#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
İddaa Tahmin Motoru
===================
Bülten oranlarından (odds) implied probability hesaplayarak
A / B / C filtrelerini uygular ve güven skoru üretir.

FİLTRELER (sistem direktifi):
  🅰️ İY KG Var            -> İY'de karşılıklı gol
  🅱️ Her İki Yarıda Gol   -> 1. ve 2. yarıda da gol
  🅲 İY Sonucu (1 / 2)    -> İlk yarı sonucu

GÜVEN SKORU: 0-10 arası; 7.5 altı öneriye alınmaz.

ÇALIŞTIRMA:
  python3 gunluk_rapor.py
  python3 gunluk_rapor.py --lig 584
  python3 gunluk_rapor.py --min-güven 7.0
"""

import argparse
import csv
import json
import os
import subprocess
import sys
from datetime import datetime

# ---------------------------------------------------------------------------
# İddaa proje dizini
# ---------------------------------------------------------------------------
PROJ = "/home/rw/Projects/IdddaaaProject"
DATA = "/data/iddaa"
VENV = "/home/rw/.hermes/hermes-agent/venv/bin/python"

MIN_GUVEN = 7.5  # Direktif: 7.5 altı öneriye alınmaz


# ---------------------------------------------------------------------------
# Odds -> implied probability
# ---------------------------------------------------------------------------
def implied(odds):
    """Odds sözlüğünden margin normalize edilmiş implied probability üretir."""
    raw = {}
    for k, v in odds.items():
        try:
            f = float(v)
            if f and f > 1.0:
                raw[k] = 1.0 / f
        except (TypeError, ValueError):
            continue
    total = sum(raw.values())
    if total <= 0:
        return {}
    return {k: v / total for k, v in raw.items()}


def _get(markets, key, default=None):
    return markets.get(key, default or {})


def _odd(markets, key, name):
    try:
        v = _get(markets, key, {}).get("odds", {}).get(name)
        return float(v) if v is not None else None
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Skorlama
# ---------------------------------------------------------------------------
def _inv(x, lo, hi):
    """Düşük odds = yüksek skor (0-10). Veri yoksa 0.0."""
    if x is None:
        return 0.0
    t = (x - lo) / (hi - lo)
    t = max(0.0, min(1.0, t))
    return (1.0 - t) * 10.0


def _norm(x, lo, hi):
    """Yüksek değer = yüksek skor (0-10). Veri yoksa 0.0."""
    if x is None:
        return 0.0
    t = (x - lo) / (hi - lo)
    t = max(0.0, min(1.0, t))
    return t * 10.0


def _f(odds, key):
    try:
        v = odds.get(key)
        return float(v) if v is not None else None
    except (TypeError, ValueError):
        return None


def _weighted(parts):
    """parts: [(skor, ağırlık), ...] — None skorlar atlanır."""
    num = den = 0.0
    for s, w in parts:
        if s is None:
            continue
        num += s * w
        den += w
    return (num / den) if den > 0 else 0.0


def score_iy_kg(row):
    """🅰️ İY KG Var skoru (0-10).

    Birincil sinyal: KG Var oranı (düşük = karşılıklı gol daha olası).
    İkincil: toplam gol beklentisi, İY beraberlik olasılığı.
    """
    m = row["markets"]
    kg = _get(m, "KG", {}).get("odds", {})
    iy = _get(m, "IY", {}).get("odds", {})
    au = _get(m, "ALTUST_2.5", {}).get("odds", {})

    parts = [
        (_inv(_f(kg, "Var"), 1.25, 1.95), 0.55),
        (_inv(_f(au, "Üst"), 1.40, 2.20), 0.20),
        (_norm(_f(iy, "0"), 1.80, 4.20), 0.15),
        (_inv(_f(iy, "1"), 1.50, 4.50), 0.05),
        (_inv(_f(iy, "2"), 1.50, 4.50), 0.05),
    ]
    return round(_weighted(parts), 1)


def score_iki_yari(row):
    """🅱️ Her iki yarıda da gol skoru (0-10)."""
    m = row["markets"]
    au25 = _get(m, "ALTUST_2.5", {}).get("odds", {})
    au35 = _get(m, "ALTUST_3.5", {}).get("odds", {})
    iy = _get(m, "IY", {}).get("odds", {})
    kg = _get(m, "KG", {}).get("odds", {})

    parts = [
        (_inv(_f(au25, "Üst"), 1.40, 2.20), 0.30),
        (_inv(_f(au35, "Üst"), 1.50, 2.80), 0.30),
        (_inv(_f(kg, "Var"), 1.25, 1.95), 0.25),
        (_inv(_f(iy, "1"), 1.50, 4.50), 0.075),
        (_inv(_f(iy, "2"), 1.50, 4.50), 0.075),
    ]
    return round(_weighted(parts), 1)


def score_iy_sonuc(row):
    """🅲 İY Sonucu skoru (0-10) — ev sahibi lehine mi, deplasmana mı?"""
    m = row["markets"]
    iy = _get(m, "IY", {}).get("odds", {})
    ms = _get(m, "MS", {}).get("odds", {})
    hk = _get(m, "HANDIKAP", {})

    iy1, iy2 = _f(iy, "1"), _f(iy, "2")
    ms1, ms2 = _f(ms, "1"), _f(ms, "2")

    # İY lehimi (birincil) — implied olasılık farkı
    if iy1 and iy2:
        q1, q2 = 1.0 / iy1, 1.0 / iy2
        iy_adv = abs(q1 - q2) / (q1 + q2)
    else:
        iy_adv = 0.0

    # Kadro değeri proxy'si: MS olasılık farkı (ikincil)
    if ms1 and ms2:
        p1, p2 = 1.0 / ms1, 1.0 / ms2
        ms_adv = abs(p1 - p2) / (p1 + p2)
    else:
        ms_adv = 0.0

    pick = "1" if (iy1 is not None and iy1 <= (iy2 or 1e9)) else "2"
    base = _norm(iy_adv, 0.05, 0.75) * 0.7 + _norm(ms_adv, 0.10, 0.60) * 0.3

    # Handikap ayarı (sov: ev sahibine verilen handikap)
    sov = hk.get("sov")
    if sov is not None:
        try:
            h = float(sov)
            if h < 0 and pick == "1":
                base = min(base + 0.5, 10.0)
            elif h < 0 and pick == "2":
                base = max(base - 0.5, 0.0)
            elif h > 0 and pick == "2":
                base = min(base + 0.5, 10.0)
            elif h > 0 and pick == "1":
                base = max(base - 0.5, 0.0)
        except (TypeError, ValueError):
            pass

    return pick, round(base, 1)


# ---------------------------------------------------------------------------
# Rapor
# ---------------------------------------------------------------------------
def _slug(name):
    """Takım adından 3 harflik kod üretir (boşluk/nokta temizlenir)."""
    parts = [p for p in (name or "").replace(".", " ").split() if p]
    return ("".join(parts)[:3].upper()) or (name or "?")[:3].upper()


def analyze(rows):
    """Tüm maçları analiz eder, öneri listesi üretir."""
    out = []
    for r in rows:
        m = r["markets"]
        if not m.get("MS") or not m.get("IY"):
            continue  # Oran yok -> analiz edilemez

        code = f"{_slug(r['home'])}-{_slug(r['away'])}"
        s_kg = round(score_iy_kg(r), 1)
        s_2y = round(score_iki_yari(r), 1)
        iy_pick, s_iy = score_iy_sonuc(r)

        # Öneri seçimi: en yüksek skorlu filtre
        candidates = [
            ("İY KG Var", s_kg),
            ("1. ve 2. Yarı Gol Olur", s_2y),
            (f"İY {iy_pick}", s_iy),
        ]
        candidates = [c for c in candidates if c[1] >= MIN_GUVEN]
        if not candidates:
            continue
        bahis, skor = max(candidates, key=lambda x: x[1])

        out.append({
            "code": code,
            "home": r["home"],
            "away": r["away"],
            "datetime": r["datetime"],
            "competition": r["competition_name"],
            "bahis": bahis,
            "skor": skor,
            "s_kg": s_kg,
            "s_2y": s_2y,
            "s_iy": s_iy,
            "iy_pick": iy_pick,
            "odds_ms": m.get("MS", {}).get("odds", {}),
            "odds_iy": m.get("IY", {}).get("odds", {}),
            "odds_kg": m.get("KG", {}).get("odds", {}),
            "odds_au": m.get("ALTUST_2.5", {}).get("odds", {}),
        })
    out.sort(key=lambda x: x["skor"], reverse=True)
    return out


def to_markdown(recs, all_rows):
    lines = [
        "# 🎯 GÜNÜN YÜKSEK POTANSIYELLİ İDDAA & TAKTİK ANALİZ RAPORU",
        "",
        f"**Tarih:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Bülten maç sayısı:** {len(all_rows)}",
        f"**Öneri sayısı (güven ≥ {MIN_GUVEN}):** {len(recs)}",
        "",
        "| Maç Kodu & Karşılaşma | Önerilen Bahis | Güven Skoru | Kadro & Oran Analizi | Taktik/Baskı Gerekçesi |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]
    for r in recs:
        ms = r["odds_ms"]
        iy = r["odds_iy"]
        kg = r["odds_kg"]
        au = r["odds_au"]

        def f(d, k):
            v = d.get(k)
            return f"{v:.2f}" if isinstance(v, (int, float)) else "-"

        ms_str = f"{f(ms,'1')}/{f(ms,'0')}/{f(ms,'2')}"
        iy_str = f"{f(iy,'1')}/{f(iy,'0')}/{f(iy,'2')}"
        kg_str = f"Var {f(kg,'Var')} / Yok {f(kg,'Yok')}"
        au_str = f"2.5 A/Ü {f(au,'Alt')}/{f(au,'Üst')}"

        # Kadro/oran yorumu
        try:
            ms1, ms2 = float(ms.get("1", 0)), float(ms.get("2", 0))
            diff = (ms1 - ms2) / max(ms1, ms2, 1) * 100
            kadro = (f"Favori {r['home'] if ms1 < ms2 else r['away']} "
                     f"(MS oranı {abs(diff):.0f}% fark)")
        except (TypeError, ValueError):
            kadro = "Oran verisi yetersiz"

        # Taktik yorumu
        try:
            kg_var = float(kg.get("Var", 0))
            kg_yok = float(kg.get("Yok", 0))
            taktik = (f"KG Var {kg_var:.2f} < Yok {kg_yok:.2f} → karşılıklı gol eğilimi yüksek"
                      if kg_var < kg_yok else
                      f"KG Var {kg_var:.2f} ≥ Yok {kg_yok:.2f} → tek taraflı gol eğilimi")
        except (TypeError, ValueError):
            taktik = "KG oranı yok"

        lines.append(
            f"| **[{r['code']}]** {r['home']} vs {r['away']} | **{r['bahis']}** | "
            f"**{r['skor']} / 10** | MS {ms_str} · İY {iy_str} · {kadro} | {kg_str} · {au_str} · {taktik} |"
        )

    lines.append("")
    return "\n".join(lines)


def to_json(recs, path):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({
            "tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "min_guven": MIN_GUVEN,
            "oneri_sayisi": len(recs),
            "ononeriler": recs,
        }, fh, ensure_ascii=False, indent=2)


def main():
    ap = argparse.ArgumentParser(description="İddaa tahmin motoru")
    ap.add_argument("--lig", type=int, action="append", dest="ligs")
    ap.add_argument("--min-guven", type=float, default=None)
    ap.add_argument("--skip-scrape", action="store_true",
                    help="Bülten yeniden çekilmez, mevcut bulten.json kullanılır")
    args = ap.parse_args()

    if args.min_guven is not None:
        globals()["MIN_GUVEN"] = args.min_guven

    os.makedirs(DATA, exist_ok=True)

    # 1) Bülteni çek
    if not args.skip_scrape:
        print("[1/3] Bülten çekiliyor...")
        cmd = [VENV, os.path.join(PROJ, "iddaa_scraper.py"), "--json",
               "--out", DATA]
        if args.ligs:
            for lg in args.ligs:
                cmd += ["--lig", str(lg)]
        rc = subprocess.call(cmd)
        if rc != 0:
            print("      Scraper hatası, mevcut veriyle devam ediliyor.")
    else:
        print("[1/3] Bülten çekimi atlandı (--skip-scrape)")

    # 2) Veriyi oku
    print("[2/3] Bülten verisi okunuyor...")
    bulten_json = os.path.join(DATA, "bulten.json")
    if not os.path.exists(bulten_json):
        print(f"      !! {bulten_json} yok")
        return 1
    rows = json.load(open(bulten_json, encoding="utf-8"))
    print(f"      {len(rows)} maç")

    # 3) Analiz
    print("[3/3] Tahmin motoru çalışıyor...")
    recs = analyze(rows)
    print(f"      {len(recs)} öneri (güven ≥ {MIN_GUVEN})")

    md = to_markdown(recs, rows)
    md_path = os.path.join(DATA, "analiz_raporu.md")
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write(md)
    json_path = os.path.join(DATA, "analiz_raporu.json")
    to_json(recs, json_path)

    print(f"      Rapor : {md_path}")
    print(f"      JSON  : {json_path}")
    print()
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
