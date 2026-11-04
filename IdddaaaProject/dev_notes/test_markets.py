from curl_cffi import requests
import json

s = requests.Session(impersonate="chrome")
s.headers.update({"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36","Accept":"application/json","Origin":"https://www.iddaa.com","Referer":"https://www.iddaa.com/"})

# Get CL event IDs
d = s.get("https://sportsbookv2.iddaa.com/sportsbook/events?st=1&type=1&version=0&live=false", timeout=25).json()['data']
evs = d['events']
cl = [e for e in evs if e.get('ci') in (46194, 126)]
eid = cl[0]['i']
print("test event:", cl[0]['hn'], "vs", cl[0]['an'], "id:", eid)

tests = [
    f"https://sportsbookv2.iddaa.com/sportsbook/markets_by_id?eventId={eid}",
    f"https://sportsbookv2.iddaa.com/sportsbook/markets_by_id?id={eid}",
    f"https://sportsbookv2.iddaa.com/sportsbook/markets_by_id?eventIds={eid}",
    f"https://sportsbookv2.iddaa.com/sportsbook/markets_by_id?ids={eid}",
]
for u in tests:
    r = s.get(u, timeout=20)
    print(f"{r.status_code}  {u.split('?')[1]}  len={len(r.text)}")
    if r.status_code == 200 and len(r.text) > 100:
        print("   head:", r.text[:250].replace("\n"," "))
