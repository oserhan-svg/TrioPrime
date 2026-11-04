from curl_cffi import requests
import json
from collections import Counter, defaultdict

s = requests.Session(impersonate="chrome")
s.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Origin": "https://www.iddaa.com",
    "Referer": "https://www.iddaa.com/",
})
r = s.get("https://sportsbookv2.iddaa.com/sportsbook/events?st=1&type=0&version=0&live=true", timeout=25)
d = r.json()['data']
print("data.sc type:", type(d['sc']), "len:", len(d['sc']) if hasattr(d['sc'],'__len__') else '')
print("data.rmi:", json.dumps(d['rmi'], ensure_ascii=False)[:300])

# Competition list
rc = s.get("https://sportsbookv2.iddaa.com/sportsbook/competitions", timeout=25)
comps = rc.json()['data']
print("\n=== Türk ligleri ===")
for c in comps:
    if 'Türk' in c.get('n','') or 'TUR' in str(c.get('cid','')).upper() or 'Süper' in c.get('n','') or '1. Lig' in c.get('n',''):
        print(" ", c.get('i'), c.get('cid'), c.get('n'), "| sport:", c.get('si'))

# Find Turkish Super Lig events
print("\n=== Süper Lig / ŞL eventleri (cid ile) ===")
evs = d['events']
# Let's see what competition field exists on events
print("event fields:", list(evs[0].keys()))
