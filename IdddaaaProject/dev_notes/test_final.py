from curl_cffi import requests
import json

s = requests.Session(impersonate="chrome")
s.headers.update({"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36","Accept":"application/json","Origin":"https://www.iddaa.com","Referer":"https://www.iddaa.com/"})
d = s.get("https://sportsbookv2.iddaa.com/sportsbook/events?st=1&type=0&version=0&live=false", timeout=25).json()['data']
evs = d['events']
print("total events:", len(evs))

sl = [e for e in evs if e.get('ci') == 584]
cl = [e for e in evs if e.get('ci') in (46194, 126)]
print(f"Süper Lig: {len(sl)} | Şampiyonlar Ligi: {len(cl)}")

for e in sl + cl:
    print(f"\n=== {e['hn']} vs {e['an']} (ci={e['ci']}) markets={len(e.get('m',[]))} ===")
    for m in e.get('m', []):
        outs = ", ".join(f"{o['n']}={o['odd']}" for o in m.get('o', [])[:6])
        print(f"  t={m['t']} st={m['st']} sov={m.get('sov')} -> {outs}")
