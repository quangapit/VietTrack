#!/usr/bin/env python3
import hashlib
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

API = "https://tramavandon.com/api/{}.php"


CARRIERS = [
    ("spx", re.compile(r"^SPXVN\d{8,}[A-Z]?$"), False),
    ("lex", re.compile(r"^LEX[A-Z0-9]{8,}$"), False),
    ("ghn", re.compile(r"^(GHN-?[A-Z0-9]{6,}|G[A-Z0-9]{7})$"), True),
    ("jtexpress", re.compile(r"^JT\d{10,}$"), True),
]

RENDERED = [
    ("vnPost", re.compile(r"^[A-Z]{2}\d{9}VN$"), "https://ipostal.vnpost.vn/tra-cuu-buu-gui"),
    ("ViettelPost", re.compile(r"^P[A-Z0-9]{9,}$"),
     "https://viettelpost.vn/viettelpost-iframe/tra-cuu-hanh-trinh-don-hang-v3-recaptcha?orderString={}"),
    ("Ninja Van", re.compile(r"^(NV|NJV)[A-Z0-9]{8,}$"),
     "https://www.ninjavan.co/vi-vn/tracking?tracking_number={}"),
    ("GHTK", re.compile(r"^[A-Z0-9]{8,}$"), "https://i.ghtk.vn/{}"),
]
NO_TRACKING = ("TikTok Express", re.compile(r"^TK[A-Z0-9]{8,}$|^TTS[A-Z0-9]{8,}$"))


TIME_KEYS = ("actual_time", "time", "log_time", "action_time", "datetime",
             "updated_time", "created_time", "create_time", "created_date",
             "updated_date", "timestamp")
DESC_KEYS = ("buyer_description", "description", "status_name", "status", "content", "note", "name")
ADDR_KEYS = ("full_address", "address", "warehouse_name", "location_name")

SPX_URL = "https://spx.vn/shipment/order/open/order/get_order_info?spx_tn=%s&language_code=vi"
LEX_URL = "https://lex.vn/api/get_package_history"
GHN_URL = "https://fe-online-gateway.ghn.vn/order-tracking/public-api/client/tracking-logs"
JT_URL = "https://jtexpress.vn/tracking?type=track&billcode=%s"


def _req(url, body=None, headers=None):
    h = {"User-Agent": "Mozilla/5.0"}
    h.update(headers or {})
    data = json.dumps(body).encode() if body is not None else None
    if data:
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=h, method="POST" if data else "GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.read().decode("utf-8", "replace")


def _json(text):
    try:
        return json.loads(text)
    except ValueError:
        return {}


def _ghn_events(code, phone=None):
    # phone_verify = sha256("<MÃ ĐƠN HOA>|<4 số cuối SĐT>")
    verify = hashlib.sha256(("%s|%s" % (code.strip().upper(), phone)).encode()).hexdigest()
    return events_of(_json(_req(GHN_URL, {"order_code": code, "phone_verify": verify})))


def _jt_events(code, phone=None):
    html = _req(JT_URL % urllib.parse.quote(code))
    m = re.search(r'class="result-tracking[^"]*"[^>]*>(.*?)<div class="result-office', html, re.S)
    block = m.group(1) if m else ""
    if not block or "Không tìm thấy dữ liệu về vận đơn" in block:
        return []
    lines = [l.strip() for l in re.sub(r"<[^>]+>", "\n", block).splitlines() if l.strip()]
    return [(0, "", l, "") for l in lines]


DIRECT = {
    "spx": lambda code, phone=None: events_of(_json(_req(SPX_URL % urllib.parse.quote(code)))),
    "lex": lambda code, phone=None: events_of(_json(_req(LEX_URL, {"trackingNumber": code},
                                                               {"Origin": "https://lex.vn",
                                                                "Referer": "https://lex.vn/"}))),
    "ghn": _ghn_events,
    "jtexpress": _jt_events,
}


def call(carrier, code, phone=None):
    body = {"tracking_id": code}
    if phone:
        body["tracking_phone"] = phone
    req = urllib.request.Request(
        API.format(carrier),
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
            "Origin": "https://tramavandon.com",
            "Referer": "https://tramavandon.com/%s/" % carrier,
            "User-Agent": "Mozilla/5.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:  
        return json.loads(e.read().decode() or "{}")


def events_of(res):

    data = res.get("data") or {}
    raw = (data.get("sls_tracking_info") or {}).get("records") or data.get("events") or res.get("events") or []
    if not raw:
        raw = [d for d in _walk(res) if any(k in d for k in TIME_KEYS) and any(k in d for k in DESC_KEYS)]
    out = []
    for e in raw:
        if e.get("actual_time"):
            when = datetime.fromtimestamp(e["actual_time"]).strftime("%H:%M %d/%m/%Y")
        else:
            t = next((e[k] for k in TIME_KEYS if e.get(k)), "")
            when = ("%s %s" % (t, e.get("date") or "")).strip()
        desc = ""
        for k in DESC_KEYS:
            if e.get(k):
                desc = str(e[k]).replace("╓", " / ")
                break
        addr = ""
        for k in ADDR_KEYS:
            v = e.get(k)
            if isinstance(v, dict):
                v = v.get("full_address") or v.get("location_name")
            if v:
                addr = v
                break
        out.append((e.get("actual_time") or 0, when, desc, addr))
    out.sort(key=lambda x: x[0], reverse=True)  
    return out


def _walk(obj):
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from _walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk(v)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if "--track" in sys.argv:
        print("Hãng vận chuyển được hỗ trợ:")
        for name, _, _ in CARRIERS:
            print("  " + name.upper())
        for name, _, _ in RENDERED:
            print("  " + name)
        print("  " + NO_TRACKING[0])
        return
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    argv = [a for a in sys.argv[1:] if a != "--open"]
    do_open = "--open" in sys.argv
    code = argv[0].strip().upper()
    phone = argv[1] if len(argv) > 1 else None

    specific = NO_TRACKING[1].match(code) or any(p.match(code) for _, p, _ in RENDERED[:-1])
    matched = [c for c, pat, _ in CARRIERS if pat.match(code)]
    for carrier in [] if specific else (matched or [c for c, _, _ in CARRIERS]):
        events, res, err = [], {}, None
        try:
            events = DIRECT[carrier](code, phone)
        except Exception as e:
            err = e
        if not events:
            try:
                res = call(carrier, code, phone) 
                events = events_of(res)
            except Exception as e:
                err = err or e
        if not events:
            if err and not res:
                print("[%s] lỗi: %s" % (carrier, err))
            else:
                print("[%s] %s" % (carrier, res.get("message") or "không có dữ liệu"))
            if not phone and carrier in ("ghn", "jtexpress"):
                print("[%s] thử lại kèm 4 số cuối SĐT: python track.py %s 1234" % (carrier, code))
            continue

        order = res.get("order") or (res.get("data") or {}).get("order_info") or {}
        status = order.get("status_name") or order.get("tracking_code_group_name") or events[0][2]
        print("Hãng: %s | Mã: %s\nTrạng thái: %s\n" % (carrier.upper(), code, status))
        for _, when, desc, addr in events:
            print("%s  %s" % (when, desc))
            if addr:
                print("   " + addr)
        return

    if NO_TRACKING[1].match(code):
        sys.exit("%s: hãng chưa có kênh tra cứu công khai, không tra được." % NO_TRACKING[0])
    hits = [(name, url) for name, pat, url in RENDERED if pat.match(code)]
    if matched: 
        hits = [h for h in hits if h[0] != "GHTK"]
    if hits:
        name, url = hits[0]
        url = url.format(code)
        print("%s: trang tra cứu cần reCAPTCHA/JS, mở link sau:\n%s" % (name, url))
        if do_open:
            import webbrowser

            webbrowser.open(url)
        return
    sys.exit("Không tra được vận đơn này.")


if __name__ == "__main__":
    main()

