"""Quality gate. Cloudflare Pages runs this before every deploy (build command).
If any listing breaks a rule, the build fails and the previous version stays live."""
import json, re, sys, datetime, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "site", "data", "opportunities.json")

TYPES = {"research_stay","mobility","conference_travel","fieldwork","thesis_completion","small_grant"}
STATUS = {"open","upcoming","rolling","monitor","paused","closed"}
PAY = {"upfront","stipend","reimbursed","varies"}
VER = {"official","secondary","needs_check"}
RULE = {"any","developing","list","region"}
REQUIRED = ["id","name","provider","type","type_label","levels","fields","nat_rule","enrol_rule","host","amount",
            "covers","payment","membership","recurrence","window","months","next_deadline","status","status_label",
            "dev_priority","url","url_checked","verification","checked","notes"]

def main():
    errors = []
    try:
        data = json.load(open(PATH, encoding="utf-8"))
    except Exception as e:
        print(f"FAIL: {PATH} is not valid JSON: {e}"); return 1
    ops = data.get("opportunities")
    if not isinstance(ops, list) or len(ops) < 10:
        print("FAIL: opportunities list missing or suspiciously short"); return 1
    seen = set()
    for i, o in enumerate(ops):
        tag = o.get("id", f"#{i}")
        for k in REQUIRED:
            if k not in o: errors.append(f"{tag}: missing field '{k}'")
        if tag in seen: errors.append(f"{tag}: duplicate id")
        seen.add(tag)
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{2,80}", str(o.get("id",""))): errors.append(f"{tag}: id must be kebab-case")
        if o.get("type") not in TYPES: errors.append(f"{tag}: bad type {o.get('type')}")
        if o.get("status") not in STATUS: errors.append(f"{tag}: bad status {o.get('status')}")
        if o.get("payment") not in PAY: errors.append(f"{tag}: bad payment {o.get('payment')}")
        if o.get("verification") not in VER: errors.append(f"{tag}: bad verification {o.get('verification')}")
        lv = o.get("levels") or []
        if not lv or any(x not in ("MSc","PhD") for x in lv): errors.append(f"{tag}: levels must be MSc and/or PhD")
        for r in ("nat_rule","enrol_rule"):
            if not isinstance(o.get(r), dict) or o[r].get("type") not in RULE: errors.append(f"{tag}: bad {r}")
        if any((not isinstance(m,int)) or m < 1 or m > 12 for m in o.get("months") or []): errors.append(f"{tag}: months must be 1-12")
        nd = o.get("next_deadline")
        if nd:
            try: datetime.date.fromisoformat(nd)
            except ValueError: errors.append(f"{tag}: next_deadline not YYYY-MM-DD")
        url = o.get("url") or ""
        if url and not url.startswith("https://") and not url.startswith("http://"): errors.append(f"{tag}: url must be http(s)")
        if o.get("verification") == "official" and not url: errors.append(f"{tag}: official listing needs a url")
        try: datetime.date.fromisoformat(o.get("checked",""))
        except ValueError: errors.append(f"{tag}: checked not YYYY-MM-DD")
    fp = os.path.join(ROOT, "site", "data", "featured.json")
    if os.path.exists(fp):
        try:
            f = json.load(open(fp, encoding="utf-8"))
            if f.get("id") and f["id"] not in seen: errors.append(f"featured.json: id '{f['id']}' is not in the listings")
            if f.get("date"): datetime.date.fromisoformat(f["date"])
        except Exception as e:
            errors.append(f"featured.json invalid: {e}")
    sp = os.path.join(ROOT, "site", "data", "scholarships.json")
    if os.path.exists(sp):
        try:
            sd = json.load(open(sp, encoding="utf-8"))
            for i, p in enumerate(sd.get("posts", [])):
                for k in ("date", "title", "provider", "destination", "level", "funding", "eligible", "deadline"):
                    if not p.get(k): errors.append(f"scholarships.json post {i}: missing {k}")
                for k in ("date", "deadline", "verified_on"):
                    if p.get(k): datetime.date.fromisoformat(p[k])
                if "apply_url" in p or "http" in json.dumps({k: v for k, v in p.items()}):
                    errors.append(f"scholarships.json post {i}: application links must stay in the WhatsApp Channel, not on the site")
            if len(sd.get("posts", [])) > 120: errors.append("scholarships.json: keep at most 120 posts")
        except Exception as e:
            errors.append(f"scholarships.json invalid: {e}")
    if errors:
        print(f"FAIL: {len(errors)} problem(s)"); print("\n".join(errors[:100])); return 1
    print(f"OK: {len(ops)} listings valid")
    return 0

if __name__ == "__main__":
    sys.exit(main())
