from curl_cffi import requests
import json

s = requests.Session(impersonate="chrome")
s.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Origin": "https://www.iddaa.com",
    "Referer": "https://www.iddaa.com/",
})
r = s.get("https://sportsbookv2.iddaa.com/sportsbook/events?st=1&type=0&version=0&live=true", timeout=25)
d = r.json()
print("top keys:", list(d.keys()))
data = d['data']
print("data keys:", list(data.keys()))
evs = data['events']
print("total events:", len(evs))
print("\n=== örnek event (keys) ===")
e = evs[0]
print(json.dumps(e, ensure_ascii=False, indent=1)[:1800])
