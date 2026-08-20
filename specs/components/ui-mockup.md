---
id: ui-mockup
kind: component
tier: molecule
status: stable        # example built + render-validated
intent: show the real product UI as a visual so claims feel concrete
triggers: [product shot, app/dashboard screen, phone mockup, skeleton placeholder UI, a screen to point at, 介面示意, 畫面示意圖, app 畫面, 화면 목업]
depends_on: [tokens]
tokens_used: [surface, muted, muted-soft, ink, accent]
icon_use: optional
learned_from: Img19, Img21
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

Variants: **browser-dashboard · phone · skeleton-cards · list-screen · tab-screen · sheet-screen**.

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

The vocabulary follows [daangn/seed-design](https://github.com/daangn/seed-design) (Apache-2.0),
whose component inventory is a good census of what a real mobile screen actually contains. The
anatomy is borrowed; the CSS is re-implemented from this system's tokens, so a mockup always matches
the deck's theme and never introduces a colour of its own.

## Tokens used
surface (frame + cards), muted-soft (skeleton bars, chrome), muted (secondary labels), ink (key labels),
accent (active element).

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
(learned from Img19, Img21).
