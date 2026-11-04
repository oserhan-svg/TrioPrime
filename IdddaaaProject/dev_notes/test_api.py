from curl_cffi import requests
import json

s = requests.Session(impersonate="chrome")
s.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Origin": "https://www.iddaa.com",
    "Referer": "https://www.iddaa.com/",
})

urls = [
    "https://sportsbookv2.iddaa.com/sportsbook/competitions",
    "https://sportsbookv2.iddaa.com/sportsbook/events?st=1&type=0&version=0&live=true",
    "https://sportsbookv2.iddaa.com/sportsbook/info",
]
for u in urls:
    try:
        r = s.get(u, timeout=25)
        print(f"{r.status_code}  {u}  len={len(r.text)}")
        if r.status_code == 200:
            print("   head:", r.text[:300].replace("\n"," "))
    except Exception as e:
        print("ERR", u, type(e).__name__, e)
