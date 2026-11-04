from curl_cffi import requests
import json

s = requests.Session(impersonate="chrome")
s.headers.update({"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36","Accept":"application/json","Origin":"https://www.iddaa.com","Referer":"https://www.iddaa.com/","Content-Type":"application/json"})

r = s.post("https://sportsbookv2.iddaa.com/sportsbook/markets_by_id", json={"eventId": 3225752}, timeout=20)
print("status:", r.status_code)
print("body:", r.text)
