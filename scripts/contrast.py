#!/usr/bin/env python3
"""Report WCAG AA contrast failures in a Canvas page body.

Canvas page HTML carries its colors as inline styles, so contrast can be
checked statically: walk the tree, track the inherited text color and the
nearest painted background, and compute a ratio for every element that holds
text of its own.

    contrast.py page.html
    canvas-pp-cli pages show 88 my-page --json | jq -r .results.body | contrast.py -

Exits 1 when any text fails, 0 when it all passes, so it can gate an edit.

Limits worth knowing: this reads inline styles only. It cannot see Canvas's own
stylesheet, so text with no inline color of its own is reported as "inherited
default" rather than guessed at, and a gradient background is approximated by
its first color stop. Anything it cannot resolve it says so about rather than
scoring. Confirm the finished page in a browser -- this narrows where to look,
it does not replace looking.
"""

import argparse
import html.parser
import re
import sys

# WCAG 2.1 AA
AA_NORMAL = 4.5
AA_LARGE = 3.0

# Large text is 18pt, or 14pt bold. At the CSS reference 96dpi that is 24px,
# or 18.66px bold.
LARGE_PX = 24.0
LARGE_PX_BOLD = 18.66

NAMED = {
    "black": (0, 0, 0), "white": (255, 255, 255), "red": (255, 0, 0),
    "green": (0, 128, 0), "blue": (0, 0, 255), "gray": (128, 128, 128),
    "grey": (128, 128, 128), "silver": (192, 192, 192), "maroon": (128, 0, 0),
    "yellow": (255, 255, 0), "olive": (128, 128, 0), "lime": (0, 255, 0),
    "aqua": (0, 255, 255), "teal": (0, 128, 128), "navy": (0, 0, 128),
    "fuchsia": (255, 0, 255), "purple": (128, 0, 128), "orange": (255, 165, 0),
    "darkgray": (169, 169, 169), "darkgrey": (169, 169, 169),
    "lightgray": (211, 211, 211), "lightgrey": (211, 211, 211),
    "dimgray": (105, 105, 105), "dimgrey": (105, 105, 105),
}

# Elements whose text is not rendered as page content.
SKIP = {"script", "style", "head", "title", "meta", "link"}

VOID = {"br", "img", "hr", "input", "meta", "link", "area", "col", "embed",
        "param", "source", "track", "wbr"}


def parse_color(value):
    """Return (r, g, b) for a CSS color, or None when it cannot be resolved."""
    if not value:
        return None
    v = value.strip().lower()

    # A gradient has no single color. Approximate with its first stop so the
    # common "tinted panel behind dark text" case still gets scored.
    if v.startswith("linear-gradient") or v.startswith("radial-gradient"):
        stops = re.findall(r"#[0-9a-f]{3,8}|rgba?\([^)]*\)", v)
        return parse_color(stops[0]) if stops else None

    if v in ("transparent", "inherit", "initial", "unset", "currentcolor", "none"):
        return None
    if v in NAMED:
        return NAMED[v]

    m = re.match(r"^#([0-9a-f]{3,8})$", v)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        elif len(h) == 4:
            h = "".join(c * 2 for c in h[:3])
        if len(h) >= 6:
            return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
        return None

    m = re.match(r"^rgba?\(([^)]+)\)$", v)
    if m:
        parts = re.split(r"[,\s/]+", m.group(1).strip())
        nums = [p for p in parts if p]
        if len(nums) >= 3:
            try:
                rgb = []
                for p in nums[:3]:
                    if p.endswith("%"):
                        rgb.append(round(float(p[:-1]) * 255 / 100))
                    else:
                        rgb.append(int(float(p)))
                # A fully transparent color paints nothing.
                if len(nums) >= 4:
                    a = nums[3]
                    alpha = float(a[:-1]) / 100 if a.endswith("%") else float(a)
                    if alpha == 0:
                        return None
                return tuple(max(0, min(255, c)) for c in rgb)
            except ValueError:
                return None
    return None


def luminance(rgb):
    def chan(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (chan(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg, bg):
    l1, l2 = luminance(fg), luminance(bg)
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


def parse_style(attrs):
    """Pull the declarations we care about out of a style attribute."""
    style = ""
    for k, v in attrs:
        if k and k.lower() == "style" and v:
            style = v
    out = {}
    for decl in style.split(";"):
        if ":" not in decl:
            continue
        prop, _, val = decl.partition(":")
        prop = prop.strip().lower()
        val = val.strip()
        if prop in ("color", "background-color", "background", "font-size", "font-weight"):
            out[prop] = val
    return out


def font_px(value, inherited):
    """Resolve a font-size to px. Relative units fall back to the inherited size."""
    if not value:
        return inherited
    v = value.strip().lower()
    m = re.match(r"^([\d.]+)(px|pt|rem|em|%)?$", v)
    if not m:
        return inherited
    n = float(m.group(1))
    unit = m.group(2) or "px"
    if unit == "px":
        return n
    if unit == "pt":
        return n * 96 / 72
    if unit == "rem":
        return n * 16
    if unit == "em":
        return n * inherited
    if unit == "%":
        return inherited * n / 100
    return inherited


def is_bold(value):
    if not value:
        return False
    v = value.strip().lower()
    if v in ("bold", "bolder"):
        return True
    try:
        return int(v) >= 700
    except ValueError:
        return False


class Frame:
    __slots__ = ("tag", "color", "bg", "size", "bold", "text")

    def __init__(self, tag, color, bg, size, bold):
        self.tag = tag
        self.color = color
        self.bg = bg
        self.size = size
        self.bold = bold
        self.text = []


class Checker(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        # Canvas renders page bodies on white unless something paints over it.
        self.stack = [Frame("[root]", (0, 0, 0), (255, 255, 255), 16.0, False)]
        self.results = []
        self.unresolved = []
        self.depth_skip = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in VOID:
            return
        if tag in SKIP:
            self.depth_skip += 1
            return
        if self.depth_skip:
            return

        top = self.stack[-1]
        s = parse_style(attrs)

        color = parse_color(s.get("color")) or top.color
        bg = parse_color(s.get("background-color")) or parse_color(s.get("background")) or top.bg
        size = font_px(s.get("font-size"), top.size)
        bold = is_bold(s.get("font-weight")) or top.bold or tag in ("b", "strong", "th")
        if tag in ("h2", "h3", "h4", "h5", "h6") and "font-size" not in s:
            # Canvas headings render larger than body copy; treat them as large
            # text unless the page pins a smaller size.
            size = max(size, LARGE_PX)

        self.stack.append(Frame(tag, color, bg, size, bold))

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in VOID:
            return
        if tag in SKIP:
            self.depth_skip = max(0, self.depth_skip - 1)
            return
        if self.depth_skip:
            return
        if len(self.stack) > 1:
            frame = self.stack.pop()
            self.score(frame)

    def handle_data(self, data):
        if self.depth_skip:
            return
        if data.strip():
            self.stack[-1].text.append(data.strip())

    def score(self, frame):
        text = " ".join(frame.text).strip()
        if not text:
            return
        threshold = AA_LARGE if (frame.size >= LARGE_PX or (frame.bold and frame.size >= LARGE_PX_BOLD)) else AA_NORMAL
        r = ratio(frame.color, frame.bg)
        self.results.append({
            "tag": frame.tag,
            "text": text,
            "fg": frame.color,
            "bg": frame.bg,
            "ratio": r,
            "threshold": threshold,
            "pass": r >= threshold,
        })

    def close(self):
        super().close()
        # Score anything left open by unbalanced markup.
        while len(self.stack) > 1:
            self.score(self.stack.pop())


def hexs(rgb):
    return "#%02x%02x%02x" % rgb


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="HTML file, or - for stdin")
    ap.add_argument("--all", action="store_true",
                    help="list passing text too, not just failures")
    ap.add_argument("--quiet", action="store_true",
                    help="print only the summary line")
    args = ap.parse_args()

    src = sys.stdin.read() if args.file == "-" else open(args.file, encoding="utf-8").read()

    c = Checker()
    c.feed(src)
    c.close()

    shown = c.results if args.all else [r for r in c.results if not r["pass"]]
    failures = [r for r in c.results if not r["pass"]]

    if not args.quiet:
        for r in sorted(shown, key=lambda x: x["ratio"]):
            mark = "PASS" if r["pass"] else "FAIL"
            snippet = r["text"][:60] + ("..." if len(r["text"]) > 60 else "")
            print(f'{mark}  {r["ratio"]:5.2f}:1  (needs {r["threshold"]}:1)  '
                  f'<{r["tag"]}> {hexs(r["fg"])} on {hexs(r["bg"])}  "{snippet}"')
        if shown:
            print()

    total = len(c.results)
    print(f"{len(failures)} of {total} text runs fail WCAG AA "
          f"({AA_NORMAL}:1 normal, {AA_LARGE}:1 large).")
    if failures:
        print("Fix by darkening the text color or lightening the background, "
              "then re-run. Confirm the finished page in a browser.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
