from curl_cffi import requests
import json
from collections import Counter, defaultdict

s = requests.Session(impersonate="chrome")
s.headers.update({"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36","Accept":"application/json","Origin":"https://www.iddaa.com","Referer":"https://www.iddaa.com/"})
d = s.get("https://sportsbookv2.iddaa.com/sportsbook/events?st=1&type=0&version=0&live=true", timeout=25).json()['data']
evs = d['events']

# Find Süper Lig events
sl = [e for e in evs if e.get('ci') == 584]
print("Süper Lig event sayısı:", len(sl))
for e in sl:
    print(f"  {e['hn']} vs {e['an']} | d={e.get('d')} | il={e.get('il')} | ci={e.get('ci')}")

# Market type distribution across all football events
print("\n=== Market t/st dağılımı (tüm eventler) ===")
cnt = defaultdict(Counter)
for e in evs:
    for m in e.get('m', []):
        cnt[m.get('t')][m.get('st')] += 1
for t in sorted(cnt, key=lambda x: str(x)):
    print(f"  t={t}: {dict(cnt[t])}")

# Champions League search
print("\n=== Şampiyonlar Ligi eventleri ===")
cl = [e for e in evs if e.get('ci') in (2,3,4,5,6,7,8,9,10,11,12,13,14,15)]
# Better: check competition names containing Şampiyon
rc = s.get("https://sportsbookv2.iddaa.com/sportsbook/competitions", timeout=25).json()['data']
print("Şampiyon Ligi komp:", [(c['i'],c['n']) for c in rc if 'Şampiyon' in c.get('n','') or 'Champions' in c.get('n','')])
