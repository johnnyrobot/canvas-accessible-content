#!/usr/bin/env python3
"""Pre-check Canvas page HTML for the issues UDOIT reports, before the course is scanned.

UDOIT (the open-source Canvas accessibility checker from UCF / Cidi Labs) runs the
phpAlly rule set in many institutions. This script reimplements the rules that most
often fire on hand-built pages, so a page can be fixed before export or import:

  color-alone        "Potential use of color alone to communicate information"
                     (phpAlly CssTextStyleEmphasize, as observed in a live scan)
  nondescript-link   "Link has nondescript text" (AnchorSuspiciousLinkText)
  styled-heading     "Styles might be used instead of semantic markup for structure"
                     (ParagraphNotUsedAsHeader, with the 10-word and end-punctuation
                     limits of the IBM text_block_heading rule, as observed)
  skipped-heading    "Page contains skipped headings" (HeadingsInOrder)
  alt-too-long       "Alternative text is too lengthy..." (ImageAltIsTooLong, > 150)
  too-long           "Content may exceed recommended length... (3000+ words)" (ContentTooLong)

The color rule here is calibrated, not copied. phpAlly's published source checks only
<span> and <font>, but a live UDOIT scan also flagged <p>, <li>, <a> and headings
that carry an inline text color or background. Matching that scan within a few
percent across five page designs took: those tags; inline `color`, `background-color`
or `background`; black or white text and white backgrounds ignored; any inline
`font-weight` or `font-style` exempting the element; and phpAlly's parent and child
exemptions. <div>, <section>, <aside> and other wrappers were not flagged, which is
why setting a text color once on a wrapper, and letting text inherit it, scans clean.
It runs a little strict: small numbered badges (hotspot markers) that the live scan did
not flag are reported here.

    udoit_check.py page.html [more.html ...]
    udoit_check.py --summary out/*.html          # counts per rule only
    canvas-pp-cli pages show 88 my-page --json --no-cache | jq -r .results.body | udoit_check.py -

Exits 1 if anything is found. Needs only the Python standard library.
"""

import argparse
import html.parser
import re
import sys
from collections import Counter

COLOR_TAGS = {"p", "li", "span", "font", "a", "h1", "h2", "h3", "h4", "h5", "h6"}
EMPH = {"b", "strong", "em", "small", "sup", "sub", "a"}
BLOCK = {"p", "td", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6"}
NONDESCRIPT = {"click here", "click", "more", "here", "read more", "learn more", "link", "this link"}
NEUTRAL_TEXT = {"#000000", "#ffffff", "black", "white", "inherit", "currentcolor", "initial", "unset"}
NEUTRAL_BG = {"#ffffff", "white", "transparent", "none", "inherit", "initial", "unset"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
ALT_LIMIT = 150
WORD_LIMIT = 3000


class Node:
    __slots__ = ("tag", "attrs", "parent", "children", "line")

    def __init__(self, tag, attrs, parent, line):
        self.tag, self.attrs, self.parent, self.children, self.line = tag, dict(attrs), parent, [], line

    def text(self):
        return "".join(c if isinstance(c, str) else c.text() for c in self.children)

    def elements(self):
        for c in self.children:
            if isinstance(c, Node):
                yield c
                yield from c.elements()

    def style(self):
        out = {}
        for part in (self.attrs.get("style") or "").split(";"):
            if ":" in part:
                k, v = part.split(":", 1)
                out[k.strip().lower()] = v.strip().lower()
        return out


class Tree(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", {}, None, 0)
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur, self.getpos()[0])
        self.cur.children.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.cur, self.getpos()[0]))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.children.append(data)


def hexnorm(v):
    v = (v or "").strip().split()[0] if v and v.strip() else ""
    m = re.fullmatch(r"#([0-9a-f]{3})", v)
    return "#" + "".join(c * 2 for c in m.group(1)) if m else v


def short(s, n=70):
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 1] + "…"


def check(src):
    t = Tree()
    t.feed(src)
    found = []

    def add(rule, node, detail):
        found.append((rule, node.line if node else 0, detail))

    els = list(t.root.elements())
    for el in els:
        st = el.style()
        # color-alone
        if el.tag in COLOR_TAGS:
            fg = hexnorm(st.get("color"))
            bg = hexnorm(st.get("background-color") or st.get("background"))
            colored = (fg and fg not in NEUTRAL_TEXT) or (bg and bg not in NEUTRAL_BG) or el.attrs.get("color")
            text = el.text().strip()
            if colored and text and "font-weight" not in st and "font-style" not in st:
                p = el.parent
                exempt = p is not None and p.tag in (EMPH | BLOCK) and p.text().strip() == text
                first = next((c for c in el.children if isinstance(c, Node) or c.strip()), None)
                exempt = exempt or (isinstance(first, Node) and first.tag in EMPH and first.text().strip() == text)
                if not exempt:
                    add("color-alone", el, f"<{el.tag}> color {fg or '-'} background {bg or '-'}: \"{short(text)}\"")
        # nondescript-link
        if el.tag == "a" and el.attrs.get("href"):
            text = " ".join(el.text().split())
            href = el.attrs["href"].strip()
            if text.lower() in NONDESCRIPT or text == href or re.fullmatch(r"(https?://|www\.)\S+", text):
                add("nondescript-link", el, f"\"{short(text)}\" -> {short(href, 50)}")
        # styled-heading
        if el.tag == "p" and el.parent is not None and el.parent.tag not in ("td", "th"):
            text = el.text().strip()
            first = next((c for c in el.children if isinstance(c, Node) or c.strip()), None)
            # As observed: bold runs that end in : , ; - . or run past 10 words are not flagged.
            headingish = len(text.split()) <= 10 and not re.search(r"[:,;\-.]$", text)
            if text and headingish and ((isinstance(first, Node) and first.tag in ("strong", "b", "font", "u") and first.text().strip() == text)
                                        or st.get("font-weight") == "bold"):
                add("styled-heading", el, f"\"{short(text)}\"")
        # alt-too-long
        if el.tag == "img" and len((el.attrs.get("alt") or "").encode()) > ALT_LIMIT:
            add("alt-too-long", el, f"{len(el.attrs['alt'])} chars: \"{short(el.attrs['alt'])}\"")
    # skipped-heading
    heads = [e for e in els if re.fullmatch(r"h[1-6]", e.tag)]
    for i, h in enumerate(heads):
        lvl = int(h.tag[1])
        if (i == 0 and lvl not in (1, 2)) or (i and lvl > int(heads[i - 1].tag[1]) + 1):
            add("skipped-heading", h, f"<{h.tag}> after <{heads[i - 1].tag if i else 'page title'}>: \"{short(h.text())}\"")
    # too-long
    if "<script" not in src.lower():
        words = len(re.findall(r"[A-Za-z'’-]+", t.root.text()))
        if words > WORD_LIMIT:
            add("too-long", None, f"about {words} words")
    return found


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="+", help="page body HTML files, or - for stdin")
    ap.add_argument("--summary", action="store_true", help="print counts per rule only")
    a = ap.parse_args()
    total = Counter()
    for f in a.files:
        src = sys.stdin.read() if f == "-" else open(f, encoding="utf-8").read()
        issues = check(src)
        total.update(r for r, _, _ in issues)
        if not a.summary:
            for rule, line, detail in issues:
                print(f"{f}:{line}  {rule:16}  {detail}")
    print("\n" + (", ".join(f"{k} {v}" for k, v in total.most_common()) or "no issues") + f"  ({len(a.files)} file(s))")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
