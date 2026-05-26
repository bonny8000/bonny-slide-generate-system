// QuoteCard — interview / VOC / usability quote with highlighted repeated phrase.
// Pass `quote` as JSX so callers can drop a <span className="highlight"> around the repeated term.
function QuoteCard({ quote, participant, context }) {
  return (
    <div className="quote-card">
      <p className="quote-text cjk">{quote}</p>
      <div className="participant">
        <span className="participant-dot"></span>
        <span className="latin">{participant}</span>
      </div>
      {context && <p className="quote-context latin">{context}</p>}
    </div>
  );
}
QuoteCard.Hero = function Hero({ quote, participant, context }) {
  return (
    <div className="quote-card hero">
      <p className="quote-text cjk">{quote}</p>
      <div className="participant"><span className="participant-dot"></span><span className="latin">{participant}</span></div>
      {context && <p className="quote-context latin">{context}</p>}
    </div>
  );
};

// PainCard — friction with cause. Pink/red accent reserved for actual pain.
function PainCard({ label, title, quote, root, severity }) {
  return (
    <article className="pain-card">
      <span className="pain-label latin">{label}</span>
      <h3 className="pain-title cjk">{title}</h3>
      {quote && <p className="pain-quote cjk">{quote}</p>}
      {root && <p className="pain-root cjk">{root}</p>}
      {severity && <span className="severity">{severity}</span>}
    </article>
  );
}

Object.assign(window, { QuoteCard, PainCard });
