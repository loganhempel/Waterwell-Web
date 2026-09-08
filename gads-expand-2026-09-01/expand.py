#!/usr/bin/env python3
"""Waterwell Google Ads — 1 Sep 2026 keyword expansion.

Extends the 22 Aug build (does NOT rebuild it). Adds only terms that phrase
match cannot already reach: shorter root phrases, different head-words, and
themes the website actually sells. Validates every addition against the ad
group's own negatives and against the existing term set for that geo.

Emits two CSVs, one per geo, for import as new tabs on the canonical sheet.
"""
import csv, json, os, sys
import brief, copy as copymod

# Kohei, 20 Jul, five separate comments on the Fatigue and Hormones ad groups:
# "not skin specific" / "Not skin related". The site leads on "Skin conditions,
# treated at the root", but it does carry four whole-body condition pages. The
# scope question is HIS to answer and is still open. Flip this to True to drop
# the whole-body groups entirely; leaving it False keeps them, flagged.
SKIN_ONLY = True   # Logan, 1 Sep: launch skin-only. Kohei flagged whole-body 5x.
WHOLE_BODY = ("Gut & Digestive Health","Hormones & Women's Health","Fatigue & Energy",
              "Stress & Sleep","Gut & Digestive Health AU","Hormones & Women's Health AU",
              "Fatigue & Energy AU")

HOME = {"NZ": "https://waterwellclinic.com/nz", "AU": "https://waterwellclinic.com/au"}

SRC = os.path.expanduser("~/Client Work/Waterwell/gads-build-2026-08-22/waterwell-2026-08-22.json")
OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- additions
# Grounded in waterwellclinic.com: 6 skin + 4 whole-body condition pages,
# three named services (naturopathic consultation, functional tests, herbal
# medicine), free 15-min discovery session, fully online, adults + children.
ADD = {
 "Brand - Waterwell": [
   "kohei naturopath","kohei iguchi clinic","waterwell skin clinic",
   "waterwell clinic booking","waterwell clinic consultation"],

 "Online Naturopath Consult": [
   # shorter roots + distinct head-words (biggest legitimate reach lever)
   "naturopath consultation nz","naturopathic doctor nz","naturopathic practitioner nz",
   "natural medicine practitioner nz","naturopathic consultation","naturopath cost nz",
   "naturopath prices nz","naturopath consultation cost","affordable naturopath nz",
   "speak to a naturopath online","talk to a naturopath online","consult a naturopath online",
   "book a naturopath consultation","naturopath discovery call","naturopath second opinion",
   # adults AND children — the site says so explicitly
   "family naturopath nz","naturopath for kids nz","childrens naturopath nz",
   "paediatric naturopath nz",
   # the three named services
   "functional testing naturopath nz","functional medicine testing nz",
   "naturopath health plan nz"],

 "General Naturopathy": [
   # cities the build did not cover (each city is its own phrase = real reach)
   "naturopath whangarei","naturopath new plymouth","naturopath whanganui",
   "naturopath gisborne","naturopath taupo","naturopath queenstown","naturopath timaru",
   "naturopath blenheim","naturopath masterton","naturopath hastings",
   "naturopath lower hutt","naturopath porirua","naturopath kapiti","naturopath north shore",
   "naturopath hawkes bay","naturopath bay of plenty","naturopath waikato","naturopath otago",
   # head-word variants
   "naturopathy nz","naturopathic medicine nz","natural therapies nz","holistic health nz"],

 "Gut & Digestive Health": [
   "naturopath for gas and bloating","naturopath for stomach issues","naturopath for gut pain",
   "naturopath for diarrhoea","naturopath for gluten intolerance",
   "naturopath for histamine intolerance","naturopath for candida","sibo testing nz",
   "candida naturopath nz","microbiome naturopath nz","gut healing naturopath nz",
   "digestive naturopath nz","gut health plan nz"],

 "Hormones & Women's Health": [
   # shorter roots of terms already present (phrase match is order/length sensitive)
   "naturopath for endometriosis","naturopath for fertility","naturopath for perimenopause",
   "naturopath for thyroid","naturopath for hormonal imbalance","naturopath for heavy periods",
   "naturopath for painful periods","naturopath for period pain","womens health naturopath nz",
   "naturopath for hypothyroid","naturopath for cycle health"],

 "Fatigue & Energy": [
   "naturopath for low energy","naturopath for chronic fatigue","naturopath for adrenal fatigue",
   "naturopath for iron deficiency","naturopath for low iron","energy naturopath nz",
   "naturopath for run down","naturopath for no energy"],

 "Stress & Sleep": [
   "naturopath for insomnia","naturopath for poor sleep","naturopath for restless sleep",
   "natural sleep support","sleep naturopath nz","naturopath for burnout and stress",
   "naturopath for cortisol","herbal support for sleep nz"],

 "Eczema": [
   "eczema naturopath","eczema specialist nz","eczema help nz","eczema treatment nz",
   "dyshidrotic eczema naturopath","hand eczema naturopath","scalp eczema naturopath",
   "eczema in children naturopath","toddler eczema naturopath","severe eczema naturopath",
   "chronic eczema naturopath","eczema and food naturopath","eczema diet plan nz",
   "herbal medicine for eczema nz"],

 "Topical Steroid Withdrawal": [
   "naturopath for tsw","tsw help nz","tsw specialist nz","steroid withdrawal naturopath",
   "coming off steroid cream","red skin syndrome","tsw diet naturopath","tsw skin support"],

 "Psoriasis": [
   "psoriasis naturopath","psoriasis help nz","psoriasis treatment nz","psoriasis specialist nz",
   "naturopath for scalp psoriasis","inverse psoriasis naturopath","nail psoriasis naturopath",
   "psoriasis diet plan nz","herbal medicine for psoriasis nz"],

 "Acne": [
   "acne naturopath","acne help nz","acne treatment nz","acne specialist nz",
   "naturopath for teenage acne","naturopath for cystic acne","back acne naturopath",
   "chin acne naturopath","acne diet plan nz","herbal medicine for acne nz"],

 "Rosacea": [
   "rosacea naturopath","rosacea help nz","rosacea treatment nz","rosacea specialist nz",
   "naturopath for facial redness","rosacea diet plan nz","flushing naturopath nz",
   "herbal medicine for rosacea nz"],

 "Skin Infections": [
   "skin infection naturopath","naturopath for hives","hives naturopath nz",
   "recurring hives naturopath","chronic urticaria naturopath nz","naturopath for itchy skin",
   "itchy skin naturopath nz","fungal skin naturopath nz","naturopath for folliculitis"],

 # ---- AU ----
 "Online Naturopath Consult AU": [
   "naturopath consultation","naturopathic consultation australia",
   "naturopathic practitioner australia","naturopathic doctor australia",
   "natural medicine practitioner australia","naturopath cost australia",
   "naturopath prices australia","affordable naturopath australia",
   "speak to a naturopath online","talk to a naturopath online",
   "consult a naturopath online","book a naturopath consultation",
   "naturopath discovery call","naturopath appointment australia",
   "family naturopath australia","naturopath for kids australia",
   "childrens naturopath australia","paediatric naturopath australia",
   "functional testing naturopath australia","functional medicine testing australia"],

 "General Naturopathy AU": [
   "naturopath newcastle","naturopath wollongong","naturopath sunshine coast",
   "naturopath geelong","naturopath townsville","naturopath cairns","naturopath toowoomba",
   "naturopath ballarat","naturopath bendigo","naturopath central coast","naturopath byron bay",
   "naturopath launceston","naturopath nsw","naturopath victoria","naturopath queensland",
   "naturopathy australia","naturopathic medicine australia","natural therapies australia",
   "holistic health australia"],

 "Gut & Digestive Health AU": [
   "naturopath for sibo australia","sibo naturopath","candida naturopath australia",
   "naturopath for stomach issues","naturopath for gas and bloating","naturopath for gut pain",
   "naturopath for diarrhoea","naturopath for gluten intolerance",
   "naturopath for histamine intolerance","microbiome testing australia",
   "stool testing naturopath australia","gut healing naturopath australia",
   "digestive naturopath australia"],

 "Hormones & Women's Health AU": [
   "naturopath for endometriosis australia","naturopath for fertility australia",
   "naturopath for menopause australia","naturopath for thyroid australia",
   "womens health naturopath australia","naturopath for hormonal imbalance",
   "naturopath for heavy periods","naturopath for painful periods",
   "hormone testing australia","naturopath for postnatal recovery australia"],

 "Fatigue & Energy AU": [
   "naturopath for chronic fatigue australia","naturopath for low energy australia",
   "naturopath for adrenal fatigue","naturopath for brain fog australia",
   "naturopath for iron deficiency","naturopath for low iron","energy naturopath australia",
   "chronic fatigue naturopath","naturopath for no energy"],

 "Eczema AU": [
   "eczema specialist australia","eczema help australia","eczema treatment australia",
   "hand eczema naturopath","dyshidrotic eczema naturopath","scalp eczema naturopath",
   "eczema in children naturopath","toddler eczema naturopath","baby eczema naturopath australia",
   "childhood eczema naturopath australia","severe eczema naturopath",
   "eczema diet naturopath australia","herbal medicine for eczema"],

 "TSW AU": [
   "naturopath for tsw australia","tsw help australia","tsw specialist australia",
   "steroid withdrawal naturopath","coming off steroid cream","red skin syndrome",
   "tsw diet naturopath","tsw skin support"],

 "Psoriasis AU": [
   "psoriasis naturopath","psoriasis help australia","psoriasis treatment australia",
   "psoriasis specialist australia","psoriasis diet naturopath","psoriasis gut health naturopath",
   "plaque psoriasis naturopath","guttate psoriasis naturopath","psoriasis trigger naturopath",
   "naturopath for scalp psoriasis","why does my psoriasis flare up",
   "herbal medicine for psoriasis"],

 "Acne AU": [
   "acne naturopath","acne help australia","acne treatment australia","acne specialist australia",
   "acne diet naturopath","acne gut health naturopath","back acne naturopath",
   "teenage acne naturopath","pcos acne naturopath","period acne naturopath",
   "naturopath for cystic acne","why wont my acne clear up","herbal medicine for acne"],

 "Rosacea AU": [
   "rosacea naturopath","rosacea help australia","rosacea treatment australia",
   "rosacea specialist australia","rosacea diet naturopath","rosacea gut health naturopath",
   "rosacea immune naturopath","naturopath for facial redness",
   "what triggers rosacea flare ups","herbal medicine for rosacea"],

 "Skin Infections AU": [
   "skin infection naturopath","naturopath for hives","hives naturopath australia",
   "recurring boils naturopath","fungal skin naturopath","naturopath for folliculitis",
   "naturopath for itchy skin","itchy skin naturopath australia","staph skin naturopath",
   "why do i keep getting skin infections"],
}

# Terms that MOVE into the new Herbal Medicine groups (removed from their old
# group so the account does not bid against itself).
MOVE_TO_HERBAL = {
  "NZ": ["online herbalist","online medical herbalist","online herbal medicine consultation",
         "medical herbalist nz"],
  "AU": [],
}

HERB_NEG = ["free","jobs","job","career","careers","course","courses","class","classes",
 "training","become a herbalist","school","degree","diploma","certificate","university",
 "salary","wage","what is","definition","meaning","wikipedia","wiki","reddit","forum","quora",
 "pdf","buy herbs","buy herbal","herbal supplements","herbal tea","herbal tincture","shop",
 "stockist","wholesale","supplier","dispensary","cure","detox","cleanse","near me",
 "doctor appointment","see a doctor","find a doctor","pharmacy","chemist","prescription"]

HERBAL = {
 "NZ": {
  "campaign":"WW | NZ | Online Naturopath",
  "name":"Herbal Medicine","theme":"Medical-herbalist head-term (a named service on site)",
  "final_url":"https://waterwellclinic.com/nz",
  "terms":["medical herbalist","medical herbalist nz","online medical herbalist","herbalist nz",
   "online herbalist","herbal medicine nz","herbal medicine consultation",
   "online herbal medicine consultation","herbalist consultation nz",
   "western herbal medicine nz","herbal medicine practitioner nz",
   "registered medical herbalist nz","qualified herbalist nz","herbalist for skin conditions",
   "herbal medicine for skin nz","prescribed herbal medicine nz","custom herbal formula nz",
   "herbal medicine online nz"],
  "negatives": HERB_NEG + ["australia","sydney","melbourne","brisbane","perth"],
  "rsa":{"headlines":["Medical Herbalist NZ","Online Medical Herbalist","Herbal Medicine Consultation",
    "Individually Prescribed Herbs","Herbal Formulas, Made For You","Consults By Secure Video",
    "10+ Years In Practice","A Decade Of Herbal Practice","Herbal Medicine, NZ-Wide",
    "Works Alongside Your GP","Free 15-Min Discovery Call","Book A Herbal Consultation",
    "Herbs Chosen For Your Case","Adjusted As Your Body Responds","Book Your Herbal Consult"],
   "descriptions":[
    "Individually prescribed herbal formulas, chosen for your case, not off a shelf.",
    "Kohei Iguchi, BNatMed, BSc. More than ten years prescribing herbal medicine.",
    "Free 15-minute call first, or book a full consultation. By secure video, NZ-wide.",
    "Works alongside your GP and current medication, this adds to your care, not against it."],
   "paths":["herbal","medicine"],
   "pinning_notes":"Pos1 pin: 'Medical Herbalist NZ'. Rest unpinned."}},
 "AU": {
  "campaign":"WW | AU | Online Naturopath",
  "name":"Herbal Medicine AU","theme":"Medical-herbalist head-term (a named service on site)",
  "final_url":"https://waterwellclinic.com/au",
  "terms":["medical herbalist","medical herbalist australia","online medical herbalist",
   "herbalist australia","online herbalist","herbal medicine australia",
   "herbal medicine consultation","online herbal medicine consultation",
   "herbalist consultation australia","western herbal medicine australia",
   "herbal medicine practitioner australia","qualified herbalist australia",
   "registered herbalist australia","herbalist for skin conditions",
   "herbal medicine for skin","herbal medicine online australia"],
  "negatives": HERB_NEG + ["nz","new zealand","auckland","wellington","hamilton","christchurch",
   "medicare","bulk billing","rebate","health fund"],
  "rsa":{"headlines":["Medical Herbalist Australia","Online Medical Herbalist",
    "Herbal Medicine Consultation","Individually Prescribed Herbs","Herbal Formulas, Made For You",
    "Consults By Secure Video","10+ Years In Practice","A Decade Of Herbal Practice",
    "Herbal Medicine, AU-Wide","Works With Your Existing Care","Free 15-Min Discovery Chat",
    "Book A Herbal Consultation","Herbs Chosen For Your Case","Adjusted As Your Body Responds",
    "Book Your Herbal Consult"],
   "descriptions":[
    "Individually prescribed herbal formulas, chosen for your case, not off a shelf.",
    "Kohei Iguchi, BNatMed, BSc. More than ten years prescribing herbal medicine.",
    "A free 15-minute chat first, or book a full consultation, by secure video.",
    "Works alongside your existing GP care. A root-cause approach to your health."],
   "paths":["herbal","australia"],
   "pinning_notes":"Pos1 pin: 'Medical Herbalist Australia'. Rest unpinned."}},
}

# Kohei, 20 Jul (comment still OPEN on the sheet): do not emphasise holding both
# naturopathy and herbal-medicine training. This headline still did.
HEADLINE_FIX = {("Eczema","Two Qualifications, One Visit"): "Herbal Formulas, Made For You"}

# ---------------------------------------------------------------- validation
def blocked_by(term, negatives):
    """A phrase-match negative blocks the term if it appears as a word-run."""
    t = f" {term} "
    return [n for n in negatives if f" {n} " in t]

def geo_of(campaign_name):
    return "AU" if "| AU |" in campaign_name else "NZ"

# A removed Google Ads campaign can never be edited or reactivated, and Editor
# matches imports on campaign NAME. The legacy account held a campaign called
# "WW | NZ | Brand"; when that was removed and this build imported, Editor merged
# the new Brand campaign into the removed one and every Brand keyword became
# uneditable. Renaming ours makes the collision impossible.
RENAME = {"WW | NZ | Brand": "WW | NZ | Brand 2026"}

def main():
    d = json.load(open(SRC))
    for cp in d["campaigns"]:
        if cp["name"] in RENAME:
            cp["name"] = RENAME[cp["name"]]
    report = {"added":0,"rejected":[],"moved":0}

    # index existing terms per geo
    seen = {"NZ":set(),"AU":set()}
    for cp in d["campaigns"]:
        g = geo_of(cp["name"])
        for ag in cp["ad_groups"]:
            for k in ag["keywords"]:
                seen[g].add(k["keyword"])

    # 1. move herbalist terms out of their old groups
    for cp in d["campaigns"]:
        g = geo_of(cp["name"])
        for ag in cp["ad_groups"]:
            mv = set(MOVE_TO_HERBAL[g])
            before = len(ag["keywords"])
            ag["keywords"] = [k for k in ag["keywords"] if k["keyword"] not in mv]
            report["moved"] += (before - len(ag["keywords"]))//2

    # 2. apply the headline fix Kohei asked for
    for cp in d["campaigns"]:
        for ag in cp["ad_groups"]:
            hs = ag["rsa"]["headlines"]
            for i,h in enumerate(hs):
                if (ag["name"], h) in HEADLINE_FIX:
                    hs[i] = HEADLINE_FIX[(ag["name"], h)]
                    print(f"  headline fixed  {ag['name']}: {h!r} -> {hs[i]!r}")

    # 3. add the new groups
    for g, spec in HERBAL.items():
        cp = next(c for c in d["campaigns"] if c["name"] == spec["campaign"])
        kws = []
        for t in spec["terms"]:
            bad = blocked_by(t, spec["negatives"])
            if bad:
                report["rejected"].append((spec["name"], t, "self-blocked by "+", ".join(bad)))
                continue
            if t in seen[g] and t not in MOVE_TO_HERBAL[g]:
                report["rejected"].append((spec["name"], t, "already live in this geo"))
                continue
            seen[g].add(t)
            kws += [{"keyword":t,"match":"phrase"},{"keyword":t,"match":"exact"}]
        cp["ad_groups"].append({"name":spec["name"],"theme":spec["theme"],
            "final_url":spec["final_url"],"keywords":kws,
            "negatives":spec["negatives"],"rsa":spec["rsa"]})
        report["added"] += len(kws)//2

    # 4. extend existing groups
    for cp in d["campaigns"]:
        g = geo_of(cp["name"])
        for ag in cp["ad_groups"]:
            for t in ADD.get(ag["name"], []):
                bad = blocked_by(t, ag["negatives"])
                if bad:
                    report["rejected"].append((ag["name"], t, "self-blocked by "+", ".join(bad)))
                    continue
                if t in seen[g]:
                    report["rejected"].append((ag["name"], t, "already live in this geo"))
                    continue
                seen[g].add(t)
                ag["keywords"] += [{"keyword":t,"match":"phrase"},{"keyword":t,"match":"exact"}]
                report["added"] += 1

    # 4b. short head terms — the reach lever
    for cp in d["campaigns"]:
        g = geo_of(cp["name"])
        for ag in cp["ad_groups"]:
            for t in brief.SHORT.get(ag["name"], []):
                bad = blocked_by(t, ag["negatives"])
                if bad:
                    report["rejected"].append((ag["name"], t, "self-blocked by "+", ".join(bad)))
                    continue
                if t in seen[g]:
                    report["rejected"].append((ag["name"], t, "already live in this geo"))
                    continue
                seen[g].add(t)
                ag["keywords"] += [{"keyword":t,"match":"phrase"},{"keyword":t,"match":"exact"}]
                report["added"] += 1; report["short"] = report.get("short",0)+1

    # 4c. drop the dead long-tail
    pr = set(brief.PRUNE) | {"naturopath perth"}
    for cp in d["campaigns"]:
        g = geo_of(cp["name"])
        for ag in cp["ad_groups"]:
            hit = {k["keyword"] for k in ag["keywords"]} & pr
            if hit:
                ag["keywords"] = [k for k in ag["keywords"] if k["keyword"] not in pr]
                report["pruned"] = report.get("pruned",0) + len(hit)
                for t in hit: seen[g].discard(t)

    # 4d. new RSA copy (problem -> root cause -> proof -> format -> offer)
    newcopy = copymod.all_copy()
    for cp in d["campaigns"]:
        for ag in cp["ad_groups"]:
            nc = newcopy.get(ag["name"])
            if nc:
                ag["rsa"] = {"headlines": nc["headlines"], "descriptions": nc["descriptions"],
                             "paths": ag["rsa"]["paths"], "pinning_notes": nc["pinning_notes"]}

    # 4d-bis. ALL ads land on the region home page — Logan's call, 8 Sep 2026.
    # The per-condition pages (/conditions/eczema, /tsw, ...) read as a blog, not
    # as a clinic that takes bookings, so every ad group now points at the region
    # home. Region, not the global "/", because /nz and /au carry different
    # compliance wording and the campaigns are geo-split — an AU click must not
    # land on the NZ page. Display paths are unchanged: they still carry the
    # condition into the visible URL, and the home page covers every one of them.
    for cp in d["campaigns"]:
        home = HOME[geo_of(cp["name"])]
        for ag in cp["ad_groups"]:
            ag["final_url"] = home

    # 4e. scope: Kohei's "not skin related" flag
    if SKIN_ONLY:
        for cp in d["campaigns"]:
            cp["ad_groups"] = [a for a in cp["ad_groups"] if a["name"] not in WHOLE_BODY]
        report["scope"] = "SKIN_ONLY — whole-body groups removed"
    else:
        report["scope"] = "whole-body groups KEPT, flagged for Kohei"

    # 5. hard gates
    errs = []
    for cp in d["campaigns"]:
        for ag in cp["ad_groups"]:
            if ag["final_url"] not in HOME.values():
                errs.append(f"{ag['name']}: final URL must be a region home, got {ag['final_url']}")
            for h in ag["rsa"]["headlines"]:
                if len(h) > 30: errs.append(f"{ag['name']}: headline {len(h)} > 30 — {h!r}")
            for x in ag["rsa"]["descriptions"]:
                if len(x) > 90: errs.append(f"{ag['name']}: description {len(x)} > 90 — {x!r}")
            for p in ag["rsa"]["paths"]:
                if len(p) > 15: errs.append(f"{ag['name']}: path {len(p)} > 15 — {p!r}")
            for k in ag["keywords"]:
                bad = blocked_by(k["keyword"], ag["negatives"])
                if bad: errs.append(f"{ag['name']}: '{k['keyword']}' self-blocked by {bad}")
            import re as _re
            LOC = _re.compile(r"\b(in nz|in new zealand|in australia|nz registered|"
                              r"au registered|based in|practising in|practicing in)\b", _re.I)
            for x in ag["rsa"]["headlines"] + ag["rsa"]["descriptions"]:
                if LOC.search(x): errs.append(f"{ag['name']}: implies a location — {x!r}")
    import collections as _c
    for geo in ("NZ","AU"):
        hs = [h for c in d["campaigns"] if geo_of(c["name"])==geo
                for ag in c["ad_groups"] for h in ag["rsa"]["headlines"]]
        for h,n in _c.Counter(hs).items():
            if n>1: errs.append(f"{geo}: headline used {n}x — {h!r}")
    if errs:
        print("\nHARD FAIL:"); [print("  -",e) for e in errs]; sys.exit(1)

    # --- negative pruning -------------------------------------------------
    # Logan's rule: negatives block JUNK ONLY. They do not do routing, and they
    # do not second-guess a searcher's wording.
    #
    # What was removed and why:
    #  * CONDITION words (eczema, acne, tsw...) — every keyword in a condition
    #    group already carries its own condition, so the routing was already
    #    free. All these bought was a dead zone: "eczema steroid withdrawal
    #    naturopath" matched in BOTH Eczema and TSW, was blocked in both, and
    #    served nothing. TSW is caused by treating eczema — that is the core
    #    prospect, not an edge case.
    #  * GEO — location targeting is Presence-based; the country gate holds.
    #  * TREATMENT names (dupixent, steroid cream) — someone searching for an
    #    alternative to their steroid cream is the best prospect on the list.
    #  * detox / cleanse — things a naturopath actually does.
    #  * cure — blocks people in real distress. The ads answer honestly.
    #  * near me — the practice is online; proximity wording is not disqualifying.
    #  * dermatologist / medication side effects — comparison research, not junk.
    #  * "online" — was blocking "online herbal medicine nz". Plainly wrong.
    DROP = {
        # conditions
        "eczema","psoriasis","acne","rosacea","tsw","topical steroid withdrawal",
        "skin infection","urticaria",
        # geo
        "australia","sydney","melbourne","brisbane","perth","nz","new zealand",
        "auckland","wellington","hamilton","christchurch","dunedin","tauranga",
        "napier","palmerston north",
        # treatment / prospect signals
        "dupixent","steroid cream","detox","cleanse","cure","near me",
        "dermatologist","medication side effects","online",
    }
    before = sum(len(ag["negatives"]) for c in d["campaigns"] for ag in c["ad_groups"])
    for cp in d["campaigns"]:
        for ag in cp["ad_groups"]:
            ag["negatives"] = [n for n in ag["negatives"] if n not in DROP]
    after = sum(len(ag["negatives"]) for c in d["campaigns"] for ag in c["ad_groups"])
    print(f"  negatives pruned to junk-only: {before} -> {after} "
          f"({before-after} removed)")

    json.dump(d, open(os.path.join(OUT,"waterwell-2026-09-01.json"),"w"), indent=1)
    write_tabs(d)
    write_editor(d)

    print(f"\n  added   {report['added']} new unique terms "
          f"({report.get('short',0)} of them short head terms)")
    print(f"  pruned  {report.get('pruned',0)} dead long-tail / review-intent terms")
    print(f"  copy    all ad groups rewritten (problem -> cause -> proof -> offer)")
    print(f"  scope   {report['scope']}")
    print(f"  moved   {report['moved']} terms into the Herbal Medicine groups")
    print(f"  rejected {len(report['rejected'])} (kept out, with reason):")
    for g,t,why in report["rejected"]:
        print(f"     {g:<30} {t:<45} {why}")
    for g in ("NZ","AU"):
        print(f"  {g} unique terms now: {len(seen[g])}")

# ---------------------------------------------------------------- tab output
def write_tabs(d):
    for geo in ("NZ","AU"):
        camps = [c for c in d["campaigns"] if geo_of(c["name"]) == geo]
        rows = []
        w = rows.append
        total = sum(len({k['keyword'] for k in ag['keywords']}) for c in camps for ag in c['ad_groups'])
        ngrp  = sum(len(c["ad_groups"]) for c in camps)
        w([f"Waterwell Naturopath — {geo} SEARCH BUILD, 1 Sep 2026"])
        w([f'{len(camps)} campaigns | {ngrp} ad groups | {total} unique terms | "phrase" = phrase match · [exact] = exact match · broad NOT used'])
        w([f'Extends the 22 Aug build. Every final URL verified on waterwellclinic.com. Ad groups aligned to the site: 6 skin + 4 whole-body condition pages, plus the three named services.'])
        w([])
        w(["CAMPAIGN MAP"])
        w(["Campaign","Stage 1 daily $","Bid Strategy","Ad Group","Final URL","Unique terms","Kohei 20 Jul"])
        for c in camps:
            first = True
            for ag in c["ad_groups"]:
                n = len({k["keyword"] for k in ag["keywords"]})
                flag = ('SCOPE — flagged "not skin related", decision open'
                        if ag["name"] in WHOLE_BODY else "")
                w([c["name"] if first else "", c.get("daily_budget_nzd","") if first else "",
                   c.get("bid_strategy","") if first else "", ag["name"], ag["final_url"], n, flag])
                first = False
            w([]); w([])
        w(["KEYWORDS — each targeted as BOTH phrase and exact"])
        w(["Campaign","Ad Group",'Phrase match  "..."',"Exact match  [...]","NEW 1 Sep?"])
        base = set()
        try:
            b = json.load(open(SRC))
            for c in b["campaigns"]:
                for ag in c["ad_groups"]:
                    for k in ag["keywords"]: base.add((ag["name"], k["keyword"]))
        except Exception: pass
        for c in camps:
            for ag in c["ad_groups"]:
                for t in sorted({k["keyword"] for k in ag["keywords"]}):
                    w([c["name"], ag["name"], f'"{t}"', f"[{t}]",
                       "" if (ag["name"], t) in base else "NEW"])
                w([]); w([])
        w([])
        w(["AD COPY — RESPONSIVE SEARCH ADS (H<=30, D<=90)"])
        w(["Campaign","Ad Group"]+[f"H{i}" for i in range(1,16)]+
          [f"D{i}" for i in range(1,5)]+["Path1","Path2","Final URL","Pin plan"])
        for c in camps:
            for ag in c["ad_groups"]:
                r = ag["rsa"]
                w([c["name"], ag["name"]] + (r["headlines"]+[""]*15)[:15] +
                  (r["descriptions"]+[""]*4)[:4] + (r["paths"]+["",""])[:2] +
                  [ag["final_url"], r.get("pinning_notes","")])
                w([]); w([])
        w([])
        w(["NEGATIVE KEYWORDS — phrase match, per ad group"])
        w(["Campaign","Ad Group","Negatives (phrase match)"])
        for c in camps:
            for ag in c["ad_groups"]:
                w([c["name"], ag["name"], "; ".join(f'"{n}"' for n in ag["negatives"])])
                w([]); w([])
        w([])
        w(["SHARED NEGATIVE LISTS (phrase match)"])
        for name, terms in d["shared_negative_lists"].items():
            w([name, "; ".join(f'"{t}"' for t in terms)])
        w([])
        w(["EXTENSIONS"])
        w(["Type","Text","Desc 1","Desc 2","URL"])
        ex = d["extensions"][geo]
        for s in ex["sitelinks"]:
            w(["Sitelink"] + list(s)[:4])
        for c_ in ex["callouts"]: w(["Callout", c_,"","",""])
        sn = ex["snippets"]
        for v in sn["values"]: w([f"Snippet: {sn['header']}", v,"","",""])
        p = os.path.join(OUT, f"Waterwell-{geo}-2026-09-01.csv")
        with open(p,"w",newline="") as f: csv.writer(f).writerows(rows)
        print(f"  wrote {p}  ({len(rows)} rows)")

def write_editor(d):
    """Google Ads Editor import files. Headers mirror the 22 Aug build, which
    imported cleanly — do not 'tidy' them."""
    e = os.path.join(OUT, "editor"); os.makedirs(e, exist_ok=True)
    # paste/ mirrors editor/ as tab-separated text. Editor's from-file CSV import
    # is brittle; Import > Paste text is what actually works, so the paste copies
    # are generated here rather than hand-converted (they were, once, and drifted).
    pt = os.path.join(OUT, "paste"); os.makedirs(pt, exist_ok=True)
    def W(name, header, rows):
        with open(os.path.join(e, name), "w", newline="") as f:
            w = csv.writer(f); w.writerow(header); w.writerows(rows)
        for row in rows:
            for cell in row:
                if "\t" in str(cell) or "\n" in str(cell):
                    raise SystemExit(f"{name}: tab or newline inside a cell breaks "
                                     f"the paste import -> {cell!r}")
        with open(os.path.join(pt, name.replace(".csv", ".txt")), "w", newline="") as f:
            w = csv.writer(f, delimiter="\t"); w.writerow(header); w.writerows(rows)
        print(f"  editor/{name:<26} {len(rows):>4} rows")

    # Only columns Google Ads Editor actually resolves. The 22 Aug file pushed
    # prose into Bid Strategy Type / Locations / Ad Schedule ("Maximise Clicks,
    # max-CPC cap ~$1.50", "New Zealand — Presence only", "Mon-Sun all hours").
    # Editor cannot parse those: it drops them and the campaign imports LOOKING
    # fine while silently mis-set. Everything Editor can't take now lives in
    # SETUP.md as an explicit manual step instead of a false success.
    camps, ags, kws, negs, ads, sl, co, ss = [], [], [], [], [], [], [], []
    for c in d["campaigns"]:
        geo = geo_of(c["name"])
        # Editor rejects a $0 budget. The AU campaigns are held at $0 in the plan,
        # so they import at the $1.00 minimum and stay Paused — Paused is what
        # stops spend, not a zero budget. Set AU back to its real figure only
        # when the Australian-state and compliance gates clear.
        budget = max(float(c.get("daily_budget_nzd") or 0), 1.00)
        camps.append([c["name"], f"{budget:.2f}", "Search", "Paused",
                      "Maximize clicks"])
        for ag in c["ad_groups"]:
            ags.append([c["name"], ag["name"], "", "Enabled"])
            for t in sorted({k["keyword"] for k in ag["keywords"]}):
                kws.append([c["name"], ag["name"], t, "Phrase", "Enabled"])
                kws.append([c["name"], ag["name"], t, "Exact", "Enabled"])
            for n in ag["negatives"]:
                # These are NEGATIVES. Nothing in this file says so — Editor takes
                # the entity type from the VIEW the bulk-edit dialog was launched
                # from. Import it by selecting "Keywords, Negative" in the tree and
                # clicking "Make multiple changes" THERE. Account > Import > Paste
                # text always writes positive keywords: a "Type" column is left
                # unmapped, and "Negative Phrase" in Match Type is silently
                # coerced to "Phrase". Both of those shipped once already.
                negs.append([c["name"], ag["name"], n, "Phrase"])
            r = ag["rsa"]
            ads.append([c["name"], ag["name"], "Responsive search ad", ag["final_url"]]
                       + (r["headlines"]+[""]*15)[:15]
                       + (r["descriptions"]+[""]*4)[:4]
                       + (r["paths"]+["",""])[:2] + ["Enabled"])
        ex = d["extensions"][geo]
        for x in ex["sitelinks"]:  sl.append([c["name"]] + list(x)[:4])
        for x in ex["callouts"]:   co.append([c["name"], x])
        # The column is "Snippet Values" — semicolon-delimited, one column.
        # Plain "Values" is not recognised and imports a snippet with zero
        # values, which then fails Google's "at least 3 values" rule; and
        # "Value 1"/"Value 2" columns are marked Not importing. Language must
        # be stated or Editor picks one for you (it chose French).
        ss.append([c["name"], "English", ex["snippets"]["header"],
                   ";".join(ex["snippets"]["values"])])

    # Editor's own schema, not the web-UI bulk-upload schema. Editor uses a single
    # "Campaign Daily Budget" column and has no "Budget"/"Budget Type" pair — that
    # mismatch is what made the 22 Aug file unimportable.
    W("campaigns.csv", ["Campaign","Campaign Daily Budget","Campaign Type","Status",
                        "Bid Strategy Type"], camps)
    W("adgroups.csv", ["Campaign","Ad Group","Max CPC","Status"], ags)
    W("keywords.csv", ["Campaign","Ad Group","Keyword","Match Type","Status"], kws)
    W("negatives.csv", ["Campaign","Ad Group","Keyword","Match Type"], negs)
    W("ads.csv", ["Campaign","Ad Group","Ad type","Final URL"]
        + [f"Headline {i}" for i in range(1,16)]
        + [f"Description {i}" for i in range(1,5)] + ["Path 1","Path 2","Status"], ads)
    W("sitelinks.csv", ["Campaign","Sitelink text","Description line 1","Description line 2",
        "Final URL"], sl)
    W("callouts.csv", ["Campaign","Callout text"], co)
    W("structured-snippets.csv",
      ["Campaign","Language","Header","Snippet Values"], ss)
    W("shared-negative-lists.csv", ["List","Keyword","Match Type"],
      [[n,t,"Phrase"] for n,ts in d["shared_negative_lists"].items() for t in ts])


if __name__ == "__main__":
    main()
