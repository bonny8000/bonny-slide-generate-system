// InsightPanel — synthesized finding. Prefers dark mode; use light variant on a light slide.
function InsightPanel({ label, statement, note, implication, light = false }) {
  return (
    <div className={`insight-panel ${light ? "light" : ""}`}>
      {label && <span className="insight-label latin">{label}</span>}
      <p className="insight-statement cjk">{statement}</p>
      {note && <p className="insight-note cjk">{note}</p>}
      {implication && <p className="insight-implication cjk">{implication}</p>}
    </div>
  );
}

// KeyBand / NextStepBand — one-sentence takeaway pinned near the bottom of a slide.
function KeyBand({ children }) {
  return <div className="key-band cjk">{children}</div>;
}
function NextStepBand({ children, green = false }) {
  return <div className={`next-step-band ${green ? "green" : ""} cjk`}>{children}</div>;
}

Object.assign(window, { InsightPanel, KeyBand, NextStepBand });
