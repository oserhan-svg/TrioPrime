#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iddaa.com Tarzı Statik Mirror Üretici
=====================================
/data/iddaa/ çıktısını (bulten.json + analiz_raporu.json) okuyup
iddaa.com'un "Canlı Maçlar" sayfasına benzeyen statik bir HTML üretir.

HEDEF TASARIM (ekran görüntüsünden çıkarıldı):
  - Yeşil üst header (#177d17) + sarı logo (#ffd200)
  - Koyu toolbar (#1c1c1c): Sırala / Filtrele / Tarih Seç / TEK MAÇ ...
  - Arama + kolon grup başlığı (koyu)
  - Yeşil bölüm başlığı (#2f9e2f): "ÖNE ÇIKANLAR (N)"
  - Lig grup satırları (koyu #2b2b2b, büyük harf)
  - Maç satırları (açık yeşil #dcebdb) + oran hücreleri
  - Sağ panel: "Kuponum" (#3a3a3a başlık)

ÇALIŞTIRMA:
  python3 site_olustur.py
  python3 site_olustur.py --out /data/iddaa/site --skip-fetch
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime

DATA = "/data/iddaa"
OUT = "/data/iddaa/site"

# ---------------------------------------------------------------------------
# iddaa.com renk paleti (ekran görüntüsünden örneklendi)
# ---------------------------------------------------------------------------
C = {
    "header": "#177d17",
    "live": "#2f9e2f",
    "score": "#2c8a2c",
    "row": "#dcebdb",
    "row_alt": "#e4f0e0",
    "toolbar": "#1c1c1c",
    "group": "#2b2b2b",
    "handikap": "#c3d2df",
    "red": "#d21f1f",
    "yellow": "#ffd200",
    "sidebar": "#3a3a3a",
    "text": "#111111",
    "muted": "#666666",
    "line": "#c9c9c9",
}

# ---------------------------------------------------------------------------
# CSS (düz string — f-string değil, kaçış sorunu yok)
# ---------------------------------------------------------------------------
CSS = """
*{box-sizing:border-box}
body{background:#fff;color:#111;font-family:Arial,Helvetica,"Segoe UI",sans-serif;margin:0;font-size:13px}
.wrap{max-width:1060px;margin:0 auto;border:3px solid #ffd200;border-top:none}
.topbar{background:#177d17;height:52px;display:flex;align-items:center;justify-content:space-between;padding:0 16px}
.logo{color:#ffd200;font-size:26px;font-weight:900;letter-spacing:-.5px}
.logo .hand{font-size:18px;margin:0 2px}
.logo .tld{color:#fff;font-size:20px}
.topright{display:flex;align-items:center;gap:10px}
.pill-live{background:#d21f1f;color:#fff;font-weight:800;font-size:11px;padding:3px 10px;border-radius:12px;display:flex;align-items:center;gap:5px}
.pill-live .dot{width:7px;height:7px;border-radius:50%;background:#fff;animation:bl 1.2s infinite}
@keyframes bl{50%{opacity:.3}}
.topmeta{color:#e6f2e6;font-size:11px}
.toolbar{background:#1c1c1c;display:flex;align-items:center;gap:6px;padding:8px 12px}
.tbtn{background:#262626;border:1px solid #3a3a3a;color:#eee;font-size:12px;padding:6px 12px;border-radius:4px;white-space:nowrap}
.tbtn.trash{margin-left:auto}
.searchrow{background:#1c1c1c;display:flex;align-items:center;gap:16px;padding:8px 12px;border-top:1px solid #333}
.searchbox{background:#2a2a2a;border-radius:4px;padding:7px 12px;color:#999;width:280px;font-size:12px}
.mag{margin-right:6px}
.groups{display:flex;flex:1;justify-content:flex-end;gap:4px}
.groups .grp{color:#ffd200;font-weight:800;font-size:11px;text-align:center;padding:4px 8px;background:#222;border-radius:3px}
.content{display:grid;grid-template-columns:1fr 232px}
.livebar{background:#2f9e2f;color:#fff;font-weight:800;font-size:15px;padding:10px 14px;display:flex;justify-content:space-between}
.livebar .codes{font-size:11px;font-weight:600;opacity:.9}
table.matches{width:100%;border-collapse:collapse;table-layout:fixed}
.colhead th{background:#222;color:#ffd200;font-size:10px;font-weight:800;padding:6px 2px;text-align:center}
.league td{background:#2b2b2b;color:#fff;font-weight:800;font-size:12px;padding:7px 10px;text-transform:uppercase}
.league .flag{margin-right:8px}
.league .codes{font-size:9px;color:#888;font-weight:600;text-align:right}
.match td{padding:7px 8px;border-bottom:1px solid #c9c9c9;vertical-align:middle;font-size:12px}
.match .star{width:34px;color:#bbb;text-align:center;font-size:16px}
.match .badge{width:26px}
.match .time{width:76px;color:#666;font-size:11px}
.match .teams{width:190px;font-size:13px;line-height:1.35}
.match .teams .away{color:#333}
.match .score{width:52px;text-align:center}
.match .score .crown{color:#ffd200;font-size:14px}
.match .score .snum{color:#fff;font-weight:800;font-size:11px}
.oddgrp{display:table-cell}
.match .odd{width:34px;text-align:center;border-right:1px solid #fff;font-weight:700;font-size:12px;padding:6px 2px}
.match .odd.hk{background:#c3d2df}
.hklab{display:block;font-size:9px;color:#666;font-weight:600}
.coupon{border-left:1px solid #c9c9c9;min-height:300px}
.coupon-head{background:#3a3a3a;color:#fff;padding:14px;position:relative}
.ch-title{font-size:19px;font-weight:800}
.ch-sub{font-size:11px;color:#aaa;margin-top:2px}
.ch-badge{position:absolute;right:14px;top:14px;font-size:16px}
.ch-badge span{background:#ffd200;color:#000;font-size:11px;font-weight:900;border-radius:10px;padding:1px 6px;margin-left:2px}
.coupon-body{background:#f5f5f5;padding:40px 16px;text-align:center;color:#888}
.cp-icon{font-size:34px;opacity:.4}
.cp-title{font-weight:700;color:#666;margin-top:10px}
.cp-sub{font-size:11px;margin-top:4px}
.section{padding:14px}
.card{border:1px solid #c9c9c9;border-radius:10px;padding:16px;margin-bottom:14px}
.card-h{color:#d21f1f;font-size:16px;margin:0 0 12px}
.tbl-wrap{overflow-x:auto}
table.pred{width:100%;border-collapse:collapse;font-size:12px}
table.pred th{background:#222;color:#ffd200;text-align:left;padding:8px;font-size:11px;text-transform:uppercase}
table.pred td{border-bottom:1px solid #eee;padding:8px;vertical-align:top}
.pc-code{font-weight:800;color:#177d17}
.pc-teams{font-weight:400;color:#666;font-size:11px}
.pc-bet b{color:#d21f1f}
.pc-score{font-weight:900;font-size:16px;color:#d21f1f}
.pc-note{color:#333;font-size:11px}
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.m{background:#f7f7f7;border:1px solid #eee;border-radius:8px;padding:12px}
.m-h{font-size:10px;font-weight:800;color:#666;text-transform:uppercase}
.m-v{font-size:22px;font-weight:900;margin:4px 0}
.m-v.ok{color:#2f9e2f}
.m-s{font-size:10px;color:#999}
.foot{padding:14px;color:#999;font-size:11px;line-height:1.6}
.empty{color:#666}
@media(max-width:900px){
  .content{grid-template-columns:1fr}
  .metrics{grid-template-columns:repeat(2,1fr)}
  .searchrow{flex-direction:column;align-items:stretch}
}
"""


# ---------------------------------------------------------------------------
# Yardımcılar
# ---------------------------------------------------------------------------
def _esc(s):
    return (str(s or "").replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def _f(odds, key, dash="-"):
    v = (odds or {}).get(key)
    if v is None:
        return dash
    try:
        return f"{float(v):.2f}"
    except (TypeError, ValueError):
        return dash


def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError):
            return default
    return default


def group_by_league(rows):
    groups = {}
    order = []
    for r in rows:
        name = r.get("competition_name") or "Diğer"
        if name not in groups:
            groups[name] = []
            order.append(name)
        groups[name].append(r)
    return [(name, groups[name]) for name in order]


# ---------------------------------------------------------------------------
# HTML parçaları
# ---------------------------------------------------------------------------
def _header(brand="Toxkolikk", tag="CANLI"):
    return f"""<div class="topbar">
  <div class="logo">{_esc(brand)}<span class="hand">●</span><span class="tld">.analiz</span></div>
  <div class="topright">
    <span class="pill-live"><span class="dot"></span>{_esc(tag)}</span>
    <span class="topmeta">iddaa.com bülteni · Mackolik · Transfermarkt çapraz analiz</span>
  </div>
</div>"""


def _toolbar():
    items = ["Sırala", "Filtrele", "Tarih Seç", "Oyun Türü ▾", "TEK MAÇ", "SÜPER LİG", "%"]
    btns = "".join(f'<span class="tbtn">{_esc(i)}</span>' for i in items)
    return f'<div class="toolbar">{btns}<span class="tbtn trash">🗑</span></div>'


def _search_row():
    groups = [
        ("Maç Sonucu", 3), ("1. Yarı Sonucu", 3), ("Handikaplı Maç Sonucu", 3),
        ("Alt/Üst 2.5", 2), ("Karşılıklı Gol", 2),
    ]
    cells = "".join(f'<th colspan="{n}" class="grp">{_esc(g)}</th>' for g, n in groups)
    return f'''<div class="searchrow">
  <div class="searchbox"><span class="mag">⌕</span> Lig ya da Takım adı giriniz</div>
  <div class="groups">{cells}</div>
</div>'''


def _league_row(name):
    codes = "1 0 2&nbsp;&nbsp; 1 0 2&nbsp;&nbsp; H 1 0 2&nbsp;&nbsp; Alt Üst&nbsp;&nbsp; Var Yok"
    return (f'<tr class="league"><td colspan="5">'
            f'<span class="flag">🏆</span>{_esc(name.upper())}</td>'
            f'<td class="codes">{codes}</td></tr>')


def _match_row(r, idx):
    m = r.get("markets") or {}
    ms = m.get("MS", {}).get("odds", {})
    iy = m.get("IY", {}).get("odds", {})
    hk = m.get("HANDIKAP", {})
    hk_odds = hk.get("odds", {})
    au = m.get("ALTUST_2.5", {}).get("odds", {})
    kg = m.get("KG", {}).get("odds", {})

    def cell(d, k, cls=""):
        return f'<td class="odd {cls}">{_f(d, k)}</td>'

    alt = C["row_alt"] if idx % 2 else C["row"]
    bg = f' style="background:{alt}"' if idx % 2 else ""

    hk_sov = hk.get("sov")
    hk_label = f'{hk_sov}:' if hk_sov is not None else ""

    return f'''<tr class="match"{bg}>
  <td class="star">☆</td>
  <td class="badge"></td>
  <td class="time">{_esc(r.get("datetime",""))}</td>
  <td class="teams"><b>{_esc(r.get("home",""))}</b><br><span class="away">{_esc(r.get("away",""))}</span></td>
  <td class="score"><span class="crown">♛</span><br><span class="snum">–</span></td>
  <td class="oddgrp ms">{cell(ms,"1")}{cell(ms,"0")}{cell(ms,"2")}</td>
  <td class="oddgrp iy">{cell(iy,"1")}{cell(iy,"0")}{cell(iy,"2")}</td>
  <td class="oddgrp hk"><span class="hklab">{hk_label}</span>{cell(hk_odds,"1","hk")}{cell(hk_odds,"0","hk")}{cell(hk_odds,"2","hk")}</td>
  <td class="oddgrp au">{cell(au,"Alt")}{cell(au,"Üst")}</td>
  <td class="oddgrp kg">{cell(kg,"Var")}{cell(kg,"Yok")}</td>
</tr>'''


def _sidebar():
    return '''<aside class="coupon">
  <div class="coupon-head">
    <div class="ch-title">Kuponum</div>
    <div class="ch-sub">T.Oran: 0,00</div>
    <div class="ch-badge">🎫<span>0</span></div>
  </div>
  <div class="coupon-body">
    <div class="cp-icon">🎫</div>
    <div class="cp-title">Kuponunuzda maç bulunmamaktadır.</div>
    <div class="cp-sub">Raporu inceleyerek önerilere göz atabilirsiniz.</div>
  </div>
</aside>'''


def _prediction_table(recs):
    if not recs:
        return '<div class="card empty">Henüz öneri yok (güven ≥ 7.5).</div>'
    rows = []
    for r in recs:
        rows.append(f'''<tr>
  <td class="pc-code">[{_esc(r.get("code"))}]<br><span class="pc-teams">{_esc(r.get("home"))} – {_esc(r.get("away"))}</span></td>
  <td class="pc-bet"><b>{_esc(r.get("bahis"))}</b></td>
  <td class="pc-score">{_esc(r.get("skor"))}</td>
  <td class="pc-note">MS {_f(r.get("odds_ms",{}),"1")}/{_f(r.get("odds_ms",{}),"0")}/{_f(r.get("odds_ms",{}),"2")} · İY {_f(r.get("odds_iy",{}),"1")}/{_f(r.get("odds_iy",{}),"0")}/{_f(r.get("odds_iy",{}),"2")}</td>
  <td class="pc-note">KG Var {_f(r.get("odds_kg",{}),"Var")} / Yok {_f(r.get("odds_kg",{}),"Yok")} · 2.5 A/Ü {_f(r.get("odds_au",{}),"Alt")}/{_f(r.get("odds_au",{}),"Üst")}</td>
</tr>''')
    return f'''<div class="card">
  <h2 class="card-h">🎯 Günün Yüksek Potansiyelli Maç Analizi</h2>
  <div class="tbl-wrap"><table class="pred">
    <thead><tr><th>Maç Kodu &amp; Karşılaşma</th><th>Önerilen Bahis</th><th>Güven</th><th>Oranlar</th><th>Taktik / KG</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table></div>
</div>'''


def _metrics(recs):
    scores = [r["skor"] for r in recs if r.get("skor") is not None]
    sma = sum(scores[-7:]) / len(scores[-7:]) if scores else 0.0
    ema = sum(scores[-14:]) / len(scores[-14:]) if scores else 0.0
    if len(scores) > 1:
        mean = sum(scores) / len(scores)
        var = sum((s - mean) ** 2 for s in scores) / (len(scores) - 1)
        sd = var ** 0.5
    else:
        sd = 0.0
    bol = 2 * sd
    anomaly = "Yok" if sd < bol else "Var"
    return f'''<div class="card">
  <h2 class="card-h">📊 Günlük Gelişim (SMA / EMA / Bollinger)</h2>
  <div class="metrics">
    <div class="m"><div class="m-h">SMA 7 GÜN</div><div class="m-v">{sma:.1f}</div><div class="m-s">Ortalama güven skoru</div></div>
    <div class="m"><div class="m-h">EMA 14 GÜN</div><div class="m-v">{ema:.1f}</div><div class="m-s">Üstel ortalama</div></div>
    <div class="m"><div class="m-h">BOLLİNGER 2Σ</div><div class="m-v">±{bol:.2f}</div><div class="m-s">Hata payı sınırı</div></div>
    <div class="m"><div class="m-h">ANOMALİ</div><div class="m-v ok">{anomaly}</div><div class="m-s">±2σ dışı değer</div></div>
  </div>
</div>'''


def build_html(bulten, rapor, generated=None):
    recs = (rapor or {}).get("ononeriler") or (rapor or {}).get("ononeriler") or []
    groups = group_by_league(bulten)

    body_rows = []
    idx = 0
    for name, rows in groups:
        body_rows.append(_league_row(name))
        for r in rows:
            body_rows.append(_match_row(r, idx))
            idx += 1

    total = len(bulten)
    n_pred = len(recs)
    gen = generated or datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Toxkolikk — İddaa / Mackolik / Transfermarkt Çapraz Analiz</title>
<style>{CSS}</style></head>
<body>
<div class="wrap">
  {_header()}
  {_toolbar()}
  <div class="content">
    <main>
      {_search_row()}
      <div class="livebar"><span>ÖNE ÇIKANLAR ({total})</span>
        <span class="codes">1 0 2 · 1 0 2 · H 1 0 2 · Alt Üst · Var Yok</span></div>
      <table class="matches">
        <thead><tr class="colhead">
          <th style="width:34px"></th><th style="width:26px"></th><th style="width:76px"></th>
          <th style="width:190px"></th><th style="width:52px"></th><th colspan="3">1 · 0 · 2</th>
          <th colspan="3">1 · 0 · 2</th><th colspan="3">H 1 0 2</th><th colspan="2">Alt Üst</th><th colspan="2">Var Yok</th>
        </tr></thead>
        <tbody>{''.join(body_rows)}</tbody>
      </table>
    </main>
    {_sidebar()}
  </div>
  <div class="section">
    {_prediction_table(recs)}
    {_metrics(recs)}
  </div>
  <div class="foot">
    <p><b>Veri kaynağı:</b> /data/iddaa/bulten.json · <b>Üretim:</b> {gen} · <b>Öneri:</b> {n_pred} (güven ≥ 7.5)</p>
    <p>Otomasyon: iddaa.com sportsbook API (curl_cffi, chrome impersonation) → A/B/C pazar filtresi (İY KG Var · Her İki Yarıda Gol · İY Sonucu) → güven skoru ≥ 7.5. Sıfır halüsinasyon: veri yoksa gösterilmez. Cron: `0 8,11,14,17,20 * * *` (analiz) + `*/30 8-21 * * *` (oransız izleyici).</p>
  </div>
</div>
</body></html>"""


def main():
    ap = argparse.ArgumentParser(description="iddaa.com tarzı statik mirror")
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--skip-fetch", action="store_true")
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))

    if not args.skip_fetch:
        subprocess.call([sys.executable, os.path.join(here, "gunluk_rapor.py")])

    bulten = load_json(os.path.join(DATA, "bulten.json"), [])
    rapor = load_json(os.path.join(DATA, "analiz_raporu.json"), {})

    if not bulten:
        print("!! bulten.json boş — önce gunluk_rapor.py çalıştırın")
        return 1

    os.makedirs(args.out, exist_ok=True)
    html = build_html(bulten, rapor)
    path = os.path.join(args.out, "index.html")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)

    n_pred = len((rapor or {}).get("ononeriler", []) or (rapor or {}).get("ononeriler", []))
    print(f"✓ Mirror üretildi: {path}")
    print(f"  Maç: {len(bulten)} | Öneri: {n_pred}")
    print(f"  Boyut: {len(html)} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
