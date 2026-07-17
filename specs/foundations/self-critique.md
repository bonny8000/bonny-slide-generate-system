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
2. **Score each dimension** (pass / fix):
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
3. **Compare to the reference** (if any): per dimension, is the build **≥** the reference? Name anything the
   reference does better and close the gap; name anything you can do better and take it.
   Compare against the matching files under `assets/illustration-style/`: soft neutral depth, restrained
   avatar/assistant system, compact hierarchy, paper speech surfaces, yellow inline highlights, and one clear
   reading path. Copy their shared visual grammar, never their literal content or Korean text.
4. **Fix the worst first, re-render, re-score.** Iterate until every dimension passes and nothing is weaker
   than the reference.

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
