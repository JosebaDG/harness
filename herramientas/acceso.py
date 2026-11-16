#!/usr/bin/env python3
"""Acceso a GitHub por device flow (GitHub App). Nunca imprime el token.
  python3 acceso.py login <client_id>   -> imprime CODE XXXX-XXXX y espera en segundo plano
  python3 acceso.py estado              -> ok | pending | expired | error ...
  python3 acceso.py token               -> token válido (lo renueva); solo dentro de comandos
Guarda el token en ~/.config/equipo/token.json (chmod 600)."""
import json, os, sys, time, urllib.request, urllib.parse
D = os.path.expanduser("~/.config/equipo"); os.makedirs(D, mode=0o700, exist_ok=True)
TOK, EST = os.path.join(D, "token.json"), os.path.join(D, "login.status")
def post(u, d):
    r = urllib.request.Request(u, data=urllib.parse.urlencode(d).encode(), headers={"Accept": "application/json"})
    with urllib.request.urlopen(r, timeout=30) as x: return json.load(x)
def est(m): open(EST, "w").write(m + "\n")
def guarda(t):
    with os.fdopen(os.open(TOK, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w") as f: json.dump(t, f)
if sys.argv[1:2] == ["estado"]:
    print(open(EST).read().strip() if os.path.exists(EST) else "sin login"); sys.exit()
if sys.argv[1:2] == ["token"]:
    if not os.path.exists(TOK): sys.exit("SIN_TOKEN: haz login")
    t = json.load(open(TOK))
    # Sin expires_in o sin refresh_token el token no caduca (App con caducidad desmarcada): no se renueva.
    if "refresh_token" in t and "expires_in" in t and time.time() > t["obtained_at"] + t["expires_in"] - 300:
        n = post("https://github.com/login/oauth/access_token", {"client_id": t["client_id"],
                 "grant_type": "refresh_token", "refresh_token": t["refresh_token"]})
        if "access_token" not in n: sys.exit("REFRESH_FAILED: haz login otra vez")
        n["client_id"], n["obtained_at"] = t["client_id"], int(time.time()); guarda(n); t = n
    print(t["access_token"]); sys.exit()
if sys.argv[1:2] != ["login"] or len(sys.argv) < 3:
    sys.exit("Uso: python3 acceso.py login <client_id> | estado | token")
cid = sys.argv[2]
d = post("https://github.com/login/device/code", {"client_id": cid})
if "device_code" not in d: sys.exit("ERROR %s" % d)
print("CODE", d["user_code"], d["verification_uri"], "expira_en", d["expires_in"], flush=True); est("pending")
if os.fork(): sys.exit(0)
iv, fin = d.get("interval", 5), time.time() + d["expires_in"]
while time.time() < fin:
    time.sleep(iv)
    try:
        t = post("https://github.com/login/oauth/access_token", {"client_id": cid, "device_code": d["device_code"],
                 "grant_type": "urn:ietf:params:oauth:grant-type:device_code"})
    except Exception: continue
    if "access_token" in t:
        t["client_id"], t["obtained_at"] = cid, int(time.time()); guarda(t)
        est("ok"); sys.exit(0)
    if t.get("error") == "slow_down": iv += 5
    elif t.get("error") != "authorization_pending": est("error " + str(t.get("error"))); sys.exit(1)
est("expired")
