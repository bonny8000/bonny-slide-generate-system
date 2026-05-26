// EvidenceCard — desk research / survey findings. 3-column default.
function EvidenceCard({ pill, title, body, source, accent }) {
  const accentClass = accent ? `card-accent card-accent-${accent}` : "";
  return (
    <article className={`card card-pad ${accentClass}`}>
      {pill && <p className="pill latin">{pill}</p>}
      <h2 className="card-title cjk">{title}</h2>
      <p className="card-body cjk">{body}</p>
      {source && <p className="source latin">{source}</p>}
    </article>
  );
}
EvidenceCard.Grid = function Grid({ children, cols = 3 }) {
  return <div className={`content grid grid-${cols}`}>{children}</div>;
};

// MetricCard — large metric + label + baseline. Use as result dashboard cards.
function MetricCard({ value, label, baseline, delta, accent = "blue" }) {
  return (
    <article className="metric-card">
      <span className={`metric-value accent-${accent} num`}>{value}</span>
      <span className="metric-label cjk">{label}</span>
      {delta && <span className={`metric-delta ${delta.direction === "down" ? "down" : "up"} latin`}>{delta.text}</span>}
      {baseline && <span className="metric-baseline latin">{baseline}</span>}
    </article>
  );
}

Object.assign(window, { EvidenceCard, MetricCard });
