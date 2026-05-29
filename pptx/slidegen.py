"""slidegen.py — build real .pptx slides from the shared design tokens.

Geometry maps the 1920x1080 px canvas onto a 13.333" x 7.5" slide:
    144 px per inch  →  Inches(px/144)
Type maps the px scale to points at pt = px/2 (h1 50px -> 25pt, body 17px -> 8.5pt).

Covered templates (core set; mirrors the HTML components):
    title        · centred eyebrow + headline (+ optional accent run)
    hbars        · card with a Q line + horizontal ranked bars (one active)
    features     · stacked feature rows, one 'headline' row filled accent

One mode per deck — pass mode='light' or 'dark' to Deck(). Never mix.
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
import tokens as TK

CJK = "Noto Sans TC"
LAT = "Arial"
def IN(px): return Inches(px/144)
def PT(px): return Pt(px/2)
def C(hexs): return RGBColor.from_string(hexs)

def no_shadow(shape):
    """Override inherited theme shadow with an empty effect list (LibreOffice-safe)."""
    sp = shape._element
    spPr = sp.spPr
    for el in spPr.findall(qn('a:effectLst')):
        spPr.remove(el)
    spPr.append(spPr.makeelement(qn('a:effectLst'), {}))
    # drop the theme style block (its effectRef is what LibreOffice renders as a shadow)
    style = sp.find(qn('p:style'))
    if style is not None:
        sp.remove(style)

PADX, PADY = 96, 80  # px, matches --pad-x/--pad-y

class Deck:
    def __init__(self, mode="light", tone=None):
        self.mode = mode
        self.t = TK.apply_tone(TK.tokens(mode), tone)
        self.prs = Presentation()
        self.prs.slide_width  = IN(1920)
        self.prs.slide_height = IN(1080)

    def _blank(self):
        s = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        # full-bleed canvas
        bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, IN(1920), IN(1080))
        bg.fill.solid(); bg.fill.fore_color.rgb = C(self.t["canvas"])
        bg.line.fill.background()
        bg.shadow.inherit = False; no_shadow(bg)
        return s

    def _text(self, s, x, y, w, h, runs, size, bold=True, color=None,
              align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, lh=1.5):
        tb = s.shapes.add_textbox(IN(x), IN(y), IN(w), IN(h)); tf = tb.text_frame
        tf.word_wrap = True; tf.vertical_anchor = anchor
        p = tf.paragraphs[0]; p.alignment = align
        try: p.line_spacing = lh
        except Exception: pass
        if isinstance(runs, str): runs = [(runs, color or self.t["ink"], CJK)]
        for txt, col, font in runs:
            r = p.add_run(); r.text = txt
            r.font.size = PT(size); r.font.bold = bold
            r.font.name = font; r.font.color.rgb = C(col)
            # set east-asian font too
            rPr = r._r.get_or_add_rPr(); ea = rPr.makeelement(qn('a:ea'), {'typeface': CJK}); rPr.append(ea)
        return tb

    def _round(self, s, x, y, w, h, fill, radius=0.12, line=None):
        sp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, IN(x), IN(y), IN(w), IN(h))
        sp.fill.solid(); sp.fill.fore_color.rgb = C(fill)
        if line: sp.line.color.rgb = C(line); sp.line.width = Pt(1)
        else: sp.line.fill.background()
        sp.shadow.inherit = False; no_shadow(sp)
        try: sp.adjustments[0] = radius
        except Exception: pass
        return sp

    # ---------- templates ----------
    def title(self, eyebrow, head_runs, sub=None):
        s = self._blank()
        self._text(s, PADX, 360, 1920-2*PADX, 60, [(eyebrow, self.t["muted"], LAT)],
                   22, bold=True, align=PP_ALIGN.CENTER)
        self._text(s, PADX, 430, 1920-2*PADX, 220, head_runs, 50, bold=True,
                   align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP)
        if sub:
            self._text(s, PADX, 660, 1920-2*PADX, 80, [(sub, self.t["muted"], LAT)],
                       17, bold=False, align=PP_ALIGN.CENTER)
        return s

    def hbars(self, q, bars):  # bars=[(label,pct,active),...]
        s = self._blank()
        n = len(bars)
        inner = 64                       # card inner padding
        header_h = 72                    # space for the Q line
        pitch = 116                      # row pitch (opens up label↔bar gap)
        bar_h = 36
        cw = 1920 - 2*PADX
        cx = PADX
        ch = inner*2 + header_h + n*pitch
        cy = (1080 - ch)/2               # vertical centre (landscape + vertical balance)
        self._round(s, cx, cy, cw, ch, self.t["surface"], radius=0.05)
        self._text(s, cx+inner, cy+inner-6, cw-2*inner, 50,
                   [("Q. ", self.t["accent"], LAT), (q, self.t["ink"], CJK)], 20, bold=True)
        bx = cx+inner
        pct_col = 220
        bw = cw - 2*inner - pct_col
        by = cy + inner + header_h
        for i,(lab,pct,active) in enumerate(bars):
            yy = by + i*pitch
            self._text(s, bx, yy, bw, 36, [(lab, self.t["ink"], CJK)], 16, bold=False)
            self._round(s, bx, yy+50, max(bw*pct/100.0, bar_h), bar_h,
                        self.t["accent"] if active else self.t["muted_soft"], radius=0.5)
            # big, heavy percentage, vertically centred on the bar
            self._text(s, bx+bw+24, yy+40, pct_col-24, bar_h+24,
                       [(f"{pct}%", self.t["accent"] if active else self.t["muted"], LAT)],
                       30, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        return s

    def features(self, intro_pill, head_runs, lead, rows):  # rows=[(zh,en,desc,headline)]
        s = self._blank()
        # left intro column, vertically centred around the slide middle
        ly = 330
        self._round(s, PADX, ly, 230, 56, self.t["accent"], radius=0.5)
        self._text(s, PADX, ly+12, 230, 40, [(intro_pill, self.t["on_accent"], CJK)], 18,
                   bold=True, align=PP_ALIGN.CENTER)
        self._text(s, PADX, ly+90, 620, 180, head_runs, 50, bold=True)
        self._text(s, PADX, ly+270, 600, 120, [(lead, self.t["muted"], CJK)], 17, bold=False)
        # right rows
        rx, rw = 900, 1920-PADX-900
        rh, gap = 150, 24
        ry = (1080-(len(rows)*rh+(len(rows)-1)*gap))/2
        for i,(zh,en,desc,headline) in enumerate(rows):
            yy = ry + i*(rh+gap)
            fill = self.t["accent"] if headline else self.t["surface"]
            self._round(s, rx, yy, rw, rh, fill, radius=0.12,
                        line=None if headline else self.t["muted_soft"])
            tcol = self.t["on_accent"] if headline else self.t["ink"]
            dcol = "FFFFFF" if headline else self.t["muted"]
            self._text(s, rx+36, yy+30, rw-160, 40,
                       [(zh+" · ", tcol, CJK), (en, tcol, LAT)], 22, bold=True)
            self._text(s, rx+36, yy+78, rw-160, 60, [(desc, dcol, CJK)], 15, bold=False)
        return s

    def save(self, path):
        self.prs.save(path); return path
