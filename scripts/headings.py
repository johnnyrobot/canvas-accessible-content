#!/usr/bin/env python3
"""Report heading-outline problems in a Canvas page body.

Canvas shows the page title as the h1, so the body's outline starts under it.
This walks every <h1>..<h6> in order and reports:

  - any <h1> in the body (Canvas already supplies one)
  - any heading more than one level deeper than the one before it
    (h3 -> h5, or a body that opens at h3)

Headings inside components count. Accordion panel headings, card titles, and
answer choices written as <h5> under an <h3> section are the usual cause of
Ally's "The HTML content does not have an appropriate heading structure".

    headings.py page.html
    canvas-pp-cli pages show 88 my-page --json --no-cache | jq -r .results.body | headings.py -

Exits 1 when it finds a problem, 0 when the outline is clean. Stdlib only.
"""

import argparse
import html.parser
import sys


class Outline(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.heads = []  # [level, text, line]
        self._open = None

    def handle_starttag(self, tag, attrs):
        if len(tag) == 2 and tag[0] == "h" and tag[1] in "123456":
            self._open = [int(tag[1]), "", self.getpos()[0]]

    def handle_endtag(self, tag):
        if self._open and tag == f"h{self._open[0]}":
            self._open[1] = " ".join(self._open[1].split())
            self.heads.append(self._open)
            self._open = None

    def handle_data(self, data):
        if self._open:
            self._open[1] += data


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("file", help="page body HTML, or - for stdin")
    a = ap.parse_args()
    src = sys.stdin.read() if a.file == "-" else open(a.file, encoding="utf-8").read()
    p = Outline()
    p.feed(src)
    problems = 0
    prev = 1  # the page title
    for level, text, line in p.heads:
        if level == 1:
            problems += 1
            print(f"FAIL  line {line}: <h1> in the body. Canvas renders the page title as the h1. \"{text[:70]}\"")
        elif level > prev + 1:
            problems += 1
            print(f"FAIL  line {line}: <h{level}> after <h{prev}> skips a level. \"{text[:70]}\"")
        prev = level
    print(f"\n{len(p.heads)} headings, {problems} problem(s).")
    if problems:
        print("Fix by changing the level to fit where the heading sits; keep its class so components still work.")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
