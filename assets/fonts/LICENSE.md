# Font licences

Both families bundled in this directory are licensed under the
**SIL Open Font License, Version 1.1**, which permits bundling and
redistribution with a project, including commercially.

| Family | Faces here | Source | Licence |
|---|---|---|---|
| Instrument Serif | regular + italic, latin & latin-ext | Instrument, via Google Fonts | OFL 1.1 |
| Manrope | variable 300–800, latin & latin-ext | Mikhail Sharanda, via Google Fonts | OFL 1.1 |

Full licence text: <https://openfontlicense.org/open-font-license-official-text/>

## Why these are self-hosted

They were previously pulled from `fonts.googleapis.com` on every page load,
which put a render-blocking third-party round trip in front of first paint on
all 16 pages. They are now served from this directory: 84KB total across six
faces, with the two first-viewport faces preloaded.

`latin-ext` is kept deliberately — it carries the macrons (ā ē ī ō ū) that a
New Zealand site needs.

## Updating

Re-fetch from Google Fonts with a modern browser User-Agent (an old UA returns
TTF instead of WOFF2), keep only the `latin` and `latin-ext` subsets, and keep
the `unicode-range` on each `@font-face` so the browser only downloads the
subset it needs. The `@font-face` block lives inline in the `<style>` of
`index.html`, `blog.html`, `tools/build_conditions.py` and `tools/build_legal.py`.
