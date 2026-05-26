// PhoneWalkthrough — phone mockup + annotation list. Pass `screen` as JSX to render
// the product UI inside the phone shell. The .phone class draws the bezel + radius.
function PhoneWalkthrough({ screen, annotations }) {
  return (
    <div className="content row" style={{ gap: 80, alignItems: "flex-start", paddingBlockStart: 24 }}>
      <div className="phone-stage" style={{ flexShrink: 0 }}>
        <div className="phone">{screen}</div>
      </div>
      <div className="stack" style={{ gap: 32, paddingBlockStart: 60 }}>
        <div className="annotation-list">
          {annotations.map((a, i) => (
            <div key={i} className="annotation-item">
              <div className="annotation-num">{i + 1}</div>
              <div className="annotation-text cjk">
                {a.text}
                {a.support && <><br /><span className="quote-context latin">{a.support}</span></>}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// Chips — method / count / phase / severity.
function MethodChip({ children }) { return <span className="method-chip">{children}</span>; }
function CountChip({ children }) { return <span className="count-chip">{children}</span>; }
function PhaseChip({ children, active }) { return <span className={`phase-chip ${active ? "active" : ""}`}>{children}</span>; }

Object.assign(window, { PhoneWalkthrough, MethodChip, CountChip, PhaseChip });
