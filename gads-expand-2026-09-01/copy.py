#!/usr/bin/env python3
"""Waterwell RSA copy — 1 Sep 2026 rewrite.

Problem -> root cause -> proof -> format -> offer. Grounded only in what
waterwellclinic.com actually says: the 75-minute initial consultation, the free
15-minute discovery session, functional tests posted out, individually
prescribed herbal formulas, and Kohei's own eczema history.

HARD RULES
  - Online-only practice. Never imply Kohei is located or registered in a
    country: no "in NZ", "NZ registered", "based in", "practising in".
    Geo may only describe who he SERVES: "NZ-Wide", "Across Australia".
  - No patient testimonials, reviews, star ratings or counts (Kohei, 17 Aug,
    both geos).
  - No cure/guarantee claims, no "quick fix", no outcome percentages.
  - No defensive copy ("no pressure", "no obligation", "no commitment").
  - AU: no mental-illness representations, no serious-disease claims, and the
    personal-recovery story stays out (NZ only).
"""

# ---- per-group hand-written angles: the differentiated copy -----------------
# kw1/kw2 = keyword headlines · p1/p2 = the problem in the patient's words
# mech    = the reframe · d1 = problem->promise · d2 = mechanism
G = {
"Brand - Waterwell": dict(
  kw1="Waterwell Clinic", kw2="Waterwell Naturopath",
  p1="Kohei Iguchi, Naturopath", p2="Skin, Gut, Hormones & Energy",
  mech="Root-Cause Naturopathy",
  d1="Waterwell Clinic. Kohei Iguchi's naturopathy practice for skin, gut, hormones and energy.",
  d2="A 75-minute initial consultation that looks for the cause, not another thing to manage."),

"Online Naturopath Consult": dict(
  kw1="Online Naturopath NZ", kw2="Online Naturopath Consultation",
  p1="Told Your Bloods Are Normal", p2="Tired Of Managing Symptoms",
  mech="Find The Root Cause",
  d1="Still no answers after normal bloods? A 75-minute consultation that looks for the cause.",
  d2="Functional testing posted to your door, then a plan built on your actual results."),

"General Naturopathy": dict(
  kw1="Naturopath NZ", kw2="Naturopath Consultation Online",
  p1="No Good Naturopath Near You?", p2="Answers, Not Another Symptom",
  mech="Whole-Body, Not Just The Bit",
  d1="No decent naturopath nearby? Consultations run by video, so location stops mattering.",
  d2="Gut, skin, hormones, sleep and energy, looked at together rather than one at a time."),

"Gut & Digestive Health": dict(
  kw1="Naturopath For Gut Health", kw2="Naturopath For Bloating",
  p1="Bloated By The Afternoon", p2="IBS You've Just Lived With",
  mech="Test Your Gut, Don't Guess",
  d1="Bloating, IBS and reflux you've stopped mentioning. Testing shows what's driving it.",
  d2="Stool and microbiome kits posted to your door, then a plan built on the results."),

"Hormones & Women's Health": dict(
  kw1="Naturopath For Hormones", kw2="Naturopath For PCOS & PMS",
  p1="PMS That Runs Your Month", p2="A Cycle That Makes No Sense",
  mech="Test Hormones, Don't Guess",
  d1="PMS, perimenopause, PCOS. Hormone testing posted out, then a plan built on results.",
  d2="A plan built around your actual cycle, not a template handed to everyone."),

"Fatigue & Energy": dict(
  kw1="Naturopath For Fatigue", kw2="Naturopath For Burnout",
  p1="Tired After A Full Night", p2="Coffee Stopped Working",
  mech="Find Out Why You're Tired",
  d1="Exhausted but your bloods came back fine? Iron, thyroid and adrenal testing, posted out.",
  d2="Fatigue has drivers. Testing finds yours instead of another supplement guess."),

"Stress & Sleep": dict(
  kw1="Naturopath For Sleep", kw2="Naturopath For Stress",
  p1="Wired At Night, Flat By Day", p2="Awake At 3am, Again",
  mech="Test Your Cortisol Pattern",
  d1="Wired at night and flat all day is a cortisol pattern, and it can be tested.",
  d2="Cortisol testing posted to your door, then a plan built around your sleep."),

"Herbal Medicine": dict(
  kw1="Medical Herbalist NZ", kw2="Online Herbal Medicine",
  p1="Not Another Off-Shelf Bottle", p2="Tried Every Supplement Going",
  mech="Formulas Made For You",
  d1="Individually prescribed herbal formulas, chosen for your case, not pulled off a shelf.",
  d2="Your formula is adjusted as your body responds, not repeated on autopilot."),

"Eczema": dict(
  kw1="Naturopath For Eczema", kw2="Eczema Naturopath Online",
  p1="Itching That Wakes You At 3am", p2="Flares That Keep Coming Back",
  mech="Eczema Starts On The Inside",
  d1="Steroid creams calm the flare. They don't touch whatever keeps causing it.",
  d2="Kohei was once head to toe in eczema himself. He treats the gut and immune drivers."),

"Topical Steroid Withdrawal": dict(
  kw1="TSW Naturopath", kw2="Topical Steroid Withdrawal",
  p1="Worse Since Stopping Steroids", p2="Red, Burning, Shedding Skin",
  mech="TSW Is A Process, Not A Flare",
  d1="Topical steroid withdrawal is brutal, and badly understood. You don't have to guess.",
  d2="Kohei came off long-term steroids himself. Support that takes TSW seriously."),

"Psoriasis": dict(
  kw1="Naturopath For Psoriasis", kw2="Psoriasis Naturopath Online",
  p1="Plaques That Never Fully Go", p2="Flares With No Clear Trigger",
  mech="Psoriasis Is An Immune Signal",
  d1="Psoriasis is immune-driven. Calming the skin without calming the driver never holds.",
  d2="Diet, gut and immune factors looked at together, then tested where it's unclear."),

"Acne": dict(
  kw1="Naturopath For Acne", kw2="Hormonal Acne Naturopath",
  p1="Adult Acne That Won't Clear", p2="Breakouts On A Monthly Cycle",
  mech="Acne Is A Hormone & Gut Signal",
  d1="Adult acne is rarely about your face wash. Usually it's hormones and gut.",
  d2="Hormone and gut testing posted out, then a plan built on what it actually shows."),

"Rosacea": dict(
  kw1="Naturopath For Rosacea", kw2="Rosacea Naturopath Online",
  p1="Redness That Flares At Random", p2="Flushing You Can't Predict",
  mech="Find Your Rosacea Triggers",
  d1="Rosacea flares have triggers. Most people are never shown how to find theirs.",
  d2="Gut, diet and trigger factors mapped properly, rather than managing the redness."),

"Skin Infections": dict(
  kw1="Naturopath For Skin Infections", kw2="Chronic Hives Naturopath",
  p1="Infections That Keep Returning", p2="Hives With No Known Cause",
  mech="Recurring Is An Immune Signal",
  d1="Skin infections and hives that keep returning are a signal, not bad luck.",
  d2="Immune and gut testing posted out, so recurring problems get looked at properly."),
}

# AU variants: same problems, no personal-recovery story, AU geo wording.
AU_OVERRIDE = {
"Online Naturopath Consult AU": dict(kw1="Online Naturopath Australia", kw2="Naturopath Consultation Online"),
"General Naturopathy AU":       dict(kw1="Naturopath Australia", kw2="Online Naturopath Consult"),
"Herbal Medicine AU":           dict(kw1="Medical Herbalist Australia", kw2="Online Herbal Medicine"),
"Eczema AU": dict(d2="Eczema is looked at from the gut and immune side, not only the skin."),
"TSW AU":    dict(d2="Unhurried support for topical steroid withdrawal, at the pace your skin sets."),
}

# ---- rotating pools: shared angles, phrased differently per group -----------
# Every RSA headline must be unique within a geo, so each group draws a
# different phrasing of the same angle. All <=30 chars.
TEST = ["Tests Posted To Your Door","Lab Testing, Done At Home","Test Kits Sent Out To You",
 "Functional Testing Included","Data, Not Another Guess","Real Testing Behind The Plan",
 "Testing, Not Trial And Error","Answers From Actual Testing","Test First, Then Treat",
 "Lab Work Without The Clinic","Your Results, Your Plan","Guesswork Taken Out","Tested, Not Assumed",
 "Evidence Before Advice"]

FORMAT = ["75-Min Initial Consultation","Consults By Secure Video","Fully Online Consultations",
 "Meet By Secure Video Call","Online, No Clinic Visit","Video Consults From Home",
 "Book Online, Meet Online","A Full 75-Minute Appointment","Private, Secure Video Calls",
 "Consult From Your Own Home","Online Video Appointments","No Travel, No Waiting Room",
 "Appointments That Fit Work","Seen Properly, Not Rushed"]

CONSULT = ["One Practitioner, Every Visit","Same Practitioner Each Time","No Waitlist, Book Direct",
 "Unhurried, One-On-One Care","You're Not Rushed Through","A Plan Built Around You",
 "Not A Template Plan","Your Case, Not A Protocol","One-On-One, Start To Finish",
 "Time To Tell It Properly","Seen As A Whole Person","Continuity, Every Appointment",
 "The Same Face Each Time","Your History Actually Heard"]

GP = ["Works Alongside Your GP","Your GP Stays In The Loop","Alongside Your Doctor's Care",
 "Not Instead Of Your Doctor","Adds To Your Current Care","Sits Beside Your GP's Plan",
 "Complements Your GP Care","Keeps Your Doctor Informed","Works With Your Doctor",
 "Fits Around Your GP's Care","Alongside Your Current Care","Your Doctor Stays Involved",
 "With Your GP, Not Against","Supports Your Medical Care"]

OFFER = ["Free 15-Minute Chat First","Start With A Free 15 Mins","Your First Call Is Free",
 "A Free 15-Minute Call","Free Discovery Call First","15 Free Minutes To Start",
 "Book A Free 15-Min Chat","Free 15-Min Discovery Call","Start With A Free Chat",
 "A Free First Conversation","Talk First, Free Of Charge","Free Intro Call Available",
 "First Conversation Is Free","A Free Chat Before You Book"]

HERB = ["Herbal Formulas Made For You","Individually Prescribed Herbs","Herbs Chosen For Your Case",
 "Prescribed, Not Off A Shelf","Your Own Herbal Formula","Formulas Adjusted As You Go",
 "Herbal Medicine, Prescribed","Made Up For Your Case","Not A Shelf Supplement",
 "Herbs Matched To Your Case","A Formula Built For You","Adjusted As Your Body Responds",
 "Custom Herbal Prescribing","Herbal Medicine, Personalised"]

def cta(kw, geo):
    return None  # per-group, built below

# ---- assembler --------------------------------------------------------------
def build(order, geo, ctas, geolines):
    """order: ad-group names in slot order for this geo."""
    out = {}
    for i, name in enumerate(order):
        key = {"TSW AU":"Topical Steroid Withdrawal"}.get(name,
               name[:-3] if name.endswith(" AU") else name)
        base = dict(G[key])
        base.update(AU_OVERRIDE.get(name, {}))
        h = [base["kw1"], base["kw2"], base["p1"], base["p2"], base["mech"],
             TEST[i], FORMAT[i], CONSULT[i], GP[i], OFFER[i], HERB[i],
             geolines[i], ctas[name][0], ctas[name][1], ctas[name][2]]
        d = [base["d1"], base["d2"],
             ("A free 15-minute discovery session first, or book the full consultation."
              if i % 2 == 0 else
              "Start with a free 15-minute session, or go straight to a full consultation."),
             ("Naturopathy that works alongside your GP and current medication, not against it."
              if i % 3 == 0 else
              "Works alongside the medical care you already have. Nothing is replaced.")]
        out[name] = {"headlines": h, "descriptions": d,
                     "paths": base.get("paths", []), "pinning_notes":
                     f"Pos1 pin: {base['kw1']!r}. Rest unpinned."}
    return out

NZ_ORDER = ["Brand - Waterwell","Online Naturopath Consult","General Naturopathy",
 "Gut & Digestive Health","Hormones & Women's Health","Fatigue & Energy","Stress & Sleep",
 "Herbal Medicine","Eczema","Topical Steroid Withdrawal","Psoriasis","Acne","Rosacea",
 "Skin Infections"]
AU_ORDER = ["Online Naturopath Consult AU","General Naturopathy AU","Gut & Digestive Health AU",
 "Hormones & Women's Health AU","Fatigue & Energy AU","Herbal Medicine AU","Eczema AU","TSW AU",
 "Psoriasis AU","Acne AU","Rosacea AU","Skin Infections AU"]

NZ_GEO = ["Waterwell, NZ-Wide","Online Naturopath, NZ-Wide","Naturopath Across NZ",
 "Gut Support, NZ-Wide","Hormone Support, NZ-Wide","Energy Support, NZ-Wide",
 "Sleep Support, NZ-Wide","Herbal Medicine, NZ-Wide","Eczema Support, NZ-Wide",
 "TSW Support, NZ-Wide","Psoriasis Support, NZ-Wide","Acne Support, NZ-Wide",
 "Rosacea Support, NZ-Wide","Skin Support, NZ-Wide"]
AU_GEO = ["Online Naturopath, AU-Wide","Naturopath Across Australia","Gut Support, AU-Wide",
 "Hormone Support, AU-Wide","Energy Support, AU-Wide","Herbal Medicine, AU-Wide",
 "Eczema Support, AU-Wide","TSW Support, AU-Wide","Psoriasis Support, AU-Wide",
 "Acne Support, AU-Wide","Rosacea Support, AU-Wide","Skin Support, AU-Wide"]

NZ_CTA = {
 "Brand - Waterwell":["Book With Waterwell","See Consultation Options","Book Your Consultation"],
 "Online Naturopath Consult":["Book A Naturopath Consult","See What's Actually Wrong","Book Your First Session"],
 "General Naturopathy":["Book A Naturopathy Session","Get To The Cause","Book Your Consult Today"],
 "Gut & Digestive Health":["Book A Gut Health Consult","Sort Your Digestion Out","Start With Your Gut"],
 "Hormones & Women's Health":["Book A Hormone Consult","Get Your Cycle Back","Start Hormone Testing"],
 "Fatigue & Energy":["Book A Fatigue Consult","Get Your Energy Back","Find Out What's Draining You"],
 "Stress & Sleep":["Book A Sleep Consult","Sleep Properly Again","Start With Your Cortisol"],
 "Herbal Medicine":["Book A Herbal Consult","Get Your Own Formula","Speak To A Herbalist"],
 "Eczema":["Book An Eczema Consult","Treat The Cause, Not The Flare","Start Your Eczema Plan"],
 "Topical Steroid Withdrawal":["Book A TSW Consult","Get Real TSW Support","Start Your TSW Plan"],
 "Psoriasis":["Book A Psoriasis Consult","Calm The Driver, Not The Skin","Start Your Psoriasis Plan"],
 "Acne":["Book An Acne Consult","Clear It From The Inside","Start Your Acne Plan"],
 "Rosacea":["Book A Rosacea Consult","Find What Sets It Off","Start Your Rosacea Plan"],
 "Skin Infections":["Book A Skin Consult","Stop The Cycle Repeating","Start Your Skin Plan"]}
AU_CTA = {
 "Online Naturopath Consult AU":["Book A Naturopath Consult","See What's Actually Wrong","Book Your First Session"],
 "General Naturopathy AU":["Book A Naturopathy Session","Get To The Cause","Book Your Consult Today"],
 "Gut & Digestive Health AU":["Book A Gut Health Consult","Sort Your Digestion Out","Start With Your Gut"],
 "Hormones & Women's Health AU":["Book A Hormone Consult","Get Your Cycle Back","Start Hormone Testing"],
 "Fatigue & Energy AU":["Book A Fatigue Consult","Get Your Energy Back","Find What's Draining You"],
 "Herbal Medicine AU":["Book A Herbal Consult","Get Your Own Formula","Speak To A Herbalist"],
 "Eczema AU":["Book An Eczema Consult","Treat The Cause, Not The Flare","Start Your Eczema Plan"],
 "TSW AU":["Book A TSW Consult","Get Real TSW Support","Start Your TSW Plan"],
 "Psoriasis AU":["Book A Psoriasis Consult","Calm The Driver, Not The Skin","Start Your Psoriasis Plan"],
 "Acne AU":["Book An Acne Consult","Clear It From The Inside","Start Your Acne Plan"],
 "Rosacea AU":["Book A Rosacea Consult","Find What Sets It Off","Start Your Rosacea Plan"],
 "Skin Infections AU":["Book A Skin Consult","Stop The Cycle Repeating","Start Your Skin Plan"]}

def all_copy():
    r = build(NZ_ORDER, "NZ", NZ_CTA, NZ_GEO)
    r.update(build(AU_ORDER, "AU", AU_CTA, AU_GEO))
    # AU must not carry the personal-recovery story
    for n in ("Eczema AU","TSW AU"):
        r[n]["descriptions"][1] = AU_OVERRIDE[n]["d2"]
    return r

if __name__ == "__main__":
    import re, collections
    c = all_copy()
    BAD = re.compile(r"\b(in nz|in new zealand|in australia|nz registered|au registered|"
                     r"based in|practising in|practicing in|nz-based|au-based|guarantee|cure|"
                     r"no pressure|no obligation|no commitment|quick fix|review|star|rated)\b", re.I)
    errs = []
    for g, r in c.items():
        for h in r["headlines"]:
            if len(h) > 30: errs.append(f"{g}: H {len(h)} — {h!r}")
            if BAD.search(h): errs.append(f"{g}: BANNED in H — {h!r}")
        for d in r["descriptions"]:
            if len(d) > 90: errs.append(f"{g}: D {len(d)} — {d!r}")
            if BAD.search(d): errs.append(f"{g}: BANNED in D — {d!r}")
        if len(set(r["headlines"])) != 15: errs.append(f"{g}: duplicate headline inside group")
    for geo, order in (("NZ", NZ_ORDER), ("AU", AU_ORDER)):
        seen = collections.Counter(h for g in order for h in c[g]["headlines"])
        for h, n in seen.items():
            if n > 1: errs.append(f"{geo}: headline repeated {n}x across groups — {h!r}")
    print(f"{len(c)} ad groups · {sum(len(r['headlines']) for r in c.values())} headlines · "
          f"{sum(len(r['descriptions']) for r in c.values())} descriptions")
    if errs:
        print(f"\n{len(errs)} PROBLEMS:")
        for e in errs[:40]: print("  -", e)
    else:
        print("PASS: lengths, banned phrases, uniqueness within each geo.")
