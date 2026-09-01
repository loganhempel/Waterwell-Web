#!/usr/bin/env python3
"""Short head terms — what people actually type — plus the dead long-tail to drop.

The 22 Aug build skewed long: 3-4 words with a geo suffix stapled on. Those
serve almost nothing in a market NZ's size. Phrase match already reaches every
LONGER form of a short term, so the short head term is the reach lever; the
specific ones stay for bid control and clean reporting.
"""

SHORT = {
"Online Naturopath Consult": ["naturopath consult","naturopath appointment","see a naturopath",
  "naturopath booking","video naturopath","naturopath session","book a naturopath"],
"General Naturopathy": ["naturopath","naturopathy","natural health","natural medicine",
  "holistic practitioner","naturopath consultation"],
"Gut & Digestive Health": ["bloating help","ibs help","gut health help","bloating naturopath",
  "ibs naturopath","gut specialist","gut testing","leaky gut help","sibo help"],
"Hormones & Women's Health": ["hormone naturopath","pms help","pcos help","menopause naturopath",
  "perimenopause help","hormone testing","period problems help"],
"Fatigue & Energy": ["fatigue help","burnout help","low energy help","always tired",
  "chronic fatigue help","adrenal fatigue","energy testing"],
"Stress & Sleep": ["insomnia help","sleep help","stress help","cant sleep help",
  "natural sleep remedies","sleep support"],
"Herbal Medicine": ["herbalist","herbal medicine","herbal remedies","herbal consultation",
  "herbal practitioner"],
"Eczema": ["eczema help","eczema treatment","eczema specialist","eczema diet","eczema causes",
  "help with eczema","eczema support","natural eczema treatment"],
"Topical Steroid Withdrawal": ["tsw help","tsw support","tsw treatment","tsw recovery",
  "topical steroid withdrawal","steroid withdrawal"],
"Psoriasis": ["psoriasis help","psoriasis treatment","psoriasis diet","psoriasis specialist",
  "psoriasis causes","help with psoriasis","natural psoriasis treatment"],
"Acne": ["acne help","acne treatment","acne diet","acne specialist","hormonal acne","adult acne",
  "cystic acne","help with acne","acne causes"],
"Rosacea": ["rosacea help","rosacea treatment","rosacea diet","rosacea specialist",
  "rosacea triggers","help with rosacea","natural rosacea treatment"],
"Skin Infections": ["chronic hives","recurring hives","hives help","hives treatment",
  "urticaria help","itchy skin help","recurring boils","skin infection help"],

"Online Naturopath Consult AU": ["naturopath consult","naturopath appointment","see a naturopath",
  "naturopath booking","video naturopath","naturopath session","book a naturopath"],
"General Naturopathy AU": ["naturopath","naturopathy","natural health","natural medicine",
  "holistic practitioner","naturopath consultation"],
"Gut & Digestive Health AU": ["bloating help","ibs help","gut health help","bloating naturopath",
  "gut specialist","gut testing","leaky gut help","sibo help"],
"Hormones & Women's Health AU": ["hormone naturopath","pms help","menopause naturopath",
  "perimenopause help","hormone testing","period problems help"],
"Fatigue & Energy AU": ["fatigue help","burnout help","low energy help","always tired",
  "chronic fatigue help","adrenal fatigue","energy testing"],
"Herbal Medicine AU": ["herbalist","herbal medicine","herbal remedies","herbal consultation",
  "herbal practitioner"],
"Eczema AU": ["eczema help","eczema treatment","eczema specialist","eczema diet","eczema causes",
  "help with eczema","eczema support","natural eczema treatment"],
"TSW AU": ["tsw help","tsw support","tsw treatment","tsw recovery","topical steroid withdrawal",
  "steroid withdrawal"],
"Psoriasis AU": ["psoriasis help","psoriasis treatment","psoriasis diet","psoriasis specialist",
  "psoriasis causes","help with psoriasis","natural psoriasis treatment"],
"Acne AU": ["acne help","acne treatment","acne diet","acne specialist","hormonal acne","adult acne",
  "cystic acne","help with acne","acne causes"],
"Rosacea AU": ["rosacea help","rosacea treatment","rosacea diet","rosacea specialist",
  "rosacea triggers","help with rosacea","natural rosacea treatment"],
"Skin Infections AU": ["chronic hives","recurring hives","hives help","hives treatment",
  "urticaria help","itchy skin help","skin infection help"],
}

# Logistics/how-it-works questions. Almost no volume, and no booking intent when
# they do fire. The "why won't my X go away" problem-phrasings are KEPT — those
# are real searches from people at the end of their patience.
PRUNE = [
 "how much does a tsw naturopath cost","how much is an online naturopath consult",
 "how to find a good naturopath nz","first naturopath appointment what to expect",
 "what happens in a naturopath consult","how does an online naturopath work",
 "naturopath that works with your doctor","naturopath consultation length australia",
 "long term steroid cream withdrawal support","naturopath for mood and hormones australia",
 "difference between naturopath and herbalist","is a naturopath worth it",
 "naturopath vs homeopath","naturopath vs gp","naturopath vs gp australia",
 "naturopath for busy professionals","naturopath alongside medication",
 "same week naturopath appointment nz","naturopath for shift work sleep",
 "naturopath for overthinking and stress","naturopath for low libido women",
 "5 star naturopath australia","online naturopath reviews australia",
 "naturopath reviews nz","waterwell clinic reviews","eczema naturopath reviews nz",
 "psoriasis naturopath reviews nz","acne naturopath reviews","rosacea naturopath reviews",
 "skin infection naturopath reviews","tsw naturopath reviews",
]
