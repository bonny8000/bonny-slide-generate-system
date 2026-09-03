# Routing cases — what the router must resolve

Fixture for `scripts/validate_routing.py`. One row per realistic slide intention, phrased the way a
user actually asks, followed by the layout it must resolve to.

**Phrasing rule: never paraphrase the router's own `intent` line.** A case written by copying the
spec's wording tests nothing — it proves the string matches itself. Every case here is written as a
request first, then checked against which layout should win. If you add a case, write the request
before you look at the candidate layout.

Coverage is deliberately uneven toward 繁中, which is the system's primary output language, with
English cases mixed in because the system must serve both.

| request | expect |
| --- | --- |
| 我們想說明專案接下來三個階段的時程與各階段產出 | timeline |
| roadmap phases and what ships in each | timeline |
| 介紹三個主要使用者輪廓，還有他們各自遇到的困擾 | persona-cards |
| two personas and the pain points they run into | persona-cards |
| 呈現這次改版帶來的四個成效數字 | results-grid |
| four outcome metrics, each with a one-line reason | results-grid |
| 把目前遇到的問題跟我們的解法放在一起對照 | problem-solution |
| 痛點放左邊，解法放右邊 | problem-solution |
| 改版前後的畫面對照 | as-is-to-be |
| 用兩個軸線畫出競品分布跟我們想去的位置 | positioning-matrix |
| 先統一幾個名詞的定義，讓大家講的是同一件事 | terminology-cards |
| 說明產品主要服務哪幾種客群 | use-case-cards |
| 把使用者的原話跟對應的數據並排呈現 | qual-quant-split |
| 一個痛點，配上訪談引述跟數據佐證 | painpoint-evidence |
| 把幾組訪談結果收斂成一個共同的洞察 | interview-affinity |
| 問卷結果整理，每一題一列 | survey-stack |
| 從背景數據一路推導到重新定義的問題 | research-flow |
| 說明這個服務從頭到尾怎麼運作 | service-flow |
| 把六個功能用卡片平均排開 | feature-grid |
| 示範這幾個功能畫面怎麼化解使用者的不安 | feature-showcase |
| 產品首頁式的介紹，這是什麼、能做什麼 | product-hero |
| landing-page style introduction to the product | product-hero |
| 三個我們的價值主張，每個都要有具體佐證 | value-points |
| 三個核心理念，等重呈現 | keyword-cards |
| 一個核心概念放中間，周圍是它的幾個面向 | hero-radial |
| 幾個概念串成一個連續的整體 | linked-circles |
| 三個依序的重點，每點配一張圖表 | numbered-rows |
| 一個設計想法，搭配支持它的證據 | idea-evidence |
| 用一個提問開場，再用並列的證據回答它 | centered-question-evidence |
| 用比較有人味的方式說明這場工作坊怎麼進行 | editorial-explainer-stage |
| 一次結帳從按下去到出帳，中間服務之間互相呼叫了什麼、順序是什麼 | event-sequence |
| walk through the calls between the app, the bridge and the ad server in the order they fire | event-sequence |
| 這個崩潰是哪幾個元件在什麼順序下互相影響造成的 | event-sequence |
| 這個功能由哪些元件組成，哪一個是跑在 webview 裡面的 | system-anatomy |
| show what the ad stack is built from and which piece is hosted inside the native app | system-anatomy |
| 說明這個當機是怎麼從監控被發現、QA 重現、最後開發找到原因的 | role-thread |
| retell the incident showing what each team saw before we landed on the cause | role-thread |
