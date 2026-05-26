# Source Analysis

Use this file when matching the design direction from the downloaded Pinterest board and the existing `bonny8000/bonnyt` skill.

## Inputs Reviewed

- Pinterest board: `https://www.pinterest.com/30237old/kr/`
- Local image set: `pinterest-kr-pins`, 64 downloaded images.
- GitHub source: `bonny8000/bonnyt`, commit `4a17661b7db032684140a523007383119eb55431`.
- Installed prior skill: `C:\Users\bonny_chen\.codex\skills\bonny-slide-system`.

## Pinterest Board Findings

The board is dominated by Korean UX/product case-study references. The visual language is not one fixed template; it is a reusable family of research, insight, solution, and result pages.

Observed distribution from the local image set:

- 64 board images downloaded.
- 59 of 64 are wide landscape or slide-like references.
- 41 are visually light, 16 are dark, and 7 are mid-tone.
- File formats: 31 PNG, 23 WebP, 10 JPG.
- Main source domains: Behance, Codeit Sprint, Notefolio, uploaded user images, and BYSU PPT.

## Repeated Design Moves

- Large headline plus smaller explanatory paragraph at top-left or centered.
- Small uppercase or category label in accent color.
- Soft white cards on pale gray canvas for evidence, background, and survey slides.
- Strong dark canvas for insight, interview, product walkthrough, and result slides.
- Three-card grouping for pain points, evidence, service principles, or key features.
- Two-column comparison for current/future, problem/opportunity, or user/admin views.
- Phone mockup as the hero when explaining app or mobile service behavior.
- Quote bubbles and chat-style cards for interview or pain-point evidence.
- Blue accents for research/data, green for improvement/product solution, purple for social/motivation, orange/yellow for attention or study themes, pink/red for friction or pain.
- Rounded cards, but usually as evidence containers, not as decorative page sections.
- Dotted lines, arrows, or callout dots appear only when they explain relationships.
- Large metric/result slides use dark backgrounds and bright green/blue numbers.

## Component Lessons From References

The best references vary the component by situation:

- Background slides use evidence cards and chart cards, not phone mockups.
- Interview slides use quotes, participant tags, and repeated-pain grouping, not raw paragraph blocks.
- Pain slides use a triad or problem-to-opportunity structure so the deck can move forward.
- Solution slides show the before/after or mechanism of change, not just a list of benefits.
- Feature slides use a product screen plus annotations; screenshots alone are not enough.
- Result slides require baseline labels, periods, and explanation of what changed.

## What `bonny8000/bonnyt` Already Does

The repo already has a good first structure:

- A compact `SKILL.md`.
- Separate references for typography, color/mode, layout patterns, component decision rules, and source observations.
- A CSS token file and HTML template.
- A lightweight HTML validation script.
- Legacy v1 examples and preview assets.

## Gaps In The Previous Version

The previous version is useful but under-specified for agents:

- Component rules are mostly "use this for that" and do not define anatomy, variants, required data, or anti-patterns.
- Layout patterns are broad; an agent still has to infer exact structure and component combinations.
- The skill does not clearly tell an agent how to convert source material into an outline, component map, and validation plan.
- Legacy v1 assets include useful spacing, card, tag, and callout ideas, but some legacy text has encoding issues; v2 should preserve structural lessons, not reuse broken text.
- The CSS tokens do not yet encode enough component-level classes for repeated slide work.

## V2 Direction

V2 should be stricter and more operational:

- Define foundations: canvas, grid, type, spacing, color, surfaces, shadows, and content writing.
- Define components by anatomy, variants, and when to use or avoid each one.
- Define slide recipes for common UX portfolio situations.
- Define agent behavior: classify, select recipe, map components, draft slide, validate, report.
- Keep `SKILL.md` concise and push detailed rules into references.
