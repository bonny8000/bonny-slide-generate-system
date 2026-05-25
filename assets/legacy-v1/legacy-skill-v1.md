# Bonny's Slide Design Tokens & Style Guide

> **Purpose**: The authoritative reference for generating any `.pptx` slide deck for Bonny. ALWAYS read this file before writing any slide generation code.
> 
> **Source**: Extracted from 90+ slides across 4 decks (跨域agent 23p, ROG UX Review 52p, Elite & ASUS 7p, high-res originals 9p).

---

## 1. Global Canvas

| Token | Value |
|-------|-------|
| Slide dimensions | 1920 × 1080 px (16:9 widescreen) |
| Background color | `#FFFFFF` (pure white) — used for ~90% of slides |
| Light tint background | `#F5F5F5` very light gray — behind swimlane flow areas |
| Dark-background pages | `#2B3A4E` navy / `#1E2A3A` deep navy — ROG data-dense slides, persona cards, emphasis |
| Grid system | Loosely two-column or asymmetric split (≈40/60 or 50/50) |

---

## 2. Color Palette

### 2.1 Primary Colors

| Role | Hex | Usage |
|------|-----|-------|
| **Primary text** | `#333333` / `#2D2D2D` | All body text on white backgrounds |
| **Section header accent** | `#2B7A78` / `#1B8A6B` | Green vertical bars, section labels, "Phase" indicators |
| **Link / emphasis blue** | `#0077B6` / `#2980B9` | Hyperlinks, "檢視完整的 Sitemap" style CTAs |
| **Dark navy background** | `#2B3A4E` / `#1E2A3A` | Dark-bg content slides, tables, summary blocks, insight callout bg |
| **Navy text on white** | `#2C3E6B` / `#34495E` | Slide titles on overview/context slides (ROG deck) |

### 2.2 Accent / Functional Colors

| Role | Hex | Usage |
|------|-----|-------|
| **Green tag / badge** | `#27AE60` / `#1B8A6B` | "可以做到…" indicator, status checkmarks, positive, Backend lane labels |
| **Red / coral callout** | `#E74C3C` / `#C0392B` | Warning/limitation callout boxes, "還做不到" blocks, red ✗, Agent lane labels |
| **Orange badge** | `#E67E22` / `#F39C12` | Category tags "資料授權深度", orange-bordered swimlane nodes, table category labels |
| **Teal badge** | `#008B8B` / `#17A589` | "協議開放程度" tags, secondary category markers |
| **Blue info badge** | `#2980B9` / `#3498DB` | "使用者行為" callout pills, User lane labels in swimlane, Samsung accent |
| **Muted gray** | `#95A5A6` / `#BDC3C7` | De-emphasized / faded-out quadrant items, disabled text |
| **Warm sand / cream** | `#F5E6D3` / `#FDF2E9` | Background tint on Amazon case study card |
| **Soft rose** | `#FADBD8` / `#F5CBA7` | Background tint on Dia / Lenovo case study cards |

### 2.3 Case Study Accent Theming

Each case study card uses a unique **accent color** applied consistently to the `/ section headers`, the `使用者價值` box background, and the left-card background tint:

| Case Study | Accent Color | `/` Header Color | Value Box Bg | Card Tint |
|------------|-------------|-----------------|-------------|-----------|
| Samsung Internet | Cool blue | `#2980B9` | Blue-gray `#7B95A8` | Light cool gray `#F0F2F5` |
| Sephora | Warm brown | `#8B6848` / `#A0522D` | Brown `#8B7355` | Warm tan `#F5EDE3` |
| Carrefour (ACP) | Gold-brown | `#8B6914` | Dark gold `#7B6B4A` | Light warm gray `#F2F0EC` |
| Dia Browser | Coral-red | `#C0392B` | Muted rose `#A06060` | Light rose `#FDF0EC` |
| PayPal × Perplexity | Warm gold | `#B8860B` | Teal-blue `#5F8A8B` | Light gray `#F0F0F0` |

### 2.4 Color Usage Rules

- **White dominates** — roughly 85-90% of all slide area is white or near-white
- **Color is surgical** — only for section markers (vertical bars), callout boxes, tags/badges, icon circles, and accent theming
- **Never use gradients** — all colors are flat/solid
- **Dark backgrounds are reserved** for: data tables, screenshots with dark UI, emphasis summary blocks, persona cards
- **Red callout boxes** always signal limitations or critical issues — never decorative
- **Green vertical bars** mark section/subsection headers — never used as background fill
- **Each case study gets its own accent** — never reuse another case's colors

---

## 3. Typography

### 3.1 Font Families

| Context | Font |
|---------|------|
| Chinese text | System default sans-serif — **Noto Sans TC** / **Microsoft JhengHei** (微軟正黑體) |
| English text | **Inter** / **Helvetica Neue** / system sans-serif — clean, geometric |
| Fallback | Arial, sans-serif |

### 3.2 Type Scale

| Element | Size (pt) | Weight | Color |
|---------|-----------|--------|-------|
| **Cover title** (Chinese) | 36-40pt | Bold (700) | `#333333` or `#000000` |
| **Cover subtitle / author** | 14-16pt | Regular (400) | `#666666` |
| **Section divider title** | 28-32pt | Bold (700) | `#333333` |
| **Section divider subtitle** | 13-14pt | Regular (400) | `#666666` |
| **Slide title** (content page) | 24-28pt | Bold (700) | `#333333` or `#2C3E6B` |
| **Phase / breadcrumb** | 11-12pt | Regular (400) | `#888888` (top-left, muted) |
| **Right-side category tag** | 11-12pt | Regular (400) | `#AAAAAA` (top-right) |
| **Section sub-header** (with green bar) | 16-18pt | SemiBold (600) | `#333333` |
| **`/` section header** (case study) | 14-16pt | SemiBold (600) | *accent color per case* |
| **Body text** | 13-15pt | Regular (400) | `#333333` / `#4A4A4A` |
| **Bullet list items** | 13-14pt | Regular (400) | `#4A4A4A` |
| **Tag / badge text** | 11-13pt | Medium (500) | `#FFFFFF` (filled) or `#333333` (outlined) |
| **Caption / source URL** | 9-10pt | Regular (400) | `#999999` / `#AAAAAA` |
| **Dark-bg body text** | 13-14pt | Regular (400) | `#FFFFFF` or `#E0E0E0` |
| **Callout box text** | 13-14pt | Regular (400) | `#FFFFFF` (on red/blue bg) |
| **Swimlane lane label** | 13-14pt | Medium (500) | *lane-specific color* (blue/red/green) |
| **Swimlane node text** | 12-13pt | Regular (400) | `#333333` |

### 3.3 Letter Spacing (Critical)

| Script | Letter-spacing | Note |
|--------|---------------|------|
| **Chinese (中文)** | **5%** (0.05em) | Applied to ALL Chinese text without exception |
| **English** | **0%** (normal) | No extra spacing |
| **Mixed CJK + Latin** | Chinese portions get 5%, English/numbers within stay at 0% | |

### 3.4 Line Height

| Context | Line-height |
|---------|-------------|
| Titles | 1.2 - 1.3 |
| Body text | 1.5 - 1.7 |
| Bullet lists | 1.6 - 1.8 (generous spacing between items) |
| Captions | 1.3 |

### 3.5 Text Alignment

- **Titles**: Left-aligned (never centered)
- **Body text**: Left-aligned
- **Tags/badges**: Center-aligned within the badge shape
- **Callout boxes**: Left-aligned inside the box
- **Source URLs**: Left-aligned, bottom of slide

---

## 4. Layout System

### 4.1 Margins & Padding

| Token | Value |
|-------|-------|
| **Left margin** | ~80-100px (≈0.8-1.0") from slide edge |
| **Top margin** | ~60-80px (breadcrumb sits here) |
| **Right margin** | ~60-80px |
| **Bottom margin** | ~40-60px |
| **Content-to-content gap** | 30-50px between major content blocks |
| **Bullet indent** | 20-30px from parent text |

### 4.2 Slide Structure Hierarchy

Every content slide follows this top-to-bottom structure:

```
┌──────────────────────────────────────────────────────────┐
│ [Breadcrumb]  (top-left, 11pt muted)    [Category tag]  │
│                                         (top-right, 11pt)│
│ [Slide Title]  (24-28pt bold, left-aligned)              │
│                                                          │
│ ┌── Content Area (varies by layout type) ──────────────┐ │
│ │                                                      │ │
│ └──────────────────────────────────────────────────────┘ │
│                                                          │
│ [Source URL / footnote]  (bottom, 9-10pt muted)          │
└──────────────────────────────────────────────────────────┘
```

### 4.3 Layout Templates (15 types)

---

#### Layout A: Cover Slide
- Pure white background
- Title: 36-40pt bold, positioned at ~40% vertical from top, left-aligned
- Author line: 14-16pt, directly below title, format: `Name｜Mentor: Name, Name`
- No decorative elements — extremely minimal
- Bottom 50% of slide is intentionally empty (breathing room)

#### Layout B: Section Divider
- Pure white background
- Title: 28-32pt bold, positioned at ~45% vertical, left-aligned
- Format: `Phase N｜章節中文名稱`
- Subtitle bullets (2-3 items): 13pt, listed below with `- ` prefix
- Generous whitespace — lower 40-50% is empty

#### Layout C: Context / Overview (Two-Column)
- Left column (~35-40%): Summary box with green vertical bar header
- Right column (~55-60%): Structured content with numbered phases (e.g., `Slide Context` / `Report Context`)
- Both columns start from same top baseline
- Content blocks separated by light horizontal lines or whitespace
- May include `資料來源` URL list at bottom-right

#### Layout D: Content Detail (Single Column)
- Full-width content area
- Green vertical bar marks each sub-section
- Bullet lists with `- ` prefix (not `•` for body, `•` only in certain contexts)
- Tags/badges inline with section headers
- Maximum 3 sub-sections per slide

#### Layout E: Case Study Card (Two-Panel) ⭐ Most distinctive layout

**Left panel (~42%)**:
- Card container with rounded corners (8-12px radius)
- Subtle drop shadow: `0 2px 12px rgba(0,0,0,0.08)`
- **Background tint** matching the case study accent color (see Section 2.3)
- Screenshot/image(s) inside the card — 1-2 product screenshots
- Below images: **Bold Chinese description title** (16-18pt bold)
- Below that: 2-3 line explanation paragraph (13pt)
- Bottom: Source URL in 9-10pt muted text

**Right panel (~53%)**:
- **Vertical timeline with dots**: Small filled gray circles (●, ~8px diameter) aligned vertically, one per section
- Three content sections, each with:
  - `/ Section Header` — forward slash prefix, **accent-colored text** (14-16pt semibold)
  - Body paragraph below (13-14pt, `#333333`)
- Section headers follow this fixed pattern:
  1. `/ 觸發點` — what triggers the user
  2. `/ 跨場域範圍` — cross-domain scope
  3. `/ Agent 主動行為` — agent proactive behavior
- **Bottom: `使用者價值` callout box**:
  - Sparkle/star icon (✦) + bold header "使用者價值"
  - Background: accent-tinted dark color (see Section 2.3)
  - Text: white, 13pt
  - Rounded corners 8px
  - Filled circle bullet (●) marker on the left side, vertically centered outside the box

**Top-right corner**: Small muted category tag (e.g., "User 觸發 X 自有 Agent")

#### Layout F: 2×2 / Quadrant Matrix
- Two axes forming a cross shape
- Horizontal axis: labeled at both ends (e.g., "自有平台內" ↔ "外部 Agent")
- Vertical axis: labeled at both ends (e.g., "User 主動觸發" ↔ "Agent 主動出擊")
- Center label in a rounded rect badge (e.g., "Chatbot [現有 AIA]")
- Four quadrants with bullet-listed items
- **Progressive highlighting**: when focusing on one quadrant, others fade to `#BDC3C7`
- Orange/teal badges overlaid on quadrant edges for insight callouts
- Numbered circles (01, 02, 03) for sequential callouts

#### Layout G: Table / Comparison
- Clean table with no outer border
- Header row: muted gray text, no background fill
- Data rows: separated by subtle horizontal lines (`#E5E5E5`)
- Cell text: 13-14pt
- Color-coded status indicators: green ✅, orange ⚠️ (triangle), red ❌
- Orange text (`#E67E22`) for row category labels in leftmost column

#### Layout H: Diagram / Flow (Simple)
- Light gray rectangles for containers (`#F0F0F0` / `#E8ECF0`)
- Directional arrows (simple, not ornate) — gray or blue-tinted
- Labels directly on shapes or adjacent
- Minimal decoration — no 3D effects, no gradients

#### Layout H2: Flowchart / Decision Tree
- **Starting node**: Rounded rectangle with light fill or colored border (e.g., `購買 ASUS / ROG 產品`)
- **Process steps**: Rounded rectangles with light gray fill (`#F0F0F0`) or thin border (`#CCCCCC`), centered text
- **Decision diamonds**: Rotated square (diamond shape) with centered question text (e.g., `累積達升等門檻？`), `yes` / `no` labels on exit paths
- **Arrows**: Thin gray lines (`#AAAAAA`), simple triangle arrowheads, strictly horizontal or vertical (no diagonal)
- **End annotations**: Bullet points (`•`) to the right of terminal nodes describing outcomes
- **Flow direction**: Generally left-to-right for main path, with vertical branches for yes/no decisions
- **Spacing**: ~40-60px between nodes, consistent alignment on invisible grid
- **Labels on arrows**: Small 12pt text (`yes`, `no`) placed adjacent to the arrow, not on it

#### Layout I: Persona Card (Two-Column)
- Dark navy background (`#2B3A4E`)
- Two equal columns (50/50)
- Each column: avatar illustration (circular), name + demographics, quote in「」marks
- Sections: 行為特徵, 怎麼看待科技, 對話風格
- All text is white on dark background
- Clean separation with vertical divider or spacing

#### Layout J: UX Issue / Heuristic Review
- Left side (~45%): Screenshot with red annotation box/rectangle overlay
- Right side (~55%): Structured issue report
  - `｜問題描述` with vertical bar
  - `｜使用者行為` with vertical bar
  - Blue/dark callout box with key insight (icon + bold text)
  - `｜修正建議` with vertical bar and bold recommendation
- Top: Task ID format: `Task A-2｜Page Name — Issue`
- Below task ID: `違反原則 [Principle Name]｜Level N` in colored text

#### Layout K: What's Next / Closing
- White background
- Title: "What's next" in 24-28pt bold, top-left
- 3-4 bullet points in the center area with `•` prefix
- Blue/teal colored text for each bullet
- Generous vertical spacing between bullets (~40-50px)
- Lower 30% empty

#### Layout L: Two-Column Comparison (Side-by-Side Systems)
- Two equal columns separated by a thin vertical divider line or arrow
- Each column has its own green vertical bar section header (e.g., `機制一：經驗值` vs `機制二：禮享回饋點數`)
- Outlined tag boxes (see Component 5.10) label sub-topics within each column
- Tables or structured lists within each column
- Optional bridging annotation between columns (e.g., a connecting note in a small text block)
- Bottom may have a muted annotation line (9-10pt, `#999999`)

#### Layout M: Comparison Table with Observation Panel
- Left side (~50%): Clean comparison table with labeled header "對比表"
  - Column headers for each system being compared
  - Rows with property names on the left
  - Color-coded values: green ✓ for positive, red ✗ for negative, orange for notable values
  - No outer border, subtle row separators
- Right side (~45%): "觀察" (observation) panel
  - 1-2 callout boxes with colored top accent bar (orange or teal)
  - Each box has a bold header and 2-3 bullet points of insight
  - Light background fill (`#FFF8F0` warm or `#F0F8FF` cool)
- Bottom: Muted footnote about next steps

#### Layout N: Multi-Lane Swimlane Flow ⭐ Very distinctive

**Structure**:
- Multiple horizontal swim lanes stacked vertically
- Each lane labeled on the left with a **color-coded role name**:
  - `User` → blue text (`#2980B9`)
  - `Agent` / `Agent (ChatGPT)` → red/coral text (`#C0392B`)
  - Backend (e.g., `Carrefour 後台`, `Paypal`) → green text (`#27AE60`)

**Nodes**:
- **User action nodes**: Rounded rect, light gray fill, gray border (`#CCCCCC`) — neutral action
- **Agent action nodes**: Rounded rect, light fill, **orange/coral dashed or solid border** (`#E67E22` or `#C0392B`) — AI-driven action
- **Backend nodes**: Rounded rect, light fill, **green border** (`#27AE60`) — system/platform action
- **Special annotation nodes** (e.g., "ACP 協議"): Different border color, sometimes with bullet content inside

**Connectors**:
- Horizontal solid arrows (→) within the same lane
- **Vertical dashed arrows** (↕) between lanes showing data flow / interaction
- Arrow color: gray `#AAAAAA`

**Layout on slide**:
- Left ~65%: The swimlane diagram(s) — may stack 2 diagrams vertically (e.g., Samsung flow + Sephora flow)
- Right ~30%: **"What's in AIA" gap analysis card** (see Component 5.14)
- Bottom: `→` summary insight line in body text

**Green-bar sub-headers** label each swimlane group (e.g., `｜Samsung Internet`, `｜Sephora Onsite AI Experience`)

#### Layout O: Insight Card + Wireframe Mockup ⭐ New

**Left panel (~40%)**:
- **Numbered insight card** with muted blue-gray background (`#8FA4B5` / `#7B95A8`)
- Numbered circle (e.g., "01", "02") in top-left of card — thin border, small
- Bold insight statement in white text (14-16pt)
- Supporting bullet points (`•`) in white text
- Same card style as quadrant matrix overlay insights

**Right panel (~55%)**:
- Green-bar sub-header: `｜可以怎麼參考`
- **Wireframe mockup(s)** showing a conceptual application:
  - Dark gray placeholder rectangles representing webpage/app UI
  - Light card overlays representing chatbot/AI assistant UI
  - Text annotations near elements showing proposed interaction
  - Dashed lines connecting data sources to UI elements
- Two mockups side-by-side: one for the webpage, one for the chatbot
- Labels above: e.g., `ROG Web page` | `AIA`

**Below the main content**: Dashed connector to data source label (e.g., "My ASUS Persona Data" with icon)

---

## 5. Components

### 5.1 Green Vertical Bar (Section Marker)
- Width: 3-4px
- Height: matches the text line height it accompanies
- Color: `#1B8A6B` / `#27AE60`
- Position: left edge of sub-section header, 8-10px gap to text
- Usage: marks every sub-section within a content slide

### 5.2 Tag / Badge (Filled)
- Shape: Rounded rectangle, border-radius 4-6px
- Padding: 6px horizontal, 3px vertical
- Background: solid color (green, orange, teal, blue depending on category)
- Text: 11-13pt, white, medium weight, center-aligned
- Usage: category labels, status indicators, inline classification

### 5.3 Callout Box (Red / Warning)
- Shape: Rectangle with slight rounded corners (6-8px)
- Background: `#E74C3C` (red) or `#D94F4F`
- Text: 13-14pt white, left-aligned
- Padding: 20-30px all sides
- Usage: limitations, critical issues, "還做不到" blocks
- May include a white border or none

### 5.4 Callout Box (Blue / Insight)
- Shape: Rounded rectangle (8px radius)
- Background: `#2B3A4E` (dark navy) or `#34495E`
- Text: 13-14pt white
- Often includes a small icon (chat bubble, arrow) on the left
- Padding: 16-24px
- Usage: user behavior insights, key takeaways

### 5.5 Case Study Card Frame
- White card with subtle shadow: `box-shadow: 0 2px 12px rgba(0,0,0,0.08)`
- Border-radius: 8-12px
- Contains: screenshot image (top/left) + descriptive text (below)
- **Background tint** matches case study accent color (see Section 2.3)

### 5.6 使用者價值 Box (Case Study Value)
- Rounded rect, 8px radius
- Background: **accent-tinted dark color** per case study (see Section 2.3)
- Icon: sparkle/star ✦ to the left of "使用者價值" header
- Header: 14pt bold white
- Body: 13pt white
- Left side: filled circle bullet (●) vertically centered outside the box
- Position: bottom-right of case study right panel

### 5.7 Timeline Dots (Case Study Right Panel)
- Small filled circles ●, ~8px diameter
- Color: `#AAAAAA` gray
- Vertically aligned, one per `/ section header`
- Implicitly connected by vertical spacing (no drawn line)
- Position: left edge of the right panel, sections flow downward

### 5.8 Numbered Circle
- Diameter: ~28-32px
- Border: 1.5px solid `#666666`
- Background: transparent (white)
- Number: 13pt, centered
- Usage: sequential insight callouts (e.g., "01", "02", "03") on matrix overlays and insight cards

### 5.9 Arrow / Connector
- **Solid arrow**: Simple straight or angled lines, `#AAAAAA` / `#999999`, small triangle arrowhead
- **Dashed arrow**: Used for cross-lane interaction in swimlanes
- **Direction**: Strictly horizontal or vertical — no curves, no diagonals

### 5.10 Tag / Badge (Outlined)
- Shape: Rounded rectangle, border-radius 4-6px
- Border: 1-1.5px solid `#AAAAAA` or `#CCCCCC`
- Background: transparent (white)
- Text: 12-13pt, `#333333`, medium weight, center-aligned
- Usage: sub-topic labels within content slides (e.g., "獲得方式", "使用方式", "升等門檻", "會員等級", "點數用途")
- Distinguishing: structural labels for information blocks, not status/category indicators

### 5.11 Flowchart Diamond (Decision Node)
- Shape: Rotated square (45°) forming a diamond
- Size: ~80-100px wide
- Border: 1.5px solid `#AAAAAA`
- Background: white or very light gray (`#FAFAFA`)
- Text: 12-13pt, centered, typically a yes/no question
- Exit labels: `yes` / `no` in 11pt muted text adjacent to outgoing arrows

### 5.12 Flowchart Process Node
- Shape: Rounded rectangle, border-radius 6-8px
- Border: 1-1.5px solid `#CCCCCC`
- Background: `#F5F5F5` or white
- Text: 12-13pt, centered
- Connected by thin gray arrows

### 5.13 Observation / Insight Side Panel
- Shape: Rounded rectangle card, border-radius 8px
- Top accent bar: 3-4px colored strip at top (orange `#E67E22` or teal `#008B8B`)
- Background: very light tint matching accent color (`#FFF8F0` or `#F0F8FF`)
- Header: 14-16pt bold, colored to match accent
- Body: 12-13pt bullets
- Usage: appears beside comparison tables to provide analytical commentary

### 5.14 "What's in AIA" Gap Analysis Card (Swimlane Companion)
- Positioned to the right of swimlane diagrams
- Green-bar header: `｜What's in AIA`
- Two-column mini table: `項目` | `AIA 應用差距`
- Red ✗ header accent
- Light gray background card, subtle border
- Bullet list of gaps per category
- Usage: always accompanies Layout N swimlanes

### 5.15 Status Indicator Icons
- ✅ / ✓ Green circle checkmark — "已做到"
- ⚠️ Orange/yellow triangle — "有限 / Idle/Hint"
- ❌ / ✗ Red X — "尚未做到"
- Used in tables, comparison matrices, and gap cards

### 5.16 Icon Style (in case study cards)
- Simple outline/line icons, not filled
- Blue or dark navy color
- Placed inside small circles or used inline with text headers
- Sources: simple icon set (Feather, Phosphor, or similar)

### 5.17 Swimlane Nodes (Color-Coded by Actor)
- **User nodes**: Gray border `#CCCCCC`, light fill — neutral
- **Agent nodes**: Orange/coral border `#E67E22` or `#C0392B`, light warm fill — AI-driven
- **Backend nodes**: Green border `#27AE60`, light fill — system/platform
- All: Rounded rect, 6-8px radius, 12-13pt centered text

---

## 6. Content Density & Information Architecture

### 6.1 Words Per Slide

| Slide Type | Chinese Characters | English Words | Max Fill |
|------------|-------------------|---------------|----------|
| Cover | 15-25 chars | 5-10 words | 30% |
| Section divider | 20-40 chars | 0-5 words | 25% |
| Context/overview | 100-200 chars | 10-30 words | 60% |
| Content detail | 80-180 chars | 10-20 words | 65% |
| Case study card | 200-350 chars | 30-60 words | 75% |
| Swimlane flow | 100-200 chars | 20-40 words | 75% |
| Matrix/quadrant | 80-150 chars | 20-40 words | 65% |
| UX issue slide | 150-300 chars | 10-30 words | 70% |
| Persona card | 200-350 chars | 5-15 words | 75% |
| Flowchart / decision tree | 80-150 chars | 10-30 words | 65% |
| Two-column comparison | 120-250 chars | 10-30 words | 70% |
| Comparison + observation | 150-300 chars | 15-40 words | 70% |
| Insight + wireframe | 100-200 chars | 10-20 words | 70% |
| Closing / next steps | 40-80 chars | 5-15 words | 35% |

### 6.2 Content Rules

- **Maximum 4-5 bullet points** per section on a single slide
- **Maximum 3 sub-sections** (with green bars) on one content slide
- **Case study cards** are the densest allowed — but still structured into clear panels
- **Never fill more than 75%** of the slide area — always leave breathing room
- **One key message per slide** — if the slide can't be summarized in one sentence, split it
- **Callout boxes** are limited to 1-2 per slide maximum
- **Screenshots**: maximum 2 per slide, with at least one being the primary focus

### 6.3 Bullet Style

| Context | Marker |
|---------|--------|
| Primary bullets (body text) | `- ` (hyphen + space) |
| Secondary bullets (nested/case studies) | `•` (bullet point) |
| Numbered items | Arabic numerals: `1`, `2`, `3` (not circled) or `一.`, `二.` for Chinese ordinals |

### 6.4 Breadcrumb / Navigation

- **Position**: Top-left, first line of every content slide
- **Format**: `Phase N｜章節中文名稱` (for 跨域agent) or `Section Title` reuse (for ROG)
- **Font**: 11-12pt, regular weight, muted gray (`#888888`)
- **Purpose**: Gives the audience a constant sense of location within the report structure
- **Right-side mini tag**: Sometimes a small category tag appears top-right (e.g., "User 觸發 × 自有平台") in `#AAAAAA` muted text

---

## 7. Slide Deck Structure

### 7.1 Standard Report Flow

```
1. Cover Slide (Layout A)
2. Context / Overview Slide (Layout C) — task definition + report roadmap
3. Section Divider (Layout B) — "Phase 1｜…"
4-N. Content Slides (Layout D/E/F/G/H/N/O) — the actual findings
    ├── Case study cards (E) with flow analysis (N) pairs
    ├── Matrix (F) as recurring anchor
    └── Insight + wireframe (O) for opportunities
N+1. Section Divider (Layout B) — "Phase 2｜…"
...repeat for each phase...
M. Summary / Insight Slide (Layout D with callouts or Layout M)
M+1. What's Next / Closing (Layout K)
```

### 7.2 Pacing Rules

- **Section dividers** appear before every major phase/chapter — they act as "breathing" slides
- **After every 3-5 dense slides**, insert a summary/synthesis slide or return to the matrix/framework to show progress
- **Case study sequences**: Matrix overview → Individual case study card → Matrix with annotations → Insight summary
- **The quadrant/matrix is reused** as a recurring anchor, with progressive highlighting to show which area is being discussed
- **Dense analytical slides (UX issues, heuristics)** are never placed back-to-back without a transition or summary

### 7.3 Case Study Presentation Pattern ⭐

The most distinctive sequence in Bonny's decks:

```
1. Quadrant matrix (F) — show which quadrant we're exploring
2. Case study card (E) — first case (e.g., Samsung)
3. Case study card (E) — second case (e.g., Sephora)
4. Return to matrix (F) — annotate with insight badges
5. Swimlane flow (N) — comparative flows + AIA gap card
6. Insight + wireframe (O) — "可以怎麼參考"
7. Return to matrix (F) — show accumulated annotations
```

### 7.4 Recurring Framework Pattern

Bonny frequently uses a **recurring 2×2 matrix** as a structural backbone:
- Introduce the matrix early (with all quadrants visible)
- In subsequent slides, highlight one quadrant at a time (others fade to muted gray)
- After covering each quadrant, show the full matrix with accumulated annotations/tags
- Orange ("資料授權深度") and teal ("協議開放程度") badges overlay the edges
- Numbered circles (01, 02, 03) appear at key insight moments
- This creates a strong narrative arc and sense of progress

---

## 8. Visual Style Principles

### 8.1 Core Aesthetic
- **Ultra-clean, editorial minimalism** — think "design research report" not "corporate pitch deck"
- **Content-first** — visuals serve the analysis, never decorative
- **Structured asymmetry** — layouts are not rigidly centered; they use left-heavy alignment with strategic right-column content
- **Color as information** — every color communicates meaning (status, category, severity, actor role)

### 8.2 Do's
- Use generous whitespace (30-50% of slide area should be empty)
- Use green vertical bars consistently for sub-sections
- Use the `Phase N｜name` breadcrumb on every content slide
- Keep screenshots in card frames with subtle shadows
- Use color-coded tags/badges for categorization
- Maintain consistent left-alignment throughout
- Use the recurring matrix pattern for multi-case analysis
- Apply 5% letter-spacing to all Chinese text
- Use case-specific accent colors for case study cards
- Use timeline dots on case study right panels

### 8.3 Don'ts
- Never use decorative backgrounds, textures, or patterns
- Never use gradients
- Never use centered body text (only titles may sometimes center, but usually don't)
- Never use underline accent lines beneath titles
- Never use more than 2 font sizes on a single slide (excluding breadcrumb/caption)
- Never use clip art, stock illustrations, or emoji
- Never use transition animations
- Never fill a slide to more than ~75% capacity
- Never use thick borders on tables — use subtle hairlines or none
- Never use 3D effects, reflections, or shadows heavier than `0 2px 12px rgba(0,0,0,0.08)`
- Never add page numbers (not present in any analyzed deck)

---

## 9. Special Patterns

### 9.1 Bilingual Content (CJK + Latin)
- Chinese is the primary language; English is used for:
  - Proper nouns (brand names, product names, technical terms)
  - Short labels within matrices or diagrams
  - Case study titles (often in English)
- When mixing: Chinese sentence flow with English terms inline, no special styling for the English portions
- Section headers sometimes use the pattern: `Chinese Title — English Subtitle`
- Phase labels use: `Phase N｜中文名稱`

### 9.2 Source Citation
- Position: Bottom-left of slide, OR bottom-right in a small boxed section
- Style: Full URL in 9pt muted gray, sometimes as clickable hyperlink in blue
- Format: bare URL (no "Source:" prefix), or with a small header "資料來源" above a list of URLs
- When multiple sources: stack vertically, one URL per line, right-aligned in a subtle bordered area

### 9.3 Slide Numbering
- Not visibly present in any analyzed deck — always omit page numbers

### 9.4 Dark-Background Slides
- Used sparingly (≈15-20% of slides in ROG deck)
- Background: `#2B3A4E` navy
- All text becomes white or light gray
- Screenshots appear with their natural backgrounds
- Used for: data-dense tables, persona cards, emphasis content, competitive analysis grids

### 9.5 Orange Text as Row Category Labels
- In comparison tables, category labels in the leftmost column may use orange (`#E67E22`) text instead of black
- This color-codes the category type (e.g., "購買", "內容參與", "日常登錄")
- The data in corresponding rows remains in standard `#333333`

### 9.6 Scope / Out-of-Scope Footer
- On context/overview slides, a muted footer line may clarify exclusions
- Format: Small text (10-11pt) in muted gray, e.g., "競品比較、設計評估、改善建議（後續階段再處理）"
- Position: Bottom-left, clearly subordinate to main content

### 9.7 Swimlane Node Color Coding
- User lane nodes: gray border → neutral user action
- Agent lane nodes: orange/coral border → AI-driven action
- Backend lane nodes: green border → system/platform action
- Cross-lane dashed arrows: data flow between actors

---

## 10. Implementation Notes for pptxgenjs

When generating slides programmatically:

```javascript
// Global defaults
const SLIDE_WIDTH = 13.33; // inches (1920px at 144dpi)
const SLIDE_HEIGHT = 7.5;  // inches (1080px at 144dpi)

// Margins
const MARGIN = { left: 0.7, top: 0.5, right: 0.5, bottom: 0.4 };

// Colors (no # prefix for pptxgenjs)
const COLOR = {
  text_primary: '333333',
  text_muted: '888888',
  text_caption: '999999',
  green_bar: '1B8A6B',
  red_callout: 'E74C3C',
  red_agent: 'C0392B',
  blue_callout: '2B3A4E',
  blue_user: '2980B9',
  orange_tag: 'E67E22',
  teal_tag: '008B8B',
  green_backend: '27AE60',
  navy_bg: '2B3A4E',
  light_gray_bg: 'F0F0F0',
  table_line: 'E5E5E5',
  white: 'FFFFFF',
};

// Case study accent colors
const CASE_ACCENT = {
  samsung:    { header: '2980B9', valueBox: '7B95A8', cardTint: 'F0F2F5' },
  sephora:    { header: '8B6848', valueBox: '8B7355', cardTint: 'F5EDE3' },
  carrefour:  { header: '8B6914', valueBox: '7B6B4A', cardTint: 'F2F0EC' },
  dia:        { header: 'C0392B', valueBox: 'A06060', cardTint: 'FDF0EC' },
  paypal:     { header: 'B8860B', valueBox: '5F8A8B', cardTint: 'F0F0F0' },
};

// Font settings
const FONT = {
  chinese: 'Microsoft JhengHei',  // or 'Noto Sans TC'
  english: 'Arial',
  fallback: 'sans-serif',
};

// Chinese text: set charSpacing to 5 (percent)
// English text: set charSpacing to 0
```

---

*Last updated: 2026-04-20*
