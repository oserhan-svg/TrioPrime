#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
İddaa Bülten Scraper
====================
iddaa.com program bültenini sportsbook API üzerinden çeker.

KAYNAK (tersine mühendislik ile doğrulandı):
  https://sportsbookv2.iddaa.com/sportsbook/events?st=1&type=0&version=0&live=false
  -> st=1 (futbol), type=0 (bülten/maç listesi), live=false (hakemi yok, market'lar dolu)
  -> live=true kullanılırsa market'lar BOŞ gelir (sadece skor)

PAZAR KODLARI (outcome name'lerinden eşleştirilir):
  MS (Maç Sonucu)        t=1  st=1    1 / 0 / 2
  İY (İlk Yarı Sonucu)   t=2  st=88   1 / 0 / 2
  Handikaplı MS          t=2  st=100  1 / 0 / 2   (sov = handikap)
  Alt/Üst                t=2  st=101  Alt / Üst   (sov = 2.5, 1.5, 3.5 ...)
  KG (Karşılıklı Gol)    t=2  st=89   Var / Yok
  İY/MS kombinasyonu     t=2  st=90   1/1, 1/0, 0/1 ...
  Korner Alt/Üst         t=2  st=48   Alt / Üst   (sov = 9.5, 10.5 ...)

LİG KODLARI (competitions endpoint):
  Türkiye Süper Lig            ci=584
  UEFA Şampiyonlar Ligi        ci=46194  (ayrıca 126 = Şampiyonlar Ligi)

ÇALIŞTIRMA:
  python3 iddaa_scraper.py
  python3 iddaa_scraper.py --lig 584        # sadece Süper Lig
  python3 iddaa_scraper.py --out /data/     # özel çıktı dizini
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime

from curl_cffi import requests

# ---------------------------------------------------------------------------
# Yapılandırma
# ---------------------------------------------------------------------------
BASE_HEADERS = {
    "User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"),
    "Accept": "application/json",
    "Origin": "https://www.iddaa.com",
    "Referer": "https://www.iddaa.com/",
}

API_EVENTS = "https://sportsbookv2.iddaa.com/sportsbook/events?st=1&type=0&version=0&live=false"
API_COMPETITIONS = "https://sportsbookv2.iddaa.com/sportsbook/competitions"

# Lig filtresi (default: Süper Lig + Şampiyonlar Ligi)
DEFAULT_COMPETITIONS = {
    584: "Türkiye Süper Lig",
    46194: "UEFA Şampiyonlar Ligi",
    126: "Şampiyonlar Ligi",
}

# Pazar eşleştirme tablosu: (t, st) -> pazar adı
MARKET_MAP = {
    (1, 1): "MS",           # Maç Sonucu
    (2, 88): "IY",          # İlk Yarı Sonucu
    (2, 100): "HANDIKAP",   # Handikaplı Maç Sonucu
    (2, 101): "ALTUST",     # Alt/Üst (sov ile)
    (2, 60): "ALTUST",      # Alt/Üst (sov ile)
    (2, 603): "ALTUST",
    (2, 604): "ALTUST",
    (2, 89): "KG",          # Karşılıklı Gol
    (2, 90): "IY_MS",       # İY/MS kombinasyonu
    (2, 7): "MS_ALTUST",    # MS + A/Ü kombinasyonu
    (2, 700): "ALTUST_KG",  # A/Ü + KG kombinasyonu
    (2, 48): "KORNER_AU",   # Korner Alt/Üst
    (2, 49): "KORNER_AU",
    (2, 91): "TEK_CIFT",
    (2, 720): "EVET_HAYIR",
    (2, 92): "MS_KOMBI",
    (2, 77): "MS_KOMBI",
    (2, 4): "GOL_ARALIKLARI",
    (2, 36): "IY_MS_ALT",   # İY/MS/AÜ kombinasyonu
    (2, 698): "MS_KG",
    (2, 699): "MS_KG",
    (2, 6): "Devre",
    (2, 69): "EVET_HAYIR",
    (2, 72): "EVET_HAYIR",
    (2, 722): "ALTUST",
    (2, 723): "ALTUST",
}

# Hedef pazarlar (bülten çıktısı için)
TARGET_MARKETS = ["MS", "IY", "HANDIKAP", "ALTUST", "KG"]


# ---------------------------------------------------------------------------
# Yardımcılar
# ---------------------------------------------------------------------------
def _session():
    s = requests.Session(impersonate="chrome")
    s.headers.update(BASE_HEADERS)
    return s


def _safe_get(s, url, timeout=25):
    r = s.get(url, timeout=timeout)
    r.raise_for_status()
    return r.json()


def _epoch_to_local(ts):
    """iddaa 'd' alanı epoch SANİYE cinsindendir."""
    try:
        return datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M")
    except (TypeError, ValueError):
        return ""


def _pick_outs(outcomes, names):
    """Verilen outcome name'lerine göre sözlük döndürür."""
    result = {}
    for o in outcomes or []:
        n = (o.get("n") or "").strip()
        if n in names:
            result[n] = o.get("odd")
    return result


def _norm_market_key(t, st):
    return (t, st)


# ---------------------------------------------------------------------------
# Çekirdek
# ---------------------------------------------------------------------------
def fetch_events(s, competition_ids=None):
    """Bülten maçlarını çeker.

    type=0 -> oranları dolu bülten maçları (ana kaynak)
    type=1 -> daha geniş liste (Süper Lig gibi henüz oranı yayınlanmamış maçlar)
    İkisi merge edilir: aynı maç ID'si için market dolu olan referans alınır.
    """
    by_id = {}
    for _type in (0, 1):
        url = (f"https://sportsbookv2.iddaa.com/sportsbook/events"
               f"?st=1&type={_type}&version=0&live=false")
        data = _safe_get(s, url)["data"]
        for e in data.get("events", []) or []:
            _id = e.get("i")
            prev = by_id.get(_id)
            if prev is None or len(e.get("m", []) or []) > len(prev.get("m", []) or []):
                by_id[_id] = e
    events = list(by_id.values())
    if competition_ids is None:
        return events
    return [e for e in events if e.get("ci") in competition_ids]


def fetch_competitions(s):
    """Lig/kulüp listesini çeker (kod -> isim)."""
    comps = _safe_get(s, API_COMPETITIONS)["data"] or []
    return {c.get("i"): c.get("n") for c in comps}


def parse_event(event):
    """Tek bir maçı normalize eder."""
    parsed = {
        "event_id": event.get("i"),
        "competition_id": event.get("ci"),
        "home": event.get("hn"),
        "away": event.get("an"),
        "datetime": _epoch_to_local(event.get("d")),
        "is_live": bool(event.get("il")),
        "markets": {},
        "raw_market_count": len(event.get("m", []) or []),
    }

    for m in event.get("m", []) or []:
        key = _norm_market_key(m.get("t"), m.get("st"))
        name = MARKET_MAP.get(key)
        if not name:
            continue
        sov = m.get("sov")
        outcomes = m.get("o", []) or []

        # Alt/Üst gibi tek başına sov'e bağlı pazarlar için altın anahtar
        if name == "ALTUST" and sov is not None:
            sub_key = f"ALTUST_{sov}"
        elif name == "KORNER_AU" and sov is not None:
            sub_key = f"KORNER_AU_{sov}"
        else:
            sub_key = name

        entry = {"sov": sov, "odds": _pick_outs(outcomes, _OUTCOME_NAMES.get(name, []))}
        # Aynı alt anahtar birden fazla kez gelirse son kazanır
        parsed["markets"][sub_key] = entry

    return parsed


# Pazar başına beklenen outcome isimleri
_OUTCOME_NAMES = {
    "MS": ["1", "0", "2"],
    "IY": ["1", "0", "2"],
    "HANDIKAP": ["1", "0", "2"],
    "ALTUST": ["Alt", "Üst"],
    "KG": ["Var", "Yok"],
    "IY_MS": ["1/1", "1/0", "1/2", "0/1", "0/0", "0/2", "2/1", "2/0", "2/2"],
    "MS_ALTUST": ["1 ve Alt", "0 ve Alt", "2 ve Alt", "1 ve Üst", "0 ve Üst", "2 ve Üst"],
    "ALTUST_KG": ["Alt ve Var", "Üst ve Var", "Alt ve Yok", "Üst ve Yok"],
    "MS_KOMBI": ["1 ve 0", "1 ve 2", "0 ve 2"],
    "KORNER_AU": ["Alt", "Üst"],
    "TEK_CIFT": ["Tek", "Çift"],
    "EVET_HAYIR": ["Evet", "Hayır"],
    "GOL_ARALIKLARI": ["0-1 gol", "2-3 gol", "4-5 gol", "6+ gol"],
    "MS_KG": ["1 ve Var", "1 ve Yok", "0 ve Var", "0 ve Yok", "2 ve Var", "2 ve Yok"],
    "Devre": ["1.", "Eşit", "2."],
    "IY_MS_ALT": ["1/1", "1/0", "1/2", "0/1", "0/0", "0/2"],
}


def build_bulletin(events, competition_names):
    """Maçları lig ve tarih sırasına göre bülten formatında döndürür."""
    rows = []
    for e in events:
        p = parse_event(e)
        p["competition_name"] = competition_names.get(p["competition_id"], str(p["competition_id"]))
        rows.append(p)
    rows.sort(key=lambda r: (r["datetime"], r["competition_name"]))
    return rows


def to_markdown(rows):
    lines = [
        "# İDDAA BÜLTENİ",
        "",
        f"**Tarih:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Maç sayısı:** {len(rows)}",
        "",
        "| # | Tarih | Lig | Maç | MS 1/X/2 | İY 1/X/2 | Handikap | 2.5 A/Ü | KG Var/Yok |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(rows, 1):
        m = r["markets"]
        ms = m.get("MS", {}).get("odds", {})
        iy = m.get("IY", {}).get("odds", {})
        hk = m.get("HANDIKAP", {})
        hk_odds = hk.get("odds", {})
        au = m.get("ALTUST_2.5", {}).get("odds", {})
        kg = m.get("KG", {}).get("odds", {})

        def f(d, k):
            v = d.get(k)
            return f"{v:.2f}" if isinstance(v, (int, float)) else "-"

        lines.append(
            f"| {i} | {r['datetime']} | {r['competition_name']} | "
            f"**{r['home']}** - **{r['away']}** | "
            f"{f(ms,'1')}/{f(ms,'0')}/{f(ms,'2')} | "
            f"{f(iy,'1')}/{f(iy,'0')}/{f(iy,'2')} | "
            f"{hk.get('sov','-')}: {f(hk_odds,'1')}/{f(hk_odds,'0')}/{f(hk_odds,'2')} | "
            f"{f(au,'Alt')}/{f(au,'Üst')} | "
            f"{f(kg,'Var')}/{f(kg,'Yok')} |"
        )
    lines.append("")
    return "\n".join(lines)


def to_csv(rows, path):
    header = ["event_id", "datetime", "competition", "home", "away",
              "ms_1", "ms_0", "ms_2", "iy_1", "iy_0", "iy_2",
              "handikap", "hk_1", "hk_0", "hk_2",
              "au25_alt", "au25_ust", "kg_var", "kg_yok"]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        for r in rows:
            m = r["markets"]
            ms = m.get("MS", {}).get("odds", {})
            iy = m.get("IY", {}).get("odds", {})
            hk = m.get("HANDIKAP", {})
            au = m.get("ALTUST_2.5", {}).get("odds", {})
            kg = m.get("KG", {}).get("odds", {})
            w.writerow([
                r["event_id"], r["datetime"], r["competition_name"], r["home"], r["away"],
                ms.get("1"), ms.get("0"), ms.get("2"),
                iy.get("1"), iy.get("0"), iy.get("2"),
                hk.get("sov"), hk.get("odds", {}).get("1"), hk.get("odds", {}).get("0"), hk.get("odds", {}).get("2"),
                au.get("Alt"), au.get("Üst"),
                kg.get("Var"), kg.get("Yok"),
            ])


def main():
    ap = argparse.ArgumentParser(description="İddaa bülten scraper")
    ap.add_argument("--lig", type=int, action="append", dest="ligs",
                    help="Sadece belirtilen kulüp kodlarını çek (örn. --lig 584)")
    ap.add_argument("--out", default="/data/iddaa",
                    help="Çıktı dizini (default: /data/iddaa)")
    ap.add_argument("--json", action="store_true", help="Ham JSON da yaz")
    args = ap.parse_args()

    comp_ids = set(args.ligs) if args.ligs else set(DEFAULT_COMPETITIONS)

    s = _session()
    print("[1/3] Lig listesi çekiliyor...")
    comp_names = fetch_competitions(s)
    print(f"      {len(comp_names)} lig/kulüp alındı")

    print("[2/3] Bülten maçları çekiliyor...")
    events = fetch_events(s, comp_ids)
    print(f"      {len(events)} maç bulundu")

    if not events:
        print("      !! Filtreye uyan maç yok. Mevcut kulüp kodlarını listeliyorum:")
        for cid, cname in list(comp_names.items())[:40]:
            print(f"         {cid}: {cname}")
        return 1

    rows = build_bulletin(events, comp_names)
    print("[3/3] Çıktılar yazılıyor...")

    os.makedirs(args.out, exist_ok=True)
    md_path = os.path.join(args.out, "bulten.md")
    csv_path = os.path.join(args.out, "bulten.csv")
    json_path = os.path.join(args.out, "bulten.json")

    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write(to_markdown(rows))
    to_csv(rows, csv_path)
    if args.json:
        with open(json_path, "w", encoding="utf-8") as fh:
            json.dump(rows, fh, ensure_ascii=False, indent=2)

    print(f"      Markdown : {md_path}")
    print(f"      CSV      : {csv_path}")
    if args.json:
        print(f"      JSON     : {json_path}")

    print("\n" + to_markdown(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
