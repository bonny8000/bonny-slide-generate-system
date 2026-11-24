#!/usr/bin/env python3
"""Read the words on built slides and point at wording worth a second look.

A companion to the rules in ``specs/writing/``. It finds things a stylesheet check cannot: a short
headline that pauses on a comma, half-width punctuation inside Chinese text, a mainland term, a
stock phrase that says nothing, a title that ends in a full stop.

**This advises, it does not gate.** Every pattern here has legitimate uses — 「透過視訊參加」 is
ordinary Chinese, 「用戶」 is the usual word in telecom and banking — and the script cannot see the
source a slide was written from, so it cannot check the things that matter most (numbers, conditions,
certainty). Those stay with the meaning check in ``foundations/plain-language.md``. Exit status is
always 0; read the output as a list of questions and overrule it when the slide's intent calls for it.

Usage:
    python scripts/check_copy.py slides/
    python scripts/check_copy.py examples/deck-demo/01-cover.html --quiet
"""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

CJK = r"一-鿿"
SKIP_TAGS = {"style", "script", "svg", "code", "pre", "template"}
HEADLINE_TAGS = {"h1", "h2"}
HEADLINE_CLASSES = {"title", "statement", "takeaway", "headline"}
VOID_TAGS = {"br", "img", "hr", "input", "meta", "link", "source", "wbr", "col"}

HALF_WIDTH = re.compile(rf"[{CJK}][,;:?!](?=[{CJK}\s]|$)")
ASCII_ELLIPSIS = re.compile(rf"[{CJK}]\.\.\.")
HEADLINE_COMMA = re.compile(r"[，,]")
FINAL_STOP = re.compile(r"[。.]$")

MAINLAND = {
    "視頻": "影片", "軟件": "軟體", "硬件": "硬體", "信息": "資訊／訊息", "默認": "預設", "設置": "設定",
    "登錄": "登入", "屏幕": "螢幕", "鼠標": "滑鼠", "打印": "列印", "搜索": "搜尋", "菜單": "選單",
    "窗口": "視窗", "服務器": "伺服器", "內存": "記憶體", "硬盤": "硬碟", "短信": "簡訊", "二維碼": "QR Code",
    "鏈接": "連結", "文件夾": "資料夾", "加載": "載入", "緩存": "快取", "兼容": "相容", "分辨率": "解析度",
    "粘貼": "貼上", "界面": "介面", "交互": "互動", "反饋": "回饋", "推送": "推播", "激活": "啟用",
    "刷新": "重新整理", "獲取": "取得", "模板": "範本", "插件": "外掛", "代碼": "程式碼", "算法": "演算法",
    "數字化": "數位化", "頭像": "大頭貼", "點贊": "按讚", "賬": "帳", "用戶": "使用者", "質量": "品質",
    "網絡": "網路", "移動端": "行動版", "智能": "智慧", "優化": "改善／最佳化", "性價比": "CP 值",
}

HABITS = (
    (re.compile(r"不僅[^。！？]{0,20}[更還]"), "is the second half really a step further, or just another item?"),
    (re.compile(r"不只是[^。！？]{0,16}更是|不是[^。！？]{0,16}而是"), "does anyone actually think the first half?"),
    (re.compile(r"至關重要|不可或缺|扮演[^。]{0,6}角色"), "what goes wrong without it? say that instead"),
    (re.compile(r"賦能|助力|打造|無縫|全方位|一站式|深耕|引領"), "who does what to whom? name the action"),
    (re.compile(r"值得注意的是|需要注意的是|值得一提的是"), "drop the lead-in and start with the difference"),
    (re.compile(r"總而言之|綜上所述|總結來說|讓我們一起"), "does this line add anything the slide has not said?"),
    (re.compile(r"在這個[^。]{0,10}的時代|隨著[^。]{0,12}的發展"), "start from the first sentence that carries information"),
    (re.compile(r"透過[^。，]{0,14}來[^。，]"), "is 透過 naming a channel, or is the verb enough?"),
    (re.compile(r"進行[^。，]{0,2}(討論|調整|修改|設定|確認|分析|評估|溝通|優化|測試)"), "can the second word be the verb?"),
    (re.compile(r"是否"), "in a question to the reader, 「要…嗎？」 reads as a person asking"),
)


class SlideText(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, bool]] = []
        self.skip = 0
        self.blocks: list[tuple[bool, str]] = []
        self._buf: list[str] = []
        self._buf_headline = False

    def _in_headline(self) -> bool:
        return any(flag for _, flag in self.stack)

    def _flush(self) -> None:
        text = re.sub(r"\s+", " ", "".join(self._buf)).strip()
        if text:
            self.blocks.append((self._buf_headline, text))
        self._buf = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in VOID_TAGS:
            if tag == "br":
                self._buf.append(" ")
            return
        classes = set((dict(attrs).get("class") or "").split())
        headline = tag in HEADLINE_TAGS or bool(classes & HEADLINE_CLASSES)
        if tag in SKIP_TAGS:
            self.skip += 1
        if headline and not self._in_headline():
            self._flush()
            self._buf_headline = True
        elif tag in {"p", "li", "div", "td", "th", "figcaption", "section"} and not self._in_headline():
            self._flush()
            self._buf_headline = False
        self.stack.append((tag, headline))

    def handle_endtag(self, tag: str) -> None:
        if tag in VOID_TAGS:
            return
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                closing = self.stack[index:]
                del self.stack[index:]
                if any(name in SKIP_TAGS for name, _ in closing):
                    self.skip = max(0, self.skip - sum(name in SKIP_TAGS for name, _ in closing))
                if any(flag for _, flag in closing) and not self._in_headline():
                    self._flush()
                    self._buf_headline = False
                break

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self._buf.append(data)

    def close(self) -> None:
        super().close()
        self._flush()


def review(path: Path) -> list[str]:
    parser = SlideText()
    parser.feed(path.read_bytes().decode("utf-8", errors="replace"))
    parser.close()
    notes: list[str] = []
    has_cjk = re.compile(rf"[{CJK}]")
    yours = 0
    for headline, text in parser.blocks:
        if not has_cjk.search(text):
            continue
        short = text if len(text) <= 36 else text[:34] + "…"
        cjk_len = len(re.findall(rf"[{CJK}]", text))
        if headline:
            if cjk_len <= 24 and HEADLINE_COMMA.search(text):
                notes.append(f"headline pauses on a comma: 「{short}」 — can it read straight through, or move the second half to the subhead?")
            if FINAL_STOP.search(text):
                notes.append(f"headline ends in a full stop: 「{short}」")
        if HALF_WIDTH.search(text):
            notes.append(f"half-width punctuation in Chinese text: 「{short}」 — use ，：？！")
        if ASCII_ELLIPSIS.search(text):
            notes.append(f"three dots after Chinese: 「{short}」 — use …")
        for term, local in MAINLAND.items():
            if term in text:
                notes.append(f"「{term}」 in 「{short}」 — Taiwan usage is usually 「{local}」")
        for pattern, question in HABITS:
            match = pattern.search(text)
            if match:
                notes.append(f"「{match.group(0)}」 in 「{short}」 — {question}")
        yours += len(re.findall(r"[你您]的", text))
    if yours > 3:
        notes.append(f"「你的／您的」 appears {yours} times — most can go unless ownership is unclear")
    return notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--quiet", action="store_true", help="print only files with notes")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    files: list[Path] = []
    for path in args.paths:
        files.extend(sorted(path.rglob("*.html")) if path.is_dir() else [path])
    total = 0
    for path in files:
        notes = review(path)
        total += len(notes)
        if notes or not args.quiet:
            print(f"{path.as_posix()}: {len(notes)} note(s)")
        for note in notes:
            print(f"  - {note}")
    print(f"\n{len(files)} file(s), {total} note(s). Advisory only — nothing here blocks delivery.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
