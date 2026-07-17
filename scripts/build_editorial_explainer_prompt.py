#!/usr/bin/env python3
"""Build a strict, variant-aware prompt for the editorial explainer generator."""

from __future__ import annotations

import argparse


COMPOSITIONS = {
    "agenda-dialogue": (
        "A slim rounded timing/step rail on the left. On the right, two vertically stacked participant "
        "questions with small circular human avatars and assistant answers in large rounded speech surfaces."
    ),
    "guided-dialogue": (
        "Use a compact progress/context rail on the left and one or more human-to-assistant exchanges on "
        "the right. Reserve clean speech surfaces for native editable prompts, assistant actions, approval "
        "moments, and the governed outcome. The page should feel like a worked example, not a chat transcript."
    ),
    "workflow-transform": (
        "Scattered speech notes, constraints, expectations, and small human avatars on the left flow via "
        "dotted connectors and a restrained assistant into one organic white central workflow capsule with "
        "three stacked transformation steps, then resolve into a clear output card and aligned people on the right."
    ),
    "ui-qa": (
        "Place the supplied real product screenshot on a quiet left panel. On the right, show two participant "
        "questions and assistant interpretations with compact highlighted phrases. Do not redraw or invent the UI."
    ),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", required=True, choices=COMPOSITIONS)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--intention", required=True)
    parser.add_argument("--aspect", default="16:9")
    parser.add_argument("--accent", default="clear blue")
    parser.add_argument("--native-copy-zones", default="headline and speech/card interiors")
    args = parser.parse_args()

    print(
        f"""Create a brand-new editorial explainer illustration about: {args.topic}.

Intention: {args.intention}
Variant: {args.variant}
Reference role: use the supplied matching references only for shared visual grammar and art direction. Do
not copy, return, crop, trace, or lightly edit any reference. Generate a genuinely new composition.

Composition: {COMPOSITIONS[args.variant]}

Shared style: soft neutral radial depth, compact editorial hierarchy, rounded white paper/speech surfaces,
gentle shadows, generous negative space, simple circular human avatars, and a restrained blue robot assistant.
Preserve colour: {args.accent} key phrases/assistant, sparse teal/orange/lavender avatar rings, and pale-yellow
inline highlights. Do not make the result grayscale.

Text mode: leave clean empty zones for native editable copy at {args.native_copy_zones}. Do not generate
random words, pseudo-text, Korean, logos, watermarks, fake UI, or invented facts.

Output: exact {args.aspect} aspect ratio, edge-to-edge full-block artwork with no side gutters. Keep every
meaningful object inside a 6% safe zone. Avoid dashboards, glossy 3D, glossy gradients, thick borders, giant
type, neon/rainbow palettes, decorative checklists, and heavy shadows."""
    )


if __name__ == "__main__":
    main()
