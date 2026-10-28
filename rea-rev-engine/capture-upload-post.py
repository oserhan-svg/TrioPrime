#!/usr/bin/env python3
"""Capture upload POST via DevTools Protocol on page 7DE3A7ACE..."""
import websocket, json, urllib.request, time, sys

ws_url = "ws://127.0.0.1:9222/devtools/page/7DE3A7ACE7232E05AF18DC4DDF21A849"

def on_message(ws, msg):
    data = json.loads(msg)
    if isinstance(data, dict) and 'method' in data:
        m = data.get('method','')
        params = data.get('params',{})
        # Capture network events
        if 'Network' in m:
            print('NETWORK EVENT:', m, params)
            # Save to file
            with open('/home/rw/Projects/rea-rev-engine/upload-capture.log','a') as f:
                f.write(json.dumps(data)+'\n')
        # Capture upload requests
        if 'requestWillBeSent' in m:
            req = params.get('request',{})
            url = req.get('url','')
            if 'upload' in url.lower() or 'transform' in url.lower() or 'pixelbin' in url.lower():
                print('POSSIBLE UPLOAD POST:', url)
                with open('/home/rw/Projects/rea-rev-engine/upload-capture.log','a') as f:
                    f.write('POST_CANDIDATE:'+json.dumps(data)+'\n')
        # Print response
        if 'response' in str(data):
            print('RESPONSE:', data)

try:
    ws = websocket.create_connection(ws_url)
    ws.send(json.dumps({"id":1,"method":"Network.enable"}))
    ws.send(json.dumps({"id":2,"method":"Page.enable"}))
    ws.send(json.dumps({"id":3,"method":"Runtime.enable"}))
    print("Connected to DevTools. Listening for 10s...")
    ws.settimeout(10.0)
    start = time.time()
    # Listen briefly
    try:
        while time.time() - start < 10:
            msg = ws.recv()
            on_message(ws, msg)
    except websocket.WebSocketTimeoutException:
        pass
    ws.close()
    print("Done. Check /home/rw/Projects/rea-rev-engine/upload-capture.log")
except Exception as e:
    print("Connection error (expected if no upload triggered):", e)
