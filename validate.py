"""Validate grants.json before publishing. Exit code 1 blocks the update.
Run: python3 validate.py"""
import json, re, sys
from datetime import date
d = json.load(open("grants.json"))
err = []
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LEVELS = {"Federal", "Provincial", "Municipal", "Foundation", "Corporate"}
REGIONS = {"Canada", "AB", "BC", "MB", "SK", "ON", "QC", "NS", "NB", "NL", "PE", "YT", "NT", "NU"}
if not ISO.match(d.get("verified", "")): err.append("verified must be YYYY-MM-DD")
P = d.get("programs", [])
if len(P) < 30: err.append(f"only {len(P)} programs; refusing to shrink the list this much")
names = set()
for i, g in enumerate(P):
    tag = f"[{i}] {g.get('n','?')}"
    for k in ("n", "f", "lv", "r", "fo", "amt", "w", "d", "el", "u"):
        if k not in g: err.append(f"{tag}: missing {k}")
    if g.get("lv") not in LEVELS: err.append(f"{tag}: bad level {g.get('lv')}")
    if g.get("r") not in REGIONS: err.append(f"{tag}: bad region {g.get('r')}")
    if not str(g.get("u", "")).startswith("https://"): err.append(f"{tag}: url must be https")
    if "—" in json.dumps(g, ensure_ascii=False): err.append(f"{tag}: contains an em dash (brand rule)")
    for w in g.get("w", []):
        if len(w) != 2: err.append(f"{tag}: window must be [opens, closes]"); continue
        o, c = w
        if o not in (None, "rolling") and not ISO.match(str(o)): err.append(f"{tag}: bad open date {o}")
        if not ISO.match(str(c)): err.append(f"{tag}: bad close date {c}")
    if g.get("n") in names: err.append(f"{tag}: duplicate name")
    names.add(g.get("n"))
d["count"] = len(P)
if err:
    print("\n".join(err)); sys.exit(1)
json.dump(d, open("grants.json", "w"), ensure_ascii=False, indent=1)
print(f"OK: {len(P)} programs, verified {d['verified']}")
