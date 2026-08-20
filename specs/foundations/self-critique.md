---
id: self-critique
kind: foundation
status: stable
---
# Self-critique — make the output match or beat the reference

A spec library doesn't guarantee a good slide on its own; you have to **look at what you built and fix it.**
After building, before delivering, evaluate the slide against a bar and iterate until it clears it. This is
the output-side loop (the mirror of `learn-from-image.md`, which is the input side).

## Two bars
1. **The reference** (when the user gave a reference image or is matching a style): does the build deliver
   the **same intention at least as well?** Not a pixel copy — it's a different language (繁中/EN, never
   Korean) and theme — but **intention-and-quality parity or better**.
2. **The rules** (always): the foundations + `audit.md`.

## How to self-critique
1. **Render it and look — for real.** Take an actual **screenshot** of the built HTML at deck size
   (1920×1080) and view it. On a machine with a Chromium browser:
   `msedge|chrome --headless=new --window-size=1920,1080 --screenshot=out.png "file:///…/slide.html"`
   then open `out.png`. **Structural validation (tag balance, link check) is NOT enough** — it cannot see a
   broken render. Critique what you *see*, not the source; most balance problems are invisible in code.
   - **Examples/built slides must be self-contained:** inline the theme tokens + `base.css` into a `<style>`
     block (as the repo's existing examples do). **Linked `<link href="../assets/…">` stylesheets can
     silently fail to load** in a preview/`file://` context, leaving an unstyled white page — a failure no
     code check catches, only the screenshot does.
2. **Run the layout gate before scoring by eye.**
   `python scripts/validate_layout.py <slide.html>` measures the things this file used to only
   describe: whether the render actually painted, whether content distributes top→bottom, whether a
   quadrant is dead, and whether density is at an extreme. It reports a named defect and the fix.
   Treat a reported failure as a **fix**, never a pass — then continue to the judgement calls below,
   which no measurement can make for you.
   **A pass is not proof.** The gate scans rows across the whole canvas, so it cannot see a card
   inflated around its content when a neighbouring column carries text. That exact case passed at
   57% whitespace during v12.9 and was caught only by looking. Always look at the screenshot.
3. **Score each dimension** (pass / fix):
   - intention delivered (the page does its job — `content-map.md`)
   - whole-page balance (no lopsided/heavy quadrant — `layout-balance.md`)
   - density: **不空不擠** (~30–45% whitespace — `layout-balance.md`)
   - proportional sizing (title/body/icon/number scaled to their boxes; content fills, doesn't float)
   - 4-color discipline · plain-language title · imagery on-system
   - for `editorial-explainer-stage`: genuine image-generator call · fresh output rather than reference
     reuse · exact target ratio · full-block fill · colour preserved · native copy fidelity · local asset
     persistence · no CSS/SVG substitute · complete `illustration-plan.json` · passing plan validator
   - **HTML/CSS code quality** — run **`modern-web-guidance`** on the built file (search/retrieve via
     `npx modern-web-guidance@latest`): `text-wrap: balance` on headings + `pretty` on body copy,
     overflow-safe layout (`min-width:0` on flex children), no fragile fixed heights, modern layout idioms.
     This is the code-level complement to the visual screenshot review.
4. **Compare to the reference** (if any): per dimension, is the build **≥** the reference? Name anything the
   reference does better and close the gap; name anything you can do better and take it.
   Compare against the matching files under `assets/illustration-style/`: soft neutral depth, restrained
   avatar/assistant system, compact hierarchy, paper speech surfaces, yellow inline highlights, and one clear
   reading path. Copy their shared visual grammar, never their literal content or Korean text.
5. **Fix the worst first, re-render, re-score.** Iterate until every dimension passes and nothing is weaker
   than the reference.

## Look at the render — the named checks the gate cannot make

A gate pass is a floor, not a verdict. Three separate changes have now passed every automated check
while looking visibly worse, and each time only the screenshot caught it. That is not a threshold
that needs tuning: nine geometric measures were scored against 37 human-labelled A/B pairs and **none
of them predicted which slide a person preferred**. The differences that decide a slide are not
geometric, so this step cannot be automated away.

Open the PNG and answer these, in order. They are the failure modes actually observed, not a
generic checklist:

1. **Is any container mostly empty?** A card drawn taller than its contents reads as a hollow void,
   not breathing room. Shrink it, fill it, or distribute it.
2. **Is content flung to a container's edges?** Label at the top, body at the bottom, a hole in the
   middle. This is the one that passed the gate at 34% whitespace and read as broken.
3. **Do the header and its content read as one block?** If the header is stranded at the top with a
   gap under it, bring it down against its content and let the leftover become even margin.
4. **Does the accent appear more than twice?** One chromatic accent, on the single load-bearing word.
5. **Is emphasis carried by ink or by fill?** Prefer accented type; paint a surface only when it also
   supplies mass a sparse slide needs. `python scripts/check_style_rules.py SLIDE.html` gives a
   second opinion on 4 and 5, and it is advisory — the slide's intent can overrule it.
6. **Would the English line still fit if it ran 150% longer than the 繁中?** Bilingual pairs expand.

If a change makes a metric better and the render worse, the render wins. Revert it.

## What "better or same as the reference" means
- **Same:** same intention, same-or-cleaner hierarchy, same density comfort, same craft — in our theme +
  繁中/English.
- **Better:** tighter 4-color discipline (no stray hues the reference used), a plainer title, better
  balance/proportion, on-system illustration where the reference used off-palette art.
- **Never copy the reference's flaws.** Keep its strengths; fix its weaknesses (e.g. multi-hue category
  coding → neutral surface tints + one accent). "Match" is about quality of communication, not imitation.

## Output
A short self-critique note before delivery: per-dimension **pass / fix**, plus **vs reference: ≥ / gap +
fix** for each. Deliver only when every dimension passes and the build is ≥ the reference.
