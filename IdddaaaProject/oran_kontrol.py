#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"Oran Yok" İzleyicisi
=====================
Bültene giren ama oranı henüz yayınlanmamış maçları (Süper Lig maçları gibi)
düzenli olarak yeniden kontrol eder. Oran geldiğinde bülteni günceller.

NEDEN GEREKLİ?
  iddaa API'sinde type=0 (bülten) ve type=1 (geniş liste) farklı kümeler döndürür.
  Süper Lig maçları maç gününe yaklaşana kadar bültene oransız girebilir
  (örn. Alanyaspor-Kocaelispor). Bu izleyici o maçları takip eder.

ÇALIŞMA MANTIĞI:
  1. bulten.json'da market'i boş maçları bul
  2. Bülteni yeniden çek
  3. Oranı gelen maçları bültene işle
  4. Değişiklik varsa bulten.json + gunluk_log.json'a yaz ve bildir

ÇALIŞTIRMA:
  python3 oran_kontrol.py
  python3 oran_kontrol.py --quiet     # değişiklik yoksa sessiz
"""

import argparse
import json
import os
import sys
from datetime import datetime

# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iddaa_scraper import (  # noqa: E402
    DEFAULT_COMPETITIONS, _session, fetch_competitions, fetch_events, build_bulletin,
)

DATA = "/data/iddaa"
BULTEN = os.path.join(DATA, "bulten.json")
LOG = os.path.join(DATA, "gunluk_log.json")


def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError):
            return default
    return default


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser(description="Oran yok izleyicisi")
    ap.add_argument("--verbose", action="store_true",
                    help="Değişiklik olmasa bile tüm adımları yazdır")
    ap.add_argument("--lig", type=int, action="append", dest="ligs")
    args = ap.parse_args()
    verbose = args.verbose  # cron: sessiz (değişiklik yoksa çıktı yok -> bildirim yok)

    rows = load_json(BULTEN, [])
    if not rows:
        print("Bülten boş — önce iddaa_scraper.py çalıştırın.")
        return 1

    # 1) Oranı olmayan maçları bul
    pending = [r for r in rows if not r.get("markets") or r.get("raw_market_count", 0) == 0]
    if not pending:
        if verbose:
            print("Bekleyen maç yok — tüm maçların oranı mevcut.")
        return 0

    if verbose:
        print(f"Bekleyen maç: {len(pending)}")
        for r in pending:
            print(f"  - {r['home']} vs {r['away']} ({r['datetime']})")

    # 2) Bülteni yeniden çek
    comp_ids = set(args.ligs) if args.ligs else set(DEFAULT_COMPETITIONS)
    s = _session()
    comp_names = fetch_competitions(s)
    events = fetch_events(s, comp_ids)
    fresh = build_bulletin(events, comp_names)

    # 3) Oranı gelen maçları işle (YALNIZCA bekleyenler)
    by_key = {(f["home"], f["away"]): f for f in fresh}
    pending_keys = {(r["home"], r["away"]) for r in pending}
    resolved = []
    updated_rows = list(rows)
    for idx, r in enumerate(updated_rows):
        if (r["home"], r["away"]) not in pending_keys:
            continue
        fresh_row = by_key.get((r["home"], r["away"]))
        if fresh_row and (fresh_row.get("markets") or fresh_row.get("raw_market_count", 0) > 0):
            updated_rows[idx] = fresh_row
            resolved.append(r)

    if not resolved:
        if verbose:
            print("Henüz oran yayınlanmadı.")
        return 0

    # 4) Kaydet
    save_json(BULTEN, updated_rows)
    log = load_json(LOG, {"girisler": [], "son_guncelleme": ""})
    log.setdefault("girisler", [])
    for r in resolved:
        log["girisler"].append({
            "tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "mac": f"{r['home']} vs {r['away']}",
            "durum": "oran_yayinlandi",
            "kaynak": "oran_kontrol",
        })
    log["son_guncelleme"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    save_json(LOG, log)

    print(f"\n✅ {len(resolved)} maçın oranı yayınlandı ve bültene işlendi:")
    for r in resolved:
        m = by_key[(r["home"], r["away"])]
        print(f"  - {r['home']} vs {r['away']}")
        ms = m["markets"].get("MS", {}).get("odds", {})
        print(f"      MS: {ms.get('1')}/{ms.get('0')}/{ms.get('2')}  |  "
              f"İY: {m['markets'].get('IY', {}).get('odds', {}).get('1')}/"
              f"{m['markets'].get('IY', {}).get('odds', {}).get('0')}/"
              f"{m['markets'].get('IY', {}).get('odds', {}).get('2')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
