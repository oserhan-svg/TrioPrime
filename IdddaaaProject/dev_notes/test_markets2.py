from curl_cffi import requests
import json

s = requests.Session(impersonate="chrome")
s.headers.update({"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36","Accept":"application/json","Origin":"https://www.iddaa.com","Referer":"https://www.iddaa.com/","Content-Type":"application/json"})

eid = 3225752
tests = [
    ("https://sportsbookv2.iddaa.com/sportsbook/markets_by_id", {"eventId": eid}),
    ("https://sportsbookv2.iddaa.com/sportsbook/markets_by_id", {"id": eid}),
    ("https://sportsbookv2.iddaa.com/sportsbook/markets_by_id", {"eventIds": [eid]}),
    ("https://sportsbookv2.iddaa.com/sportsbook/markets_by_id", {"ids": [eid]}),
    ("https://sportsbookv2.iddaa.com/sportsbook/markets_by_id", [eid]),
]
for u, body in tests:
    try:
        r = s.post(u, json=body, timeout=20)
        print(f"{r.status_code}  body={json.dumps(body)[:50]}  len={len(r.text)}")
        if r.status_code == 200 and len(r.text) > 100:
            print("   head:", r.text[:300].replace("\n"," "))
    except Exception as e:
        print("ERR", e)
