# Canvas HTML editor allowlist

What Canvas keeps when it saves page, announcement, assignment, discussion, and quiz
HTML. Anything outside these lists is **silently stripped** — the write succeeds, the
markup is gone, and the response body shows the sanitized version.

That silence is the trap: a page can save cleanly and still lose the element you added.
After writing, re-read the body and confirm your markup survived (see `cli-workflow.md`).

## Allowed tags

```
a, acronym, address, area, article, aside, audio, b, bdo, big, blockquote, br,
caption, cite, code, col, colgroup, dd, del, details, dfn, div, dl, dt, em, embed,
footer, h2, h3, h4, h5, h6, header, hr, i, img, ins, iframe, kbd, legend, li, map,
nav, object, ol, p, param, picture, pre, q, ruby, rp, rt, samp, section, small,
span, strike, strong, sub, summary, sup, table, tbody, td, tfoot, th, thead, time,
tr, track, tt, u, ul, var, video
```

Note what is absent: **`h1` is not on the list**, and neither are `html`, `head`,
`body`, `!DOCTYPE`, `form`, `input`, `button`, `script`, or `style` blocks. Page
bodies are document *fragments*.

## Allowed MathML tags

```
annotation, annotation-xml, maction, maligngroup, malignmark, math, menclose,
merror, mfenced, mfrac, mglyph, mi, mlabeledtr, mlongdiv, mmultiscripts, mn, mo,
mover, mpadded, mphantom, mprescripts, mroot, mrow, ms, mscarries, mscarry,
msgroup, msline, mspace, msqrt, msrow, mstack, mstyle, msub, msubsup, msup,
mtable, mtd, mtext, mtr, munder, munderover, none, semantics, mark
```

## Attributes

**Every element** may carry: `style`, `class`, `id`, `title`, `role`, `lang`, `dir`.

| Element | Additional allowed attributes |
|---|---|
| `a` | `href`, `target`, `name` |
| `abbr` | `title` |
| `area` | `alt`, `coords`, `href`, `shape`, `target` |
| `aria-*` | `labelledby`, `atomic`, `busy`, `controls`, `describedby`, `disabled`, `dropeffect`, `flowto`, `grabbed`, `haspopup`, `hidden`, `invalid`, `label`, `live`, `owns`, `relevant`, `autocomplete`, `checked`, `expanded`, `level`, `multiline`, `multiselectable`, `orientation`, `pressed`, `readonly`, `required`, `selected`, `sort`, `valuemax`, `valuemin`, `valuenow`, `valuetext` |
| `audio` | `name`, `src`, `muted`, `controls` |
| `blockquote` | `cite` |
| `col`, `colgroup` | `span`, `width` |
| `embed` | `name`, `src`, `type`, `allowfullscreen`, `pluginspage`, `wmode`, `allowscriptaccess`, `width`, `height` |
| `font` | `face`, `color`, `size` |
| `img` | `align`, `alt`, `height`, `src`, `title`, `usemap`, `width` |
| `iframe` | `src`, `width`, `height`, `name`, `align`, `allowfullscreen` |
| `map` | `name` |
| `object` | `width`, `height`, `style`, `data`, `type`, `classid`, `codebase` |
| `ol` | `start`, `type` |
| `param` | `name`, `value` |
| `q` | `cite` |
| `source` | `height`, `media`, `sizes`, `src`, `srcset`, `type`, `width` |
| `table` | `summary`, `width`, `border`, `cellpadding`, `cellspacing`, `center`, `frame`, `rules` |
| `tr` | `align`, `valign`, `dir` |
| `td` | `abbr`, `axis`, `colspan`, `rowspan`, `width`, `align`, `valign`, `dir` |
| `th` | `abbr`, `axis`, `colspan`, `rowspan`, `width`, `align`, `valign`, `dir`, `scope` |
| `ul` | `type` |
| `video` | `name`, `src`, `allowfullscreen`, `muted`, `poster`, `width`, `height`, `controls`, `playsinline` |

`scope` is on `th` only. That is the attribute that makes a data table readable by a
screen reader, and it is the one most often dropped.

## Allowed URL protocols

`ftp`, `http`, `https`, `mailto` — plus `skype` on `href`.

Applies to: `a href`, `blockquote cite`, `img src`, `q cite`, `object data`,
`embed src`, `iframe src`.

A `javascript:` or `data:` URL is stripped.

## Allowed style properties

```
background, border, border-radius, clear, color, cursor, direction, display, flex,
float, font, grid, height, left, line-height, list-style, margin, max-height,
max-width, min-height, min-width, overflow, overflow-x, overflow-y, padding,
position, right, text-align, table-layout, text-decoration, text-indent, top,
vertical-align, visibility, white-space, width, z-index, zoom
```

### The `style` tension, resolved

`style-rules.md` says not to add CSS. This allowlist permits `style` on every element,
and the templates in `templates.md` use inline `style` heavily. Both are right, and
they are not in conflict:

- **Allowed and expected:** inline `style` attributes, which is the only styling
  mechanism Canvas keeps. The templates depend on them.
- **Not allowed:** `<style>` blocks and stylesheets. Canvas strips them, and a
  `<style>` element is not on the tag allowlist at all.

So "do not add CSS" means *do not write a stylesheet*. Set colors and spacing with
inline `style` attributes, using only the properties listed above.

Because inline styles are the only mechanism, **there is no cascade to fall back on**.
Text with no inline `color` inherits from its nearest styled ancestor, or from Canvas's
own theme, which you cannot see from the API. That is why contrast has to be confirmed
in a browser and not inferred from the stored HTML.
