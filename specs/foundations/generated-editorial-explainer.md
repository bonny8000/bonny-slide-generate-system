---
id: generated-editorial-explainer
kind: foundation
status: stable
learned_from: Img39, Img40, Img41, Img42, Img43
last_synced: 2026-07-15
---
# Generated editorial explainer

Use this route when a slide is clearer as a humanized editorial explanation than as native cards alone.
This is a **real image-generation workflow**, not a diagram recipe.

## Composition variants
Choose exactly one by intention:

1. **`agenda-dialogue`** — a slim left timing/step rail plus two facilitator/assistant Q&A blocks. Use for
   workshop rules, rounds, breaks, prompts, grouping, voting, and discussion.
2. **`guided-dialogue`** — a compact progress rail or context card plus one or more human/assistant exchanges.
   Use for chat-driven worked examples, owner approval loops, agent-assisted operations, and “say these lines”
   instruction pages outside workshops.
3. **`workflow-transform`** — scattered inputs and avatars on the left, an assistant transition, one organic
   central workflow capsule, then a shared-direction/output card on the right.
4. **`ui-qa`** — a **real supplied screenshot** on the left and a participant/assistant interpretation on the
   right. Use for onboarding, locked states, hierarchy, likely actions, or research interpretation. Never
   generate or fabricate the product UI.

Reject all variants for precise data, dense comparisons, or evidence that must remain directly inspectable.

## Canonical references
- `agenda-dialogue`: `editorial-workshop-grouping.png`, `editorial-workshop-crazy8.png`,
  `editorial-workshop-categorization.png`
- `guided-dialogue`: `editorial-workshop-grouping.png`, `editorial-workshop-categorization.png`
- `workflow-transform`: `workflow-intent-reference.png`
- `ui-qa`: `editorial-ui-qa.png` plus the user's real screenshot as content reference

All live under `assets/illustration-style/`. Together they establish soft neutral radial depth, compact dark
type, rounded white paper/speech surfaces, small teal/orange/lavender human avatars, a restrained blue robot,
blue key phrases, pale-yellow inline highlights, gentle shadows, generous negative space, and a clear reading
path. The references are **style/layout only**. Never return, crop, trace, or lightly edit them. Image43 may
contain Korean; learn structure only and always output Traditional Chinese + supporting English.

## Required generator workflow
1. Create `illustration-plan.json` beside the deck and record **every slide**, including `gate: no` pages.
   Every record must include `trigger`, `hard_candidate`, `gate`, and `reason`. A hard candidate may use
   `gate: no` only with one explicit precision override: `precise-table`, `data`, `code`, `evidence`, or
   `real-ui-detail`. For a generated page also record its variant, target dimensions, native-copy zones,
   local asset path, matching references, and `generator: built-in-imagegen`. Use
   `../editorial-explainer-plan.example.json` as the canonical contract.
2. Run `scripts/build_editorial_explainer_prompt.py --variant …` with the topic, intention, ratio, and copy zones.
3. Load the `imagegen` skill and invoke the built-in image-generation tool. Pass only the matching canonical
   variant references through `referenced_image_paths`; for `ui-qa`, also include the real screenshot.
4. Generate a **fresh composition**. Prefer textless/short-label surfaces so exact copy can be native/editable.
5. Generate at the target block's exact ratio with meaningful objects inside a 6% safe zone.
6. Save under the deck, e.g. `assets/generated-illustrations/NN-editorial-explainer.png`.
7. Run `scripts/validate_generated_illustration.py IMAGE --aspect W:H`; reject wrong-ratio or grayscale output.
8. Place at `width:100%; height:100%`. No `object-fit:contain`, side gutters, grayscale, or desaturation.
9. Render at 1920×1080 and compare against the selected reference family.
10. Run `scripts/validate_editorial_explainer_plan.py illustration-plan.json DECK.html`. Delivery is blocked
    if any slide is missing, a `gate: yes` asset is absent, provenance is not built-in imagegen, or the HTML
    lacks the matching asset and `data-editorial-explainer` variant.

## Mandatory gate triggers
Default to `yes` for human/assistant dialogue, assistant-operated workflows, workshop facilitation,
multi-person inputs converging into one decision, and multi-tool handoffs where the audience benefits from
seeing who does what. Use `no` only when inspectable precision (table, data, code, real screenshot detail)
is more important than the human explanation. If generation is unavailable after a `yes`, stop; do not
replace it with HTML cards, an SVG diagram, or a canonical reference image.

Use this tie-breaker when two variants seem plausible:
- **system-level handoffs across people and tools** → `workflow-transform`
- **turn-by-turn prompt, action, review, or approval** → `guided-dialogue`

If one source page contains both a hard-candidate workflow and a precise table, split it into two slides:
generated overview first, native evidence second. Do not use the table as a reason to suppress the overview.

## Prompt invariants
- State the intention, audience takeaway, variant, and reference-as-style-only rule.
- Preserve the shared visual system; vary composition only through the four sanctioned variants.
- Preserve restrained teal/orange/lavender avatar rings, blue assistant/key phrases, and pale-yellow highlights.
- Leave planned native-copy zones empty; prohibit random text, pseudo-text, Korean, logos, and watermarks.
- Require exact ratio, edge-to-edge fill, 6% safe zone, and no gutters.
- Avoid dashboards, glossy 3D, heavy shadows, thick borders, giant type, neon/rainbow palettes, and fake UI.

## Audit
Gate fit · correct variant · real generator invocation · fresh output · correct references passed · exact ratio ·
full-block fill · colour preserved · native copy fidelity · local persistence · no reuse/trace/CSS/SVG substitute.
