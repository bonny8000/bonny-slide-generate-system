"""Small structural HTML reader shared by slide checks (Python standard library only).

This inspects authored elements, not computed CSS. It excludes inert markup and explicit hidden
ancestors; browser rendering and human review still decide whether an image actually paints well.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from html.parser import HTMLParser
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

VOID = set("area base br col embed hr img input link meta param source track wbr".split())
INERT = {"head", "script", "style", "template", "noscript"}
HIDDEN_STYLE = re.compile(r"(?:^|;)\s*(?:display\s*:\s*none|visibility\s*:\s*(?:hidden|collapse)|opacity\s*:\s*0(?:\.0*)?)(?:\s*!important)?\s*(?:;|$)", re.I)
URL_RE = re.compile(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", re.I)


@dataclass
class Element:
    tag: str
    attrs: dict[str, str]
    children: list[Element | str] = field(default_factory=list)

    @property
    def classes(self) -> set[str]:
        return set(self.attrs.get("class", "").split())

    @property
    def hidden(self) -> bool:
        return (self.tag in INERT or "hidden" in self.attrs
                or self.attrs.get("aria-hidden", "").lower() == "true"
                or bool(HIDDEN_STYLE.search(self.attrs.get("style", ""))))

    def walk(self, visible: bool = False):
        if visible and self.hidden:
            return
        yield self
        for child in self.children:
            if isinstance(child, Element):
                yield from child.walk(visible)

    def text(self) -> str:
        if self.hidden:
            return ""
        return " ".join(c.text() if isinstance(c, Element) else c for c in self.children)

    def asset_urls(self) -> list[str]:
        urls = []
        if self.tag in {"img", "source", "image"}:
            for key in ("src", "href", "xlink:href"):
                if self.attrs.get(key):
                    urls.append(self.attrs[key])
            # Local output normally uses src; support common responsive file candidates too.
            for candidate in self.attrs.get("srcset", "").split(","):
                if candidate.strip() and not candidate.strip().startswith("data:"):
                    urls.append(candidate.strip().split()[0])
        urls.extend(URL_RE.findall(self.attrs.get("style", "")))
        return urls


class SlideParser(HTMLParser):
    def __init__(self, html: str):
        super().__init__(convert_charrefs=True)
        self.root = Element("document", {})
        self.stack = [self.root]
        self.feed(html)
        self.close()

    def handle_starttag(self, tag, attrs):
        node = Element(tag, {k: v or "" for k, v in attrs})
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, text):
        self.stack[-1].children.append(text)


def document(html: str) -> Element:
    return SlideParser(html).root


def slides(html: str) -> list[Element]:
    # Inert markup is not a slide, even if a template or comment contains a slide-shaped string.
    def walk(node):
        if node.tag in INERT:
            return
        if "slide" in node.classes:
            yield node
        for child in node.children:
            if isinstance(child, Element):
                yield from walk(child)
    return list(walk(document(html)))


def local_asset(url: str, html_path: Path) -> Path | None:
    parsed = urlsplit(url.replace("\\", "/"))
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    return (html_path.parent / unquote(parsed.path)).resolve()


def has_visual(html: str) -> bool:
    frames = {"phone", "appframe", "ui-mockup", "device-stack", "logo-row", "logorow"}
    for node in document(html).walk(visible=True):
        if node.tag == "img" and node.attrs.get("src", "").strip():
            return True
        if node.classes & frames and (node.text().strip() or any(isinstance(c, Element) for c in node.children)):
            return True
        if "data-editorial-explainer" in node.attrs:
            if any(child.asset_urls() for child in node.walk(visible=True)):
                return True
    return False
