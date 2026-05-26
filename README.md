# Bonny Slide Design System

A design system for building **bilingual UX/product case-study slides** in Bonny's editorial portfolio style. Optimized for **Traditional Chinese as primary voice** with **English as supporting labels, subtitles, captions, and metrics**. Built for 16:9 surfaces (`1920 × 1080` HTML or widescreen PPTX), with stricter component rules than a generic deck template so an agent can pick layouts by content intent, not by decoration.

> **The core promise:** every slide is a clear, well-laid-out argument made of named components. Use whichever accent color makes sense for the message, but the **structure, type, spacing, and component vocabulary stay consistent** — so a deck mixed from many slide types still reads as one coherent set.

## Sources

This design system is derived from the **bonny8000/bonnyt** Codex skill plus a Pinterest reference board of Korean UX portfolio slides. Explore the originals to do a better job designing with this system:

- GitHub repo: <https://github.com/bonny8000/bonnyt>
- Pinterest board: <https://www.pinterest.com/30237old/kr/>
- Files imported from the repo live under `references/` and `assets/` in this project — they are the original Codex source of truth.

---

## Index

```
README.md                       ← you are here
SKILL.md                        ← Agent Skills cross-compat entry
colors_and_type.css             ← base color + type tokens (root-level vars)
assets/
  bonny-slide-v2-tokens.css     ← full slide-component token sheet
  templates/slide-template.html ← minimum-viable slide shell
references/
  foundations.md                ← canvas, grid, type, spacing, color, mode
  component-system.md           ← every component's anatomy + variants + rules
  component-html.md             ← copy-paste HTML for each component
  slide-recipes.md              ← intent → component map for common slide jobs
  agent-playbook.md             ← how an agent classifies, picks, builds, validates
  source-analysis.md            ← what the reference board taught us
scripts/
  check_slide_html.py           ← (from upstream) validate an HTML slide
preview/                        ← design-system cards (one concept per file)
slides/                         ← sample slides — one HTML file per intent
ui_kits/
  slides/                       ← React/JSX recreations of the slide components
fonts/                          ← Inter + Noto Sans TC (loaded via Google Fonts CDN)
```

---

## Content Fundamentals

### Voice

**Editorial, evidence-led, calm.** Slides describe what the team found, then what they decided. Never marketing language. Never exclamation marks. Headlines are full sentences that state an argument, not category labels.

> 늘어나는 모빌리티 서비스 수요와 코레일톡의 방향 → in the system this becomes →
> 用戶意圖明確，但<span class="accent-blue">行動轉換率持續下降</span>

### Casing

- **CJK headlines** in Traditional Chinese, weight 700, with **one** phrase or metric highlighted via `.accent-*`.
- **English support lines** in `Title Case` for product names and method labels (`Online survey · N=320`), `UPPERCASE` for eyebrows (`DESK RESEARCH`, `INSIGHT 02`).
- Numbers stay in Latin font with no tracking — `88%`, `+34%p`, `19.9% increased`.

### Person

Mostly **third-person / observational** ("Users repeatedly mentioned…", "在第一步就放棄"). First-person plural ("we / 我們") only on principle slides and next-step bands.

### Tone examples (from the reference board)

| Slide intent | Headline shape |
|---|---|
| Context / background | `成長中的市場 + 為什麼現有服務不足？` |
| Pain point | `當前系統無法<accent>快速反映</accent>客戶需求` |
| Insight | `使用者並非不願意，而是<accent>沒有足夠的信心</accent>` |
| Result | `任務完成率<accent>+34%</accent>，回訪率提升 2.1x` |

### Emoji & decorative characters

**Sparingly.** The reference board uses:
- 3D illustrated emoji or sticker characters on warm/empathy slides only (pain-with-avatar variants).
- Unicode arrows (→, ↗, ↘) inside next-step bands.
- No emoji in formal client / report slides; no emoji as bullet markers.

### Compression rules

- Raw paragraph → headline + 2 cards.
- 5 quotes → 3 quote patterns with one highlighted repeated phrase.
- Feature list → 3 feature outcomes.
- Dense metrics → 1 hero metric + 2 supporting.
- Workflow → 4 stages max on one slide.

---

## Visual Foundations

### Canvas

- HTML slide is a **fixed `1920 × 1080`** with margins `104px × 72px` (standard), `88 × 64` (dense), or `128 × 96` (sparse cover).
- 12-column grid, `28px` gutters. Content usually spans 10–12 columns.
- Three zones: Header `72–210px`, Evidence `240–900px`, Footer `920–1008px`.

### Color

- One **accent family per slide** unless explicitly comparing categories or actors.
- Light canvas (`#F6F8FB`) for evidence, comparison, MVP explanation, report pages.
- Dark canvas (`#101418`) for emotional interview findings, insight reveal, product walkthrough, result dashboards.
- Accents are **semantic** — see `references/foundations.md`:
  - Blue → research / data / product clarity
  - Green → improvement / success / service simplification
  - Purple → social / motivation / friendly AI
  - Orange / yellow → attention / study / warm service
  - Pink / red → friction / pain / warning
  - Gray → baseline / inactive / current state

### Type

Two-language stack, two letter-spacing values, no overlap:

| Role | Family | Tracking | Heaviest weight |
|---|---|---|---|
| Traditional Chinese | **思源黑體** (Noto Sans TC / Source Han Sans TC) | `0.10em` | 600 |
| English / numbers / product names | **Arial** | `0` | 600 |

Default line-height `1.5`; dense chart labels `1.25–1.35`. **Title weight tops out at 600** — no heavy 700 — so the editorial voice stays calm. **Always mark CJK and Latin runs separately** with `.cjk` / `.latin` (or `:lang()` containers).

### Backgrounds

Mostly **flat solid surfaces** — `#F6F8FB` for light, `#101418` for dark. No decorative gradient blobs, no abstract atmosphere stock. **Exception:** cover slides may use one full-bleed photographic background with a darkening overlay (see `slides/01_cover.html`). Pain & insight slides occasionally use a darkened photo background with the canvas at ~85% opacity.

### Borders & shadows

- Standard card: `border-radius: 24px`, `border: 1px solid rgba(152,162,179,.18)`, `box-shadow: 0 16px 40px rgba(15,23,42,.08)`.
- Dense dashboard: `16px` radius, prefer borders over shadows.
- Dark mode: shadow becomes `0 18px 50px rgba(0,0,0,.28)`, border drops to `rgba(255,255,255,.08)`.
- Pills: `border-radius: 999px`.

### Spacing

8-based scale: `8, 12, 16, 20, 24, 32, 40, 48, 64, 80`. Title-to-content gap is `48–72px`. Card gaps `28–40px`. Section gaps `48–80px`.

### Animation, hover, press

Slides are **static** by default — they print to PPTX and PDF. The only on-screen motion is the page-turn between slides handled by the host. When a slide is opened in a click-thru prototype:
- Hover on a card: shadow deepens to `0 22px 48px rgba(15,23,42,.10)`, ~120ms ease-out.
- Press state on interactive elements: scale `0.98`, 80ms.
- No bounces, no parallax, no decorative entrance animations.

### Transparency & blur

Reserved for two cases:
1. Glass-panel overlays on cover/insight slides where a photo sits behind (e.g. `rgba(255,255,255,.65)` + `backdrop-filter: blur(12px)`).
2. Light "soft" surface variants like `--blue-soft`, `--green-soft`, `--pain-soft` — these are flat opaque pastels, not transparent.

### Imagery vibe

When real imagery is used, it is **cool-toned, sharp, modern**. No grain, no warm filters. App screenshots are shown at native resolution inside a `phone` mockup with `12px` bezel and `42px` radius. 3D / claymorphic icon assets appear on cover and MVP slides only.

### Iconography

See **ICONOGRAPHY** section below.

---

## Iconography

The reference board mixes several icon families across different decks — there is **no single brand icon set**. The system codifies this as four allowed approaches, in priority order:

1. **Real product screenshots** for any feature slide. Crop tightly. Use `phone` mockup.
2. **Lucide** (`https://unpkg.com/lucide@latest`) as the default UI icon set when an icon is genuinely informational — feature stack rows, timeline stage markers, severity badges. 24px stroke, `1.75` weight. Loaded via CDN; no need to copy into the project.
3. **3D illustrated icons / claymorphic stickers** for cover and MVP slides — copy real PNG assets when available; never hand-draw with SVG. The reference board uses pieces from Microsoft Fluent Emoji and various 3D icon kits. Until real assets are provided, slides leave a labeled placeholder rectangle.
4. **Unicode arrows and connector glyphs** — `→ ↗ ↘ ↓ ‣` inside next-step bands and bridges. Always paired with a real label.

**Emoji** appear only as embedded characters inside quote bubbles (e.g. `🙁 🤔`) on warm interview slides — never as data labels or section markers.

**Logos.** No "Bonny" wordmark exists yet — the system has no proprietary brand mark. Slides identify themselves with a small `eyebrow` + a `footer-bar` page marker instead of a top-right logo. If a Bonny wordmark is created later, drop it in `assets/logo/` and reference it from `slides/01_cover.html`.

> ⚠️ **Substitutions flagged:** Lucide is a substitute for the unspecified Korean UX-portfolio icon style observed on the reference board. If you have a specific icon kit in mind, drop SVGs into `assets/icons/` and update this section.

---

## Skill use

Read `SKILL.md` for the Agent Skills entry, then `references/foundations.md` + `references/component-system.md` for every slide task. Use `references/component-html.md` as the copy-paste source for HTML snippets — **never invent class names**.

## Known caveats

- **Fonts:** loaded from Google Fonts CDN. For offline / PPTX export, install Noto Sans TC and Inter locally and the system falls back to Microsoft JhengHei / PingFang TC.
- **No "Bonny" logo or proprietary icon set** is provided. The system relies on real product screenshots, Lucide, and Unicode glyphs. Flag this to the user if a brand mark is required.
- **The original repo's `SKILL.md` references `Codex` validation.** The included `scripts/check_slide_html.py` still works; it's not required to use this system.
