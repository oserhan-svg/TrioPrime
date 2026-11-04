from curl_cffi import requests
import json

s = requests.Session(impersonate="chrome")
s.headers.update({"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36","Accept":"application/json","Origin":"https://www.iddaa.com","Referer":"https://www.iddaa.com/"})

variants = [
    "https://sportsbookv2.iddaa.com/sportsbook/events?st=1&type=0&version=0&live=false",
    "https://sportsbookv2.iddaa.com/sportsbook/events?st=1&type=1&version=0&live=false",
    "https://sportsbookv2.iddaa.com/sportsbook/events?st=1&type=0&version=0",
]
for u in variants:
    r = s.get(u, timeout=25)
    try:
        d = r.json().get('data', {})
        evs = d.get('events', [])
        sl = [e for e in evs if e.get('ci') == 584]
        cl = [e for e in evs if e.get('ci') in (46194, 126, 2074)]
        print(f"{r.status_code} {u.split('?')[1]} -> events={len(evs)} SL={len(sl)} CL={len(cl)}")
    except Exception as e:
        print(f"{r.status_code} {u.split('?')[1]} -> ERR {e}")
