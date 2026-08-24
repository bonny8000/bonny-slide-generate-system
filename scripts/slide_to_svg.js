/* Serialise a rendered slide into an SVG figure for the README.
 *
 * A README figure that is hand-drawn is a claim about the system; one serialised from the real
 * render is evidence from it. This walks the laid-out DOM and emits every painted box and text
 * run at the position the browser actually gave it, so the figure cannot drift from the slide.
 *
 * Usage — open the built slide, then in the browser console:
 *     copy(slideToSvg())                       // clipboard
 *     slideToSvg(document.querySelector('.slide'))
 * Save the result under assets/readme/ and reference it with a RELATIVE path in README.md.
 * Do not pin it to a raw.githubusercontent URL with a commit SHA: the image then freezes at that
 * commit and later regenerations of the figure never appear.
 *
 * Vector, not a screenshot: it stays crisp at any width, diffs as text, and weighs a few KB.
 * It covers what these slides are made of — filled/stroked boxes, border radii, text runs and
 * painted ::before/::after. It is not a general HTML renderer: gradients, shadows, transforms,
 * clipping and images are not carried over.
 */
function slideToSvg(slide = document.querySelector(".slide")) {
  const S = slide.getBoundingClientRect();
  const R = (n) => Math.round(n * 10) / 10;
  const esc = (t) => t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const vis = (c) => c && c !== "rgba(0, 0, 0, 0)" && c !== "transparent";
  const FONT =
    "ui-sans-serif,-apple-system,Segoe UI,Roboto,Helvetica Neue,Arial,PingFang TC,Noto Sans TC,sans-serif";
  const out = [];

  const box = (r, g) => {
    const x = R(r.left - S.left), y = R(r.top - S.top), w = R(r.width), h = R(r.height);
    if (w < 0.5 || h < 0.5) return;
    const rx = R(Math.min(parseFloat(g.borderTopLeftRadius) || 0, w / 2, h / 2));
    const op = +g.opacity < 1 ? ` opacity="${g.opacity}"` : "";
    if (vis(g.backgroundColor))
      out.push(`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${g.backgroundColor}"${op}/>`);
    const bw = parseFloat(g.borderTopWidth) || 0;
    if (bw > 0 && vis(g.borderTopColor) && g.borderTopStyle !== "none")
      out.push(
        `<rect x="${R(x + bw / 2)}" y="${R(y + bw / 2)}" width="${R(w - bw)}" height="${R(h - bw)}" rx="${rx}" fill="none" stroke="${g.borderTopColor}" stroke-width="${bw}"/>`,
      );
  };

  for (const el of [slide, ...slide.querySelectorAll("*")]) {
    const g = getComputedStyle(el);
    if (g.display === "none" || g.visibility === "hidden" || +g.opacity === 0) continue;
    const r = el.getBoundingClientRect();
    box(r, g);
    // Painted pseudo-elements carry real furniture here — a toggle knob, a sheet's grab handle.
    for (const pe of ["::before", "::after"]) {
      const pg = getComputedStyle(el, pe);
      if (!pg || pg.content === "none" || !vis(pg.backgroundColor)) continue;
      const pw = parseFloat(pg.width) || 0, ph = parseFloat(pg.height) || 0;
      if (!pw || !ph) continue;
      const abs = pg.position === "absolute";
      const left = parseFloat(pg.left), top = parseFloat(pg.top);
      box({
        left: r.left + (abs && !isNaN(left) ? left : 0),
        top: r.top + (abs && !isNaN(top) ? top : 0),
        width: pw, height: ph,
      }, pg);
    }
  }

  // Text node by text node, positioned from its own Range — an element's rect would lose every
  // run that sits beside a child element, which is most of the bilingual copy.
  const walker = document.createTreeWalker(slide, NodeFilter.SHOW_TEXT);
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    const t = n.nodeValue.replace(/\s+/g, " ").trim();
    if (!t) continue;
    const range = document.createRange();
    range.selectNodeContents(n);
    const r = range.getBoundingClientRect();
    if (r.width < 0.5 || r.height < 0.5) continue;
    const g = getComputedStyle(n.parentElement);
    const fs = parseFloat(g.fontSize);
    out.push(
      `<text x="${R(r.left - S.left)}" y="${R(r.bottom - S.top - (r.height - fs * 0.78) / 2)}" font-family="${FONT}" font-size="${R(fs)}" font-weight="${g.fontWeight}" fill="${g.color}" xml:space="preserve">${esc(t)}</text>`,
    );
  }

  const bg = getComputedStyle(slide).backgroundColor;
  return (
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${R(S.width)} ${R(S.height)}" width="${R(S.width)}" height="${R(S.height)}" role="img" aria-label="Rendered slide">` +
    `<rect width="${R(S.width)}" height="${R(S.height)}" fill="${vis(bg) ? bg : "#FBFBFE"}"/>\n` +
    out.join("\n") + "\n</svg>"
  );
}
