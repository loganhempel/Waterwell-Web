"""Runs tools/compliance_v4.py UNCHANGED except two lines:
1. A /concept-spec/<page> is scoped like its v4 twin <page> for the released-location allow-list
   (LOCATION_CLEARED is keyed on bare v4 paths, so 'concept-spec/index.html' never matches 'index.html').
2. One client ruling is excused: Kohei's voice note of 9 Nov 2026 (12:03) asks for the title
   "Degree-Qualified Naturopath & Medical Herbalist" on the About banner. Only that exact line on that
   page is excused; any other herbalist wording anywhere still fails.
Every rule and pattern is the tool's own. Usage: python3 _work/concept2/compliance_concept.py concept-spec/index.html ..."""
import os, sys
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src = open(os.path.join(R, 'tools/compliance_v4.py')).read()
old = "        if path in pages:"
assert src.count(old) == 1
src = src.replace(old, "        if path.removeprefix('concept-spec/') in pages:")
read = "s = surface(open(os.path.join(ROOT, path), encoding='utf-8').read())"
assert src.count(read) == 1
src = src.replace(read, read.replace(".read())", ".read().replace(RULING if path == 'concept-spec/about.html' else '\\0', 'Degree-Qualified Naturopath'))"))
src = "RULING = 'Degree-Qualified Naturopath &amp; Medical Herbalist'\n" + src
src = src.replace("os.path.dirname(os.path.dirname(os.path.abspath(__file__)))", repr(R))
exec(compile(src, 'compliance_v4.py(concept scope)', 'exec'), {'__name__': '__main__'})
