# Final URLs → region home page (8 Sep 2026)

**Why.** The per-condition pages (`/conditions/eczema`, `/tsw`, `/psoriasis`,
`/acne`, `/rosacea`, `/skin-infections`) read as a blog, not as a clinic that
takes bookings. Every ad now lands on the region home page instead.

**Region home, not the global `/`.** `/nz` and `/au` carry different compliance
wording and the campaigns are geo-split — an AU click must never land on the NZ
page. `waterwellclinic.com/` is a third, separate global page; sending geo-split
campaigns there would drop the region targeting the whole build is structured
around.

## What changed — 12 ads

| Campaign | Ad group | Was | Now |
|---|---|---|---|
| WW \| NZ \| Skin Conditions | Eczema | /conditions/eczema | **/nz** |
| WW \| NZ \| Skin Conditions | Topical Steroid Withdrawal | /conditions/tsw | **/nz** |
| WW \| NZ \| Skin Conditions | Psoriasis | /conditions/psoriasis | **/nz** |
| WW \| NZ \| Skin Conditions | Acne | /conditions/acne | **/nz** |
| WW \| NZ \| Skin Conditions | Rosacea | /conditions/rosacea | **/nz** |
| WW \| NZ \| Skin Conditions | Skin Infections | /conditions/skin-infections | **/nz** |
| WW \| AU \| Skin Conditions | Eczema AU | /conditions/eczema | **/au** |
| WW \| AU \| Skin Conditions | TSW AU | /conditions/tsw | **/au** |
| WW \| AU \| Skin Conditions | Psoriasis AU | /conditions/psoriasis | **/au** |
| WW \| AU \| Skin Conditions | Acne AU | /conditions/acne | **/au** |
| WW \| AU \| Skin Conditions | Rosacea AU | /conditions/rosacea | **/au** |
| WW \| AU \| Skin Conditions | Skin Infections AU | /conditions/skin-infections | **/au** |

The other 7 ads were already on `/nz` or `/au` and are untouched.

**Display paths are unchanged.** `/online/eczema`, `/australia/psoriasis` etc.
still carry the condition into the visible URL — that is the CTR asset, and the
home page covers every one of those conditions, so the path stays accurate.

## Posting it to the live account (125-697-3392)

⚠ **Do NOT run `Account > Import` on `editor/ads.csv`.** Editor matches ads on
their full content, so an import creates 12 NEW ads and leaves the 12 running
ones in place — you would end up serving both. Change the URL in the grid:

1. Google Ads Editor → **Get recent changes** (Basic) on 125-697-3392.
2. Left tree → **Ads and extensions > Responsive search ads**.
3. Filter the ad list to `Campaign contains "Skin Conditions"` → 12 rows.
4. Select all 12 → in the edit panel set **Final URL**:
   - the 6 NZ rows → `https://waterwellclinic.com/nz`
   - the 6 AU rows → `https://waterwellclinic.com/au`
   (do the two geos as two selections, they take different URLs)
5. **Post**.

RSAs are editable in place, so the ads keep their IDs and history. They will go
back to **Under review** for a few hours — normal, and in this health vertical
expect the **Request exemption** banner again on the Health-in-personalized-
advertising flag. Tick it, same as at launch.

## Still pointing at a condition page — needs a call

The **"Gut, Hormones & Energy"** sitelink on all 5 campaigns still goes to
`/conditions/gut-health`. Same blog problem, and it is off-scope anyway since
SKIN_ONLY removed the whole-body ad groups. Options: retire the sitelink, or
retarget it at `/nz#conditions` (which duplicates the "Skin Health" sitelink
destination). Left as-is pending Logan.

## Source

`expand.py` now forces `ag["final_url"]` to the region home for every ad group,
and the hard gate rejects anything that is not `/nz` or `/au`. Regenerating the
build can no longer reintroduce a condition-page URL.
