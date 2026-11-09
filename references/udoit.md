# UDOIT: what it flags and how to clear it

UDOIT is the open-source Canvas accessibility checker from UCF, now maintained with
Cidi Labs. Many institutions install it next to Anthology Ally. It scans every page,
assignment, discussion, quiz and HTML file, and lists each finding in its UFIXIT tab.
These notes come from tracing a real UDOIT scan of a hand-built course back to its HTML,
and from UDOIT's and phpAlly's public source.

Run `scripts/udoit_check.py` on page HTML before a course is imported or scanned. It
models the rules below and matched a live scan within a few percent.

## Two engines

- **phpAlly** (`cidilabs/phpally`, UDOIT 3.x) has the rules most institutions still
  show: "Link has nondescript text", "Page contains skipped headings", "Potential use of
  color alone…", "Alternative text is too lengthy…", "Content may exceed recommended
  length… (3000+ words)", "Styles might be used instead of semantic markup…".
- **IBM Equal Access** (UDOIT 4 on `main`) replaces several of those with its own
  rules. A live instance can run a mix, so trust the scan over the source.

## Potential use of color alone (usually the biggest number)

The published rule (`CssTextStyleEmphasize`) checks `<span>` and `<font>` only. A live
scan also flagged `<p>`, `<li>`, `<a>` and headings. What triggers it:

- The element has an inline `color`, `background-color` or `background`.
- Black or white text and a white background do not count.
- The element has no inline `font-weight` or `font-style`.
- Its text is not wrapped whole in an emphasis element (`strong`, `b`, `em`, `small`,
  `sup`, `sub`, `a`), and it is not the whole text of a block parent.
- Wrappers (`div`, `section`, `aside`, `header`, `nav`) are not checked.

A page that repeats `color: #003B5C` on every paragraph gets one finding per paragraph,
hundreds per course. **Fixes that do not change how the page looks:**

1. Set the text color once on a wrapper and let paragraphs inherit it. Drop any inline
   color that equals the color the element would inherit.
2. For a label already drawn bold through the `font` shorthand, wrap its text in
   `<strong>`. **Canvas strips an inline `font-weight`**, so spelling the weight out does
   not survive the save.
3. Do not wrap a whole `<p>` in `<strong>`. That trades this finding for
   "Styles might be used instead of semantic markup".

Links keep their own color; a link's color is never inherited. Colored links, colored
labels and colored bands that remain after these fixes are design choices: make the
text bold, move the color to a wrapper, or accept the finding as a false positive.

## Link has nondescript text

- Link text that is exactly "click here", "click", "more" or "here".
- Link text that is the URL itself (`<a href="https://…">https://…</a>`), which is how
  a sources list usually ends up.
- **Fix:** make the citation or a description the link text.

## Styles might be used instead of semantic markup for structure

- A `<p>` whose whole text is one `<strong>`, `<b>`, `<u>` or `<font>`, or a `<p>` with
  inline `font-weight: bold`, reads as a fake heading.
- In the live scan, runs that end in `:` `,` `;` `-` or `.`, or that run past 10 words,
  were not flagged ("Correct." passes; "Try it" does not; a bold question ending in "?"
  does not pass).
- **Fix:** make real sub-headings real headings at the right level, or let the bold run
  into the sentence that follows (`<p><strong>Try it.</strong> Open…</p>`).

## Page contains skipped headings

- The first heading must be `h1` or `h2`, and no heading may go more than one level
  deeper than the one before. Going back up is fine. See `scripts/headings.py`.

## Alternative text is too lengthy

- `alt` longer than 150 characters (counted in bytes). Move detail into a caption or the
  text, and keep `alt` to what the image shows.

## Content may exceed recommended length (3000+ words)

- More than 3000 words on one page. Split the page, or accept it for long readings.

## Reading the report

- UFIXIT hides unpublished and unused content by default. Turn both filters off to see
  everything a re-import will carry.
- The page search matches loosely, so it counts by design or prefix rather than by page.
- "Review" opens a fix form. Opening it changes nothing; Save writes to the course.
