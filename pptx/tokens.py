"""tokens.py — PPTX colour bridge.
Mirrors assets/tokens-light.css and assets/tokens-dark.css so HTML and PPTX
decks share one source of truth. Edit the CSS and these together.
"""
LIGHT = dict(
    canvas="FBFBFE", surface="F1F4F9", chip="FFFFFF",
    ink="2B3040", muted="7C7E92", muted_soft="DCE0EB",
    accent="7077FB", accent_soft="E7E8FC", on_accent="FFFFFF",
    band_fill="2B3040", band_tag="B7BCD0", donut_3="C2C6D4",
    pos="2FB67A", pos_soft="DCF3E8", neg="E5556E", neg_soft="FBE2E7",
    warn="E08A1E", warn_soft="FBEED7",
)
DARK = dict(
    canvas="1B1B20", surface="2C2C33", chip="34343C",
    ink="FFFFFF", muted="9A9CA8", muted_soft="454652",
    accent="4D77FF", accent_soft="2A3358", on_accent="FFFFFF",
    band_fill="23242C", band_tag="B7BCD0", donut_3="5E6070",
    pos="34D399", pos_soft="173A30", neg="F26D82", neg_soft="3A1F26",
    warn="F2B04E", warn_soft="3A2E18",
)

# tone modifier: swap the single accent per slide intent (mirrors .slide.tone-*)
def apply_tone(t, tone=None):
    t = dict(t)
    if tone == "pos":  t["accent"], t["accent_soft"] = t["pos"], t["pos_soft"]
    if tone == "neg":  t["accent"], t["accent_soft"] = t["neg"], t["neg_soft"]
    if tone == "warn": t["accent"], t["accent_soft"] = t["warn"], t["warn_soft"]
    return t

def tokens(mode):
    return dict(LIGHT) if mode == "light" else dict(DARK)
