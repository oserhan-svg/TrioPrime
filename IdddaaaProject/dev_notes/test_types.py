from curl_cffi import requests
import json

s = requests.Session(impersonate="chrome")
s.headers.update({"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36","Accept":"application/json","Origin":"https://www.iddaa.com","Referer":"https://www.iddaa.com/"})

for t in [0,1,2,3,4,5,6,7,8]:
    u = f"https://sportsbookv2.iddaa.com/sportsbook/events?st=1&type={t}&version=0&live=false"
    try:
        r = s.get(u, timeout=20)
        if r.status_code != 200:
            print(f"type={t}: {r.status_code}")
            continue
        d = r.json().get('data', {})
        evs = d.get('events', [])
        withm = [e for e in evs if len(e.get('m',[]))>0]
        print(f"type={t}: events={len(evs)} with_markets={len(withm)}")
        if withm:
            e = withm[0]
            print(f"    ex: {e['hn']} vs {e['an']} markets={len(e['m'])}")
            for m in e['m'][:3]:
                print(f"      t={m['t']} st={m['st']} sov={m.get('sov')} outs={[ (o['n'],o['odd']) for o in m.get('o',[])][:4]}")
    except Exception as e:
        print(f"type={t}: ERR {e}")
