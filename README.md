# Bonny Slide System

Bonny Slide System is a Codex skill for creating and reviewing bilingual UX/product slide decks in Bonny's editorial portfolio style. It is designed for Traditional Chinese primary content with English support text, and it gives agents clear rules for choosing slide components by situation.

## What It Helps With

- UX research and product case-study decks
- Research, problem, insight, solution, workflow, and result slides
- HTML or PPTX-style 16:9 slide templates
- Slide design-system critique and redesign
- Agent-facing guidance for selecting components, modes, colors, and layouts

## Design Direction

The current version is V2. It replaces the older broad rule set with a more explicit system:

- Choose the slide intent first.
- Pick components by content job, not decoration.
- Use light mode for evidence and explanation.
- Use dark mode for insights, product walkthroughs, and result dashboards.
- Keep CJK and Latin typography separate.
- Include source, method, baseline, or context labels when claims depend on evidence.

## Structure

```text
SKILL.md
agents/openai.yaml
assets/
  bonny-slide-v2-tokens.css
  templates/slide-template.html
references/
  agent-playbook.md
  component-system.md
  foundations.md
  slide-recipes.md
  source-analysis.md
scripts/
  check_slide_html.py
```

## How Agents Should Use It

1. Read `SKILL.md` to understand the workflow.
2. Load `references/foundations.md` and `references/component-system.md` for every slide task.
3. Load `references/slide-recipes.md` when creating a deck or mapping source material into slides.
4. Load `references/agent-playbook.md` when deciding how to classify content and report design choices.
5. Use `assets/templates/slide-template.html` and `assets/bonny-slide-v2-tokens.css` for HTML slide work.

## Validation

Validate the skill folder:

```bash
python path/to/skill-creator/scripts/quick_validate.py .
```

Validate an HTML slide:

```bash
python scripts/check_slide_html.py assets/templates/slide-template.html
```

## Notes

This repo is the source package for the `bonny-slide-system` skill. Keep the frontmatter name in `SKILL.md` as `bonny-slide-system` so existing Codex skill triggers continue to work.
