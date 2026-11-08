"""Runs tools/compliance_v4.py UNCHANGED except one line: a /concept-spec/<page> is scoped like
its v4 twin <page> for the released-location allow-list (LOCATION_CLEARED is keyed on bare v4
paths, so 'concept-spec/index.html' never matches 'index.html'). Every rule and pattern is the
tool's own. Usage: python3 _work/concept2/compliance_concept.py concept-spec/index.html ..."""
import os, sys
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src = open(os.path.join(R, 'tools/compliance_v4.py')).read()
old = "        if path in pages:"
assert src.count(old) == 1
src = src.replace(old, "        if path.removeprefix('concept-spec/') in pages:")
src = src.replace("os.path.dirname(os.path.dirname(os.path.abspath(__file__)))", repr(R))
exec(compile(src, 'compliance_v4.py(concept scope)', 'exec'), {'__name__': '__main__'})
