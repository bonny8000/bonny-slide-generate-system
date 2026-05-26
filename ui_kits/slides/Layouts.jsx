// ComparisonGrid — As-Is / To-Be parallel comparison.
function ComparisonGrid({ asIs, toBe, asIsLabel = "AS-IS", toBeLabel = "TO-BE" }) {
  return (
    <div className="content comparison-grid">
      <div className="state-col">
        <div className="state-header as-is latin">{asIsLabel}</div>
        <div className="state-body">
          {asIs.map((row, i) => <div key={i} className="state-row">{row}</div>)}
        </div>
      </div>
      <div className="state-divider">→</div>
      <div className="state-col">
        <div className="state-header to-be latin">{toBeLabel}</div>
        <div className="state-body to-be">
          {toBe.map((row, i) => <div key={i} className="state-row">{row}</div>)}
        </div>
      </div>
    </div>
  );
}

// Timeline — workflow timeline with 3–5 stages.
function Timeline({ stages }) {
  return (
    <div className="content timeline">
      {stages.map((s, i) => (
        <div key={i} className={`timeline-stage ${s.inactive ? "inactive" : ""}`}>
          <div className="stage-num latin">{i + 1}</div>
          <div className="stage-card">
            <h3 className="stage-title cjk">{s.title}</h3>
            {s.body && <p className="stage-body cjk">{s.body}</p>}
            {s.actor && <span className="stage-actor latin">{s.actor}</span>}
          </div>
        </div>
      ))}
    </div>
  );
}

// FeatureStack — MVP / pillar feature rows.
function FeatureStack({ items }) {
  return (
    <div className="content feature-stack">
      {items.map((it, i) => (
        <div key={i} className={`feature-row ${it.highlight ? "highlight" : ""}`}>
          {it.icon && <div className="feature-icon">{it.icon}</div>}
          <div className="feature-content">
            <h3 className="feature-title cjk">{it.title}</h3>
            {it.value && <p className="feature-value cjk">{it.value}</p>}
          </div>
        </div>
      ))}
    </div>
  );
}

Object.assign(window, { ComparisonGrid, Timeline, FeatureStack });
