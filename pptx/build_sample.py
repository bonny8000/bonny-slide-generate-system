"""build_sample.py — generate real sample decks from the shared tokens.
Run:  python build_sample.py
Outputs sample-light.pptx and sample-dark.pptx next to this file.
Proves the token bridge: same content, mode = one argument.
"""
from slidegen import Deck, CJK, LAT

def build(mode, tone=None, out="out.pptx"):
    d = Deck(mode=mode, tone=tone)
    t = d.t
    # 1 · title
    d.title(
        "User Research · Interview",
        [("獨居住戶對「", t["ink"], CJK), ("陌生訪客接觸", t["accent"], CJK),
         ("」的焦慮，與對自動化驗證的明確期待", t["ink"], CJK)],
        sub="Findings from 3 in-depth interviews with solo dwellers.",
    )
    # 2 · ranked bars
    d.hbars("獨居者最擔心的安全情境是什麼？", [
        ("陌生訪客接觸", 59.8, True),
        ("包裹堆積、暴露行蹤", 30.8, False),
        ("夜間返家被尾隨", 17.3, False),
        ("鄰里出現陌生人", 14.0, False),
    ])
    # 3 · features (one headline row)
    d.features(
        "產品特色 · MVP",
        [("為獨居住戶而生的", t["ink"], CJK)],
        "將「等待」轉為「主動」，覆蓋從通知到收件的完整安全流程。",
        [("到達通知", "Notification", "配送員抵達即時推播。", False),
         ("安心對講", "Smart Intercom", "QR／編號驗證，一鍵 OK／拒絕。", True),
         ("無人收件保管", "Pickup Locker", "不在時自動保管，回家解鎖取件。", False)],
    )
    return d.save(out)

if __name__ == "__main__":
    import pathlib
    here = pathlib.Path(__file__).parent
    print(build("light", out=str(here/"sample-light.pptx")))
    print(build("dark",  out=str(here/"sample-dark.pptx")))
