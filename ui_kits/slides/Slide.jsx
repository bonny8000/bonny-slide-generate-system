// Slide.jsx — the shell. Wraps the .slide + .frame structure and handles data-mode.
function Slide({ mode = "light", children }) {
  return (
    <main className="slide" data-mode={mode} data-screen-label={`Slide · ${mode}`}>
      <section className="frame">{children}</section>
    </main>
  );
}

// TitleBlock — eyebrow + headline + subtitle. Headline accepts JSX so the caller can
// drop a <span className="accent-blue"> in to highlight a single phrase.
function TitleBlock({ eyebrow, headline, subtitle, variant = "left" }) {
  if (variant === "center") {
    return (
      <div className="center stack" style={{ gap: 20, paddingBlockStart: 180 }}>
        {eyebrow && <p className="eyebrow latin">{eyebrow}</p>}
        <h1 className="headline cjk" style={{ textAlign: "center", maxInlineSize: 1100 }}>{headline}</h1>
        {subtitle && <p className="subtitle latin">{subtitle}</p>}
      </div>
    );
  }
  return (
    <>
      {eyebrow && <p className="eyebrow latin">{eyebrow}</p>}
      <h1 className="headline cjk">{headline}</h1>
      {subtitle && <p className="subtitle latin">{subtitle}</p>}
    </>
  );
}

// Footer — source + page marker, pinned to the slide bottom by .footer-bar.
function Footer({ source, page }) {
  return (
    <div className="footer-bar">
      <span className="footer-source latin">{source}</span>
      <span className="page-marker latin">{page}</span>
    </div>
  );
}

Object.assign(window, { Slide, TitleBlock, Footer });
