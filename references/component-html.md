# Component HTML Reference

Use this file when composing any HTML slide. Copy the snippet, fill in real content, and do not invent new class names. All classes are defined in `assets/bonny-slide-v2-tokens.css`.

**Rule: never write inline `style=""` for colors, font sizes, or spacing. Use token classes only.**

The outer shell for every slide is always:

```html
<!doctype html>
<html lang="zh-TW">
<head>
  <meta charset="utf-8" />
  <title>Slide Title</title>
  <link rel="stylesheet" href="../assets/bonny-slide-v2-tokens.css" />
</head>
<body>
  <main class="slide" data-mode="light">   <!-- or data-mode="dark" -->
    <section class="frame">
      <!-- title block goes here -->
      <!-- content goes here -->
    </section>
    <!-- footer-bar goes here if needed -->
  </main>
</body>
</html>
```

---

## 1. Title Block

Use on every slide except a pure full-bleed visual cover.

### Standard editorial left (default)

```html
<p class="eyebrow latin">RESEARCH EVIDENCE</p>
<h1 class="headline cjk">
  用戶在發現後無法將意圖轉化為<span class="accent-blue">行動</span>
</h1>
<p class="subtitle latin">In-depth interview · N=12 · 2024 Q3</p>
```

### Centered (section divider or insight)

```html
<div class="center stack" style="gap:20px; padding-block-start: 180px;">
  <p class="eyebrow latin">INSIGHT 03</p>
  <h1 class="headline cjk" style="text-align:center; max-inline-size:1100px;">
    使用者<span class="accent-green">並非不願意</span>，而是沒有足夠的信心
  </h1>
</div>
```

### Split title (title left + status/metric right)

```html
<div class="split-title">
  <div>
    <p class="eyebrow latin">RESULT</p>
    <h1 class="headline cjk">任務完成率顯著提升</h1>
    <p class="subtitle latin">Usability test · Round 2 · N=8</p>
  </div>
  <div class="metric-card" style="min-inline-size:260px;">
    <span class="metric-value accent-green num">+34%</span>
    <span class="metric-label cjk">任務完成率</span>
    <span class="metric-baseline latin">vs. Round 1 baseline</span>
  </div>
</div>
```

**Eyebrow accent by mode:**
- Light mode → `.eyebrow` defaults to blue.
- Dark mode → `.eyebrow` defaults to green (handled by CSS automatically).

---

## 2. Evidence Card (3-column default)

Use for desk research, survey findings, or market background.

```html
<p class="eyebrow latin">DESK RESEARCH</p>
<h1 class="headline cjk">外部數據驗證了<span class="accent-blue">核心問題假設</span></h1>
<p class="subtitle latin">3 independent sources · 2023–2024</p>

<div class="content grid grid-3">
  <article class="card card-pad">
    <p class="pill latin">01</p>
    <h2 class="card-title cjk">找到關鍵數據點</h2>
    <p class="card-body cjk">一句話說明這項數據對用戶的意義，不超過兩行。</p>
    <p class="source latin">Source: Report Name, 2024</p>
  </article>

  <article class="card card-pad">
    <p class="pill latin">02</p>
    <h2 class="card-title cjk">第二個發現</h2>
    <p class="card-body cjk">保持卡片高度對齊。每張卡只放一個論點。</p>
    <p class="source latin">Source: Report Name, 2024</p>
  </article>

  <article class="card card-pad card-accent card-accent-blue">
    <p class="pill latin">KEY</p>
    <h2 class="card-title cjk">最關鍵的發現（視覺加強）</h2>
    <p class="card-body cjk">用 card-accent-blue 讓關鍵卡片稍微突出，其他卡片維持原樣。</p>
    <p class="source latin">Source: Report Name, 2024</p>
  </article>
</div>
```

**Metric evidence variant** — replace the card body with a large number:

```html
<article class="metric-card">
  <span class="metric-value accent-blue num">68%</span>
  <span class="metric-label cjk">的用戶在第一步就放棄</span>
  <span class="metric-baseline latin">Source: Funnel analytics, Q3 2024 · N=4,200</span>
</article>
```

---

## 3. Chart Card

Use when a number or trend relationship carries the main message.

```html
<p class="eyebrow latin">SURVEY RESULT</p>
<h1 class="headline cjk">超過半數用戶對<span class="accent-blue">推薦流程感到困惑</span></h1>
<p class="subtitle latin">Online survey · N=320 · 5-point scale</p>

<div class="content grid grid-2">
  <!-- Chart card (left) -->
  <div class="card card-pad stack" style="gap:16px;">
    <h2 class="card-title cjk">對推薦流程的理解程度</h2>
    <!-- Insert chart image or inline SVG here -->
    <img src="chart-placeholder.png" alt="Bar chart: comprehension ratings" style="width:100%; border-radius:12px;" />
    <p class="card-body cjk">
      <span class="accent-blue">52%</span> 表示「完全不理解」或「有點不理解」推薦的依據。
    </p>
    <p class="source latin">Q: 「您是否理解系統推薦課程的原因？」· 2024-09</p>
  </div>

  <!-- Interpretation card (right) -->
  <div class="stack" style="gap:20px;">
    <div class="metric-card">
      <span class="metric-value accent-blue num">52%</span>
      <span class="metric-label cjk">對推薦理由感到困惑</span>
      <span class="metric-baseline latin">N=320 respondents</span>
    </div>
    <div class="card card-pad card-accent card-accent-blue">
      <h3 class="card-title cjk">關鍵發現</h3>
      <p class="card-body cjk">困惑程度在新用戶（使用 ≤30 天）中更高，達 71%。</p>
    </div>
  </div>
</div>
```

**Rules:** always include an axis/baseline/source label. Never show a chart without `.source`.

---

## 4. Quote Card

Use for interview findings, user testing, or VOC evidence.

### Three-quote cluster (default)

```html
<p class="eyebrow latin">USER INTERVIEW</p>
<h1 class="headline cjk">用戶重複提到<span class="accent-blue">「不知道為什麼」</span>這個痛點</h1>
<p class="subtitle latin">In-depth interview · N=12 · Recurring theme</p>

<div class="content grid grid-3">
  <div class="quote-card">
    <p class="quote-text cjk">「<span class="highlight">不知道為什麼</span>系統推薦這個給我，我就不敢點。」</p>
    <div class="participant">
      <span class="participant-dot"></span>
      <span class="latin">P03 · F · 28 · 上班族</span>
    </div>
    <p class="quote-context latin">Task 2 — browse recommendations</p>
  </div>

  <div class="quote-card">
    <p class="quote-text cjk">「看到推薦清單我第一個反應就是：<span class="highlight">這是廣告嗎</span>？」</p>
    <div class="participant">
      <span class="participant-dot"></span>
      <span class="latin">P07 · M · 34 · 自由工作者</span>
    </div>
    <p class="quote-context latin">Task 2 — browse recommendations</p>
  </div>

  <div class="quote-card">
    <p class="quote-text cjk">「如果能告訴我為什麼推薦，我會更<span class="highlight">願意去嘗試</span>。」</p>
    <div class="participant">
      <span class="participant-dot"></span>
      <span class="latin">P11 · F · 41 · 中階主管</span>
    </div>
    <p class="quote-context latin">Post-task interview</p>
  </div>
</div>
```

### Hero single quote (dark slide)

Use `data-mode="dark"` on `.slide` for emotional insight moments.

```html
<!-- inside a dark slide -->
<div style="display:flex; align-items:center; block-size:100%;">
  <div class="quote-card hero" style="max-inline-size:1100px; margin-inline:auto;">
    <p class="quote-text cjk">
      「我以為這個功能是給<span class="highlight">別人</span>用的，不是給我這種人用的。」
    </p>
    <div class="participant">
      <span class="participant-dot"></span>
      <span class="latin">P09 · F · 52 · 退休教師 · 首次使用數位學習平台</span>
    </div>
    <p class="quote-context latin">Observation note — onboarding session</p>
  </div>
</div>
```

**Key rule:** highlight repeated phrases with `.highlight` — this shows pattern, not decoration.

---

## 5. Pain Point Card

Use when defining what blocks users. Always explain cause, not only symptom.

```html
<p class="eyebrow latin">PAIN POINT</p>
<h1 class="headline cjk">三個核心痛點阻礙了<span class="accent-pink">用戶的學習意願</span></h1>
<p class="subtitle latin">Synthesized from interview + usability test · N=12+8</p>

<div class="content grid grid-3">
  <div class="pain-card">
    <span class="pain-label">PAIN 01</span>
    <h3 class="pain-title cjk">找不到理由相信推薦</h3>
    <p class="pain-quote cjk">「不知道為什麼推薦這個，我就不敢點。」</p>
    <p class="pain-root cjk">根本原因：缺乏可見的推薦依據，用戶無法建立信任。</p>
    <span class="severity">高頻痛點 · 10/12 提及</span>
  </div>

  <div class="pain-card">
    <span class="pain-label">PAIN 02</span>
    <h3 class="pain-title cjk">進度感消失讓人焦慮</h3>
    <p class="pain-quote cjk">「我不知道我學到哪裡了，好像一直在原地。」</p>
    <p class="pain-root cjk">根本原因：進度指標只顯示完成率，沒有階段性里程碑。</p>
    <span class="severity">中頻痛點 · 7/12 提及</span>
  </div>

  <div class="pain-card">
    <span class="pain-label">PAIN 03</span>
    <h3 class="pain-title cjk">首次使用沒有引導</h3>
    <p class="pain-quote cjk">「一進來就看到這麼多東西，不知道要從哪裡開始。」</p>
    <p class="pain-root cjk">根本原因：Onboarding 直接進入全功能首頁，沒有任務導引。</p>
    <span class="severity">首次用戶集中 · 8/8</span>
  </div>
</div>
```

---

## 6. Insight Module

Use to synthesize evidence into a strategic finding. Almost always dark mode.

### Insight trio (3 columns)

```html
<!-- data-mode="dark" on .slide -->
<p class="eyebrow latin">KEY INSIGHTS</p>
<h1 class="headline cjk">研究揭示了<span class="accent-green">三個設計必須解決的核心張力</span></h1>

<div class="content grid grid-3">
  <div class="insight-panel">
    <p class="insight-label">INSIGHT 01</p>
    <h2 class="insight-statement cjk">信任感不是功能問題，<br>是<span class="highlight">透明度</span>問題</h2>
    <p class="insight-note cjk">用戶不拒絕推薦，但需要看到邏輯才願意採取行動。</p>
    <p class="insight-implication cjk">→ 顯示推薦依據，不是增加功能</p>
  </div>

  <div class="insight-panel">
    <p class="insight-label">INSIGHT 02</p>
    <h2 class="insight-statement cjk">進度感的缺失會讓<br><span class="highlight">動機提前消耗</span></h2>
    <p class="insight-note cjk">用戶在感覺「沒有進步」後，通常 3–5 天內就會停止登入。</p>
    <p class="insight-implication cjk">→ 設計里程碑，不只是百分比</p>
  </div>

  <div class="insight-panel">
    <p class="insight-label">INSIGHT 03</p>
    <h2 class="insight-statement cjk">新用戶需要的是<br><span class="highlight">任務感</span>，不是選項</h2>
    <p class="insight-note cjk">功能過多反而讓新用戶離開，導引式流程比開放式首頁更有效。</p>
    <p class="insight-implication cjk">→ Onboarding 給任務，不給選擇</p>
  </div>
</div>
```

### Single cinematic insight (dark slide, full emphasis)

```html
<!-- data-mode="dark" on .slide -->
<div style="display:flex; flex-direction:column; justify-content:center; block-size:100%; gap:32px;">
  <p class="eyebrow latin">CORE INSIGHT</p>
  <div class="insight-panel" style="max-inline-size:1200px;">
    <p class="insight-label">INSIGHT</p>
    <h2 class="insight-statement cjk" style="font-size:52px;">
      用戶不缺功能，缺的是<span class="highlight">「這個對我有用」</span>的感受
    </h2>
    <p class="insight-note cjk">所有測試中，功能探索行為與信任程度成正相關（r=0.78）。<br>當用戶感覺「系統懂我」，行動率提升 2.4 倍。</p>
    <p class="insight-implication cjk">→ 個人化的感受比個人化的演算法更重要</p>
  </div>
</div>
```

---

## 7. Problem-to-Opportunity Bridge

Use when the deck transitions from research to solution space.

```html
<p class="eyebrow latin">OPPORTUNITY</p>
<h1 class="headline cjk">每個痛點都指向一個<span class="accent-blue">可設計的機會</span></h1>

<div class="content grid grid-3">
  <!-- Column 1 -->
  <div class="stack" style="gap:16px;">
    <div class="pain-card">
      <span class="pain-label">PAIN</span>
      <h3 class="pain-title cjk">找不到相信推薦的理由</h3>
    </div>
    <div style="text-align:center; font-size:28px; color:var(--muted-light);">↓</div>
    <div class="card card-pad card-accent card-accent-blue">
      <p class="eyebrow latin" style="font-size:13px;">HMW</p>
      <h3 class="card-title cjk">如何讓推薦依據<br>在用戶行動前變得可見？</h3>
    </div>
  </div>

  <!-- Column 2 -->
  <div class="stack" style="gap:16px;">
    <div class="pain-card">
      <span class="pain-label">PAIN</span>
      <h3 class="pain-title cjk">進度感消失讓人焦慮</h3>
    </div>
    <div style="text-align:center; font-size:28px; color:var(--muted-light);">↓</div>
    <div class="card card-pad card-accent card-accent-blue">
      <p class="eyebrow latin" style="font-size:13px;">HMW</p>
      <h3 class="card-title cjk">如何讓用戶在每次登入時<br>都感覺到自己的成長？</h3>
    </div>
  </div>

  <!-- Column 3 -->
  <div class="stack" style="gap:16px;">
    <div class="pain-card">
      <span class="pain-label">PAIN</span>
      <h3 class="pain-title cjk">首次使用沒有引導</h3>
    </div>
    <div style="text-align:center; font-size:28px; color:var(--muted-light);">↓</div>
    <div class="card card-pad card-accent card-accent-blue">
      <p class="eyebrow latin" style="font-size:13px;">HMW</p>
      <h3 class="card-title cjk">如何在用戶完成第一個任務前<br>不讓他們感到迷失？</h3>
    </div>
  </div>
</div>
```

---

## 8. As-Is / To-Be Comparison

Use for process, service, UI, or value improvement.

```html
<p class="eyebrow latin">SOLUTION DIRECTION</p>
<h1 class="headline cjk">設計方向：從<span class="accent-gray">模糊選項</span>到<span class="accent-green">有依據的引導</span></h1>

<div class="content comparison-grid" style="gap:24px;">
  <!-- As-Is column -->
  <div class="state-col">
    <div class="state-header as-is">AS-IS · 現況</div>
    <div class="state-body">
      <div class="state-row">
        <span style="color:var(--gray); margin-top:2px;">✕</span>
        <span class="cjk">推薦清單無依據說明，用戶不知為何出現</span>
      </div>
      <div class="state-row">
        <span style="color:var(--gray); margin-top:2px;">✕</span>
        <span class="cjk">進度只顯示完成百分比，無里程碑</span>
      </div>
      <div class="state-row">
        <span style="color:var(--gray); margin-top:2px;">✕</span>
        <span class="cjk">首頁直接展示全部功能，新用戶無引導</span>
      </div>
    </div>
  </div>

  <!-- Arrow divider -->
  <div class="state-divider">→</div>

  <!-- To-Be column -->
  <div class="state-col">
    <div class="state-header to-be">TO-BE · 設計方向</div>
    <div class="state-body to-be">
      <div class="state-row">
        <span style="color:var(--green); margin-top:2px;">✓</span>
        <span class="cjk">每個推薦顯示 2–3 個依據標籤（興趣、目標、歷史）</span>
      </div>
      <div class="state-row">
        <span style="color:var(--green); margin-top:2px;">✓</span>
        <span class="cjk">進度拆分為階段里程碑，完成時有明確慶祝回饋</span>
      </div>
      <div class="state-row">
        <span style="color:var(--green); margin-top:2px;">✓</span>
        <span class="cjk">新用戶 Onboarding 流程：3 步任務 → 首頁解鎖</span>
      </div>
    </div>
  </div>
</div>
```

---

## 9. Workflow Timeline

Use for sequence, journey, project phase, or product flow. Max 5 stages on one slide.

```html
<p class="eyebrow latin">USER JOURNEY</p>
<h1 class="headline cjk">用戶從<span class="accent-blue">發現到完成課程</span>的關鍵流程</h1>
<p class="subtitle latin">Service blueprint · Primary path · Mobile</p>

<div class="content timeline">
  <div class="timeline-stage">
    <div class="stage-num latin">01</div>
    <div class="stage-card">
      <h3 class="stage-title cjk">發現</h3>
      <p class="stage-body cjk">透過首頁推薦或搜尋找到課程</p>
      <span class="stage-actor latin">Learner</span>
    </div>
  </div>

  <div class="timeline-stage">
    <div class="stage-num latin">02</div>
    <div class="stage-card">
      <h3 class="stage-title cjk">評估</h3>
      <p class="stage-body cjk">查看課程介紹、評分、推薦依據</p>
      <span class="stage-actor latin">Learner</span>
    </div>
  </div>

  <div class="timeline-stage">
    <!-- active / current stage: no class change needed, just style -->
    <div class="stage-num latin" style="background:var(--green); color:var(--bg-dark);">03</div>
    <div class="stage-card" style="border-color:var(--green); border-width:2px;">
      <h3 class="stage-title cjk">開始學習</h3>
      <p class="stage-body cjk">進入課程，完成第一個單元</p>
      <span class="stage-actor latin">Learner</span>
    </div>
  </div>

  <div class="timeline-stage inactive">
    <div class="stage-num latin">04</div>
    <div class="stage-card">
      <h3 class="stage-title cjk">持續回訪</h3>
      <p class="stage-body cjk">收到進度通知，繼續未完成課程</p>
      <span class="stage-actor latin">System + Learner</span>
    </div>
  </div>

  <div class="timeline-stage inactive">
    <div class="stage-num latin">05</div>
    <div class="stage-card">
      <h3 class="stage-title cjk">完成</h3>
      <p class="stage-body cjk">取得證書，觸發新推薦</p>
      <span class="stage-actor latin">Learner</span>
    </div>
  </div>
</div>
```

**Rule:** use `.inactive` on future stages. Highlight the current focus stage manually with green border and stage-num color.

---

## 10. Phone Mockup Walkthrough

Use for mobile product, app feature, or UI state explanation.

```html
<!-- data-mode="dark" on .slide for walkthrough slides -->
<p class="eyebrow latin">FEATURE WALKTHROUGH</p>
<h1 class="headline cjk">推薦卡片加入<span class="accent-green">依據標籤</span>後的互動流程</h1>

<div class="content row" style="align-items:flex-start; gap:80px; padding-block-start:16px;">
  <!-- Phone mockup area -->
  <div class="phone-stage" style="flex:0 0 auto;">
    <div class="phone">
      <!-- Replace with actual screenshot img -->
      <img src="screen-placeholder.png" alt="App screen: recommendation card with tags"
           style="width:100%; height:100%; object-fit:cover; border-radius:30px;" />
    </div>
  </div>

  <!-- Annotation list -->
  <div class="annotation-list" style="flex:1; padding-block-start:40px;">
    <div class="annotation-item">
      <div class="annotation-num latin">1</div>
      <p class="annotation-text cjk">推薦依據標籤顯示在課程卡片下方（興趣 / 目標 / 你的歷史）</p>
    </div>
    <div class="annotation-item">
      <div class="annotation-num latin">2</div>
      <p class="annotation-text cjk">點擊標籤可展開完整推薦說明，讓用戶建立信任感</p>
    </div>
    <div class="annotation-item">
      <div class="annotation-num latin">3</div>
      <p class="annotation-text cjk">「立即開始」按鈕在說明展開後，點擊率提升 +28%</p>
    </div>
    <p class="source latin" style="margin-block-start:24px;">A/B test · N=1,200 · 2024-11</p>
  </div>
</div>
```

---

## 11. Feature Stack

Use for MVP scope, service principles, or product pillars.

```html
<p class="eyebrow latin">MVP FEATURE SET</p>
<h1 class="headline cjk">三個核心功能解決<span class="accent-blue">信任與動機</span>問題</h1>
<p class="subtitle latin">Phase 1 scope · 8-week sprint</p>

<div class="content feature-stack">
  <div class="feature-row highlight">
    <div class="feature-icon">📌</div>
    <div class="feature-content">
      <h3 class="feature-title cjk">透明推薦依據</h3>
      <p class="feature-value cjk">在每個推薦課程旁顯示 2–3 個依據標籤，讓用戶理解「為什麼是這個」。</p>
    </div>
    <span class="phase-chip active latin" style="margin-inline-start:auto; align-self:center;">優先</span>
  </div>

  <div class="feature-row">
    <div class="feature-icon">🏁</div>
    <div class="feature-content">
      <h3 class="feature-title cjk">階段里程碑進度</h3>
      <p class="feature-value cjk">將進度條拆分為有名稱的學習階段，完成里程碑時提供明確回饋。</p>
    </div>
    <span class="phase-chip latin" style="margin-inline-start:auto; align-self:center;">P1</span>
  </div>

  <div class="feature-row">
    <div class="feature-icon">🧭</div>
    <div class="feature-content">
      <h3 class="feature-title cjk">新用戶 Onboarding 任務流</h3>
      <p class="feature-value cjk">首次進入時引導完成 3 步任務，完成後解鎖全功能首頁。</p>
    </div>
    <span class="phase-chip latin" style="margin-inline-start:auto; align-self:center;">P1</span>
  </div>
</div>
```

---

## 12. Result Dashboard

Use for outcomes, final impact, or test results. Usually dark mode.

```html
<!-- data-mode="dark" on .slide -->
<p class="eyebrow latin">RESULT</p>
<h1 class="headline cjk">可用性測試第二輪：<span class="accent-green">三項指標全面提升</span></h1>
<p class="subtitle latin">Usability test Round 2 · N=8 · vs. Round 1 baseline</p>

<div class="content grid grid-3">
  <div class="metric-card">
    <span class="metric-value accent-green num">+34%</span>
    <span class="metric-label cjk">任務完成率</span>
    <span class="metric-delta up latin">↑ 58% → 92%</span>
    <span class="metric-baseline latin">Task: find & start a recommended course</span>
  </div>

  <div class="metric-card">
    <span class="metric-value accent-green num">-41%</span>
    <span class="metric-label cjk">平均任務時間</span>
    <span class="metric-delta up latin">↓ 4m32s → 2m41s</span>
    <span class="metric-baseline latin">Same task · same protocol</span>
  </div>

  <div class="metric-card">
    <span class="metric-value accent-green num">4.3</span>
    <span class="metric-label cjk">信任感評分</span>
    <span class="metric-delta up latin">↑ 2.8 → 4.3 / 5</span>
    <span class="metric-baseline latin">Post-task survey · 5-point scale</span>
  </div>
</div>

<div class="next-step-band green" style="margin-block-start:32px;">
  → 下一步：將設計方案提交開發，安排 Sprint 1 kickoff
</div>
```

---

## 13. Positioning Map

Use for user segmentation, behavior grouping, or strategy focus.

```html
<p class="eyebrow latin">USER SEGMENTATION</p>
<h1 class="headline cjk">根據學習動機與數位熟悉度<span class="accent-blue">定位目標用戶群</span></h1>

<div class="content grid grid-2" style="gap:40px; align-items:start;">
  <!-- Map placeholder + description -->
  <div class="card card-pad">
    <!-- Insert 2x2 matrix image or SVG -->
    <img src="positioning-map.png" alt="2x2 matrix: motivation vs digital fluency"
         style="width:100%; border-radius:12px;" />
    <p class="source latin" style="margin-block-start:12px;">N=320 survey respondents clustered by k-means</p>
  </div>

  <!-- Segment cards -->
  <div class="stack" style="gap:20px;">
    <div class="card card-pad card-accent card-accent-blue">
      <p class="pill latin" style="background:var(--blue); margin-bottom:12px;">TARGET</p>
      <h3 class="card-title cjk">主動學習者</h3>
      <p class="card-body cjk">動機強、數位熟悉度高。會主動搜尋，但對「不透明推薦」最為敏感。</p>
      <p class="source latin">38% of sample · Most likely to churn if trust breaks</p>
    </div>
    <div class="card card-pad">
      <h3 class="card-title cjk">被動探索者</h3>
      <p class="card-body cjk">動機中等、對介面不熟悉。最需要引導式 Onboarding。</p>
      <p class="source latin">29% of sample</p>
    </div>
  </div>
</div>
```

---

## 14. Case Study Card

Use when introducing benchmarks, references, or competitive analysis.

```html
<p class="eyebrow latin">BENCHMARK</p>
<h1 class="headline cjk">三個參考案例的<span class="accent-blue">可遷移設計模式</span></h1>

<div class="content grid grid-3">
  <div class="card card-pad">
    <img src="case-duolingo.png" alt="Duolingo streak screenshot"
         style="width:100%; border-radius:12px; margin-bottom:16px;" />
    <p class="eyebrow latin" style="font-size:14px;">Duolingo</p>
    <h3 class="card-title cjk">Streak 里程碑機制</h3>
    <p class="card-body cjk">連續學習天數轉化為具體數字和慶祝回饋，強化每日回訪動機。</p>
    <p class="source latin">Transferable: milestone celebration pattern</p>
  </div>

  <div class="card card-pad card-accent card-accent-blue">
    <img src="case-netflix.png" alt="Netflix recommendation tag screenshot"
         style="width:100%; border-radius:12px; margin-bottom:16px;" />
    <p class="eyebrow latin" style="font-size:14px;">Netflix</p>
    <h3 class="card-title cjk">推薦依據標籤</h3>
    <p class="card-body cjk">「因為你看了 X」讓推薦立即有邏輯，大幅降低「這是廣告嗎」的疑慮。</p>
    <p class="source latin">Transferable: transparent recommendation rationale</p>
  </div>

  <div class="card card-pad">
    <img src="case-duolingo-onboarding.png" alt="Duolingo onboarding flow"
         style="width:100%; border-radius:12px; margin-bottom:16px;" />
    <p class="eyebrow latin" style="font-size:14px;">Duolingo Onboarding</p>
    <h3 class="card-title cjk">任務式引導流程</h3>
    <p class="card-body cjk">先完成一個小任務再進入全功能，建立早期成就感。</p>
    <p class="source latin">Transferable: task-first onboarding</p>
  </div>
</div>
```

---

## 15. Key Band

Use for final takeaway, HMW transition, or section bridge. One sentence only.

### Bottom band under evidence

```html
<div class="next-step-band" style="margin-block-start:32px;">
  核心機會：讓「為什麼推薦給我」在用戶點擊前就已經可見
</div>
```

### Standalone full-width center band (section divider)

```html
<div style="display:flex; align-items:center; justify-content:center; block-size:100%;">
  <div class="key-band" style="max-inline-size:1100px; font-size:32px; border-radius:28px; padding:40px 60px;">
    從「功能完整」走向「用戶感覺被理解」
  </div>
</div>
```

### Dark band on light slide

```html
<div class="insight-panel" style="padding:28px 40px;">
  <p class="insight-label">TAKEAWAY</p>
  <p class="insight-statement cjk" style="font-size:28px;">
    設計的目標不是讓用戶學更多，而是讓用戶<span class="highlight">敢開始</span>
  </p>
</div>
```

---

## Footer Bar (always include for evidence slides)

```html
<div class="footer-bar">
  <span class="footer-source latin">Source: In-depth interview N=12, Usability test N=8 · 2024 Q3–Q4</span>
  <span class="page-marker latin">04 / 18</span>
</div>
```

---

## Chip Row (method metadata under title block)

Add after the subtitle when showing research method context:

```html
<div class="row" style="gap:12px; margin-block-start:20px; flex-wrap:wrap;">
  <span class="method-chip latin">In-depth Interview</span>
  <span class="count-chip latin">N=12</span>
  <span class="method-chip latin">Usability Test</span>
  <span class="count-chip latin">N=8</span>
  <span class="method-chip latin">2024 Q3–Q4</span>
</div>
```
