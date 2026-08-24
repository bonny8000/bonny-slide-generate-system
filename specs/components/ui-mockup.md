---
id: ui-mockup
kind: component
tier: molecule
status: stable        # example built + render-validated
intent: show the real product UI as a visual so claims feel concrete
triggers: [product shot, app/dashboard screen, phone mockup, skeleton placeholder UI, a screen to point at, screen interior, dashboard overview screen, checkout screen, settings screen, empty state screen, component specimen sheet, 介面示意, 畫面示意圖, app 畫面, 畫面內部, 儀表板畫面, 結帳畫面, 設定畫面, 空狀態畫面, 화면 목업, 화면 내부]
depends_on: [tokens]
tokens_used: [surface, muted, muted-soft, ink, accent]
icon_use: optional
learned_from: Img19, Img21, screen-interiors
example: examples/light-product-hero.html
---
# ui-mockup

## Purpose
A framed product UI — browser window, phone, or card stack — standing in for the real screen.

## Intention & rationale
The job is to **make the product tangible**. Why this form:
- **A recognizable product shot proves the thing exists** and is usable — stronger than a description.
- **Skeleton placeholder bars** (`--muted-soft`) for body content keep the eye on *structure*, not on
  fake/unreadable data; real labels only on the headers that matter.
- **One `--accent`** marks the single active element (selected tab, highlighted row).

## When to use / When NOT
Use inside `product-hero` / `feature-showcase` to show a screen. **Not** as a decorative frame around
unrelated content.

## Structure
A `--surface` frame (browser chrome / phone bezel / floating cards) holding a simplified UI: real header
labels + **skeleton bars** for content.

Variants — chrome: **browser-dashboard · phone · skeleton-cards · list-screen · tab-screen · sheet-screen**.
Variants — interior: **overview · form-summary · rail-rows · table · empty · specimen** (below).

### App-screen furniture
A schematic screen reads as a real app when its **chrome** is right, not when its content is detailed.
`base.css` ships the anatomy: `.appbar` (back chevron, title, actions), `.tabbar` and `.segbar`
(section switching), `.listrow` with `.toggle`, `.sheet` (a bottom sheet with its grab handle),
`.banner` (inline notice, with `.warn` / `.neg` / `.pos`), `.fab`, and `.badge` / `.badge.dot`.

Label the chrome — an app bar title, two or three tab names — and leave everything below it as `.sk`
skeleton bars. That is what keeps the eye on structure. A screen full of invented rows and plausible
numbers is both harder to read and a claim about a product that may not be true.

- **list-screen** — `.appbar` + repeated `.listrow`, one `.toggle` or `.badge` marking the state
  being discussed.
- **tab-screen** — `.appbar` + `.tabbar`/`.segbar` with one `.on`, skeleton content beneath.
- **sheet-screen** — any of the above with `.sheet` raised over it, for a decision or confirmation
  moment.

All of it is built from this system's own tokens, so a mockup always matches the deck's theme and
never introduces a colour of its own.

### Screen interiors
Chrome says which **product** a mock is. The interior says which **screen**. That is a separate
decision and it is the one that usually gets skipped — a frame with undifferentiated `.sk` bars
inside reads as "some app", which is exactly the vagueness a mockup was supposed to remove.

An overview, a checkout and a settings page are each recognisable from across a room by their
skeleton alone. So the *arrangement* carries the recognition, and no invented data is needed to
get it — the same reason this component already prefers `.sk` bars to tiny fake text, moved up
from the content level to the layout level.

`base.css` C17 ships six interiors. Each is a shape, not a screenshot:

| interior | what makes it legible | built from |
|---|---|---|
| **overview** | one dominant number above a bar row, exactly one bar accented | `.ui-metric` + `.ui-bars` / `.ui-bar.on` |
| **form-summary** | stacked inputs in a column against a fixed side panel, single action bottom-right | `.ui-split` + `.ui-field` + `.ui-panel` + `.ui-cta` |
| **rail-rows** | a side rail with one item lit, rows with end-aligned controls | `.ui-rail` / `.ui-railitem.on` + `.ui-tr` + `.toggle` |
| **table** | zebra rows on a fixed left gutter, one row marked | `.ui-tr.alt` / `.ui-tr.on` |
| **empty** | a mark, two short lines, one action, centred | `.ui-empty` |
| **specimen** | variants down, states across, undefined combinations left blank | `.ui-matrix` + `.ui-cellbox` |

Pick the interior from **what the slide is arguing about**, not from what looks fullest. A slide
about a drop-off does not want a `specimen`; a slide about component drift does not want an
`overview`. If none of the six fits, the honest move is a plain `.ui-body` of `.sk` bars — an
interior that misrepresents the screen is worse than one that stays generic.

One accent per frame, on the single element the slide is about. Two accents inside one mock and
the audience has to work out which one you meant.

**Text inside a mock screen uses the UI scale, not the slide scale.** Slide type runs 14–150px
because it is read across a room; text drawn inside an interface is read as an *image* of an
interface, so it uses `--fs-ui-1`…`--fs-ui-5` (11/12/13/14/16px) paired with the `--lh-ui-` token of
the same number, and a weight from `--fw-regular` / `--fw-medium` / `--fw-bold`. Size and line-height
travel together; weight stays an independent choice. Never set a raw px size on mock UI text — that
is how a mockup drifts out of the system.

**A `.phone` is a scaled device, so its interior is measured in points.** `--uis` is one iOS point at
that mock's size — a real iPhone is 390pt wide, so `calc(width / 390)` converts any Apple spec
straight across. The frame is 390×844, the nav bar 44pt sitting under a 59pt status inset, the
dynamic island 125×36pt, a switch 51×31pt, a list row 44pt, body type 17pt.

Setting absolute px inside a phone is what makes a mockup look wrong at a glance, and it is hard to
name when you see it: shrink the frame to fit a slide and the type does not shrink with it, so the
proportions stop reading as a real screen even though every individual element looks fine. Size
everything from `--uis`, or in `em` off the screen's font-size, and a mock is accurate at any width.

**The status area belongs to the device, not the app.** Phones have a floating dynamic island, not a
notch cut into the top edge, and the app bar reserves the status inset so the island never lands on a
title. `base.css` handles both; do not override the padding.

`.appframe` and `.mock` are different — they stand in for desktop or card UI shown at 1:1, so they
use the absolute `--fs-ui-*` scale directly with no device conversion.

## Tokens used
surface (frame + cards, interior panels + zebra rows), muted-soft (skeleton bars, chrome, fields,
rail items), muted (secondary labels), ink (key labels, the dominant number), accent (active
element — one per frame), accent-soft (a lit rail item or marked row).

## Icon use
Optional small UI glyphs, one style.

## Color
Chrome + placeholders in muted tints; one accent for the active element; differentiate multiple screens by
**surface tone**, not new hues.

## Do / Don't
- **Do** use skeleton bars instead of tiny unreadable text.
- **Don't** introduce new hues for screens or fake precise data.

## Example
A dashboard with "發注現況 / 庫存管理 / 客戶管理" cards using skeleton rows; a phone showing a profile screen
(learned from Img19, Img21). Interiors: `examples/light-screen-interiors.html` — overview,
form-summary and rail-rows side by side in `.appframe` chrome.
