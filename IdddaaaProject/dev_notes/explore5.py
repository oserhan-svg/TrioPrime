from curl_cffi import requests
import json
from collections import Counter

s = requests.Session(impersonate="chrome")
s.headers.update({"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36","Accept":"application/json","Origin":"https://www.iddaa.com","Referer":"https://www.iddaa.com/"})

d = s.get("https://sportsbookv2.iddaa.com/sportsbook/events?st=1&type=1&version=0&live=false", timeout=25).json()['data']
evs = d['events']
print("total:", len(evs))
# date distribution
dates = Counter()
for e in evs:
    dd = e.get('d')
    if dd:
        # d might be epoch ms
        try:
            from datetime import datetime
            dates[datetime.fromtimestamp(int(dd)/1000).strftime('%Y-%m-%d %H:%M')] += 1
        except: dates[str(dd)[:10]] += 1
    else:
        dates['NO_D'] += 1
print("\n=== tarih dağılımı (ilk 25) ===")
for k in sorted(dates)[:25]:
    print(f"  {k}: {dates[k]}")

print("\n=== Süper Lig eventi ===")
for e in evs:
    if e.get('ci') == 584:
        print(json.dumps(e, ensure_ascii=False)[:600])
