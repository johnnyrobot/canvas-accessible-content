# Canvas content style rules

The normative rules for Canvas page content. Target is **WCAG 2.1 Level AA**.

## Structure

- **Never use `<h1>`.** Canvas renders the page title as the H1. A second one breaks
  the document outline. It is also absent from the tag allowlist.
- **Headings start at `<h2>`**, then `<h3>`, `<h4>` in order. Never skip a level to get
  a font size.
- **No document-structure elements.** No `<!DOCTYPE>`, `<html>`, `<head>`, `<body>`.
  A page body is a fragment.
- **No stylesheets.** Inline `style` attributes only — see `html-allowlist.md` for why
  this is not a contradiction.
- Containers and `<div>`s are fine. Use semantic elements (`<section>`, `<nav>`,
  `<header>`, `<footer>`, `<article>`, `<aside>`) where they fit.
- Navigation links get `aria-label` or `aria-labelledby`.

## Color and contrast

- Normal text: **4.5:1** minimum against its background.
- Large text (18pt / 24px, or bold 14pt / 18.66px): **3:1** minimum.
- Keep existing color coding when editing — darken or lighten to reach the ratio rather
  than flattening everything to black.
- Never use color alone to carry meaning.

Measure, do not estimate:

```bash
python3 scripts/contrast.py page.html
```

The script reports every failing text run with its computed ratio. A color that "looks
dark enough" routinely lands at 3.9:1.

## Text

- Correct spelling, grammar, and syntax.
- Rewrite for clarity and readability where sentences are awkward; do not change meaning.
- Remove underlining from anything that is not a link — underline reads as "link".
- Use `<strong>` and `<em>`, not styling attributes, to carry emphasis.
- Convert plain text input into accessible HTML rather than pasting it raw.

## Links

- Link text describes its destination. Never "click here", "read more", or a bare URL.
- Write URLs as natural descriptive text: `<a href="...">How do I submit an
  assignment?</a>`, not `<a href="...">https://...</a>`.
- External links: `target="_blank" rel="noopener"`.

## Images

- Every image needs `alt`. Keep it under 80 characters (the templates' own guidance
  says under 120; use 80 as the working limit and never exceed 120).
- `alt` describes content or function, not "image of".
- An image whose existing alt text reads `decorative` gets `alt=""` — do not write
  new alt text for it.
- Wrap image + caption in `<figure>`, with `<figcaption>` **after** the `<img>`.
- Banner images stay at the top of the page.
- If a page has no images, a content-relevant copyright-free image may be added from
  pexels.com or unsplash.com, placed at the top but **below** any banner, at least
  400×400 px.
- Videos need descriptive text alongside them.

## Tables

- Always include a `<caption>`, center-aligned.
- `<th>` elements must carry `scope="col"` or `scope="row"`.
- Keep existing table sizing. If none is specified, use `width="100%"` and `border="1"`.
- Left-align header, row, and column text unless told otherwise.
- Ledger style: alternating row colors. Both row colors must clear contrast against the
  text on them.
- Keep the structure simple — no merged cells or nested tables.

## Lists

Use `<ul>` / `<ol>` with `<li>`. Never fake a list with `<br>` and hyphens or bullet
characters — a screen reader announces a real list's length and position.

## Icons

Decorative icons and glyphs get `aria-hidden="true"`. An icon that carries meaning gets
a text alternative.

## Math

- LaTeX via the Canvas Equations Editor format only.
- The rendered form Canvas produces:

```html
<img class="equation_image"
     title="\displaystyle \sqrt{x}"
     src="/equation_images/%255Cdisplaystyle%2520%255Csqrt%257Bx%257D?scale=1"
     alt="LaTeX: \displaystyle \sqrt{x}"
     data-equation-content="\displaystyle \sqrt{x}"
     data-ignore-a11y-check="" />
```

## Content you must not invent

Never generate placeholder text for:

- **Course descriptions**
- **Student Learning Outcomes (SLOs)**

These are academic content of record. If they are missing, leave the placeholder in
place and say what is needed. Every other placeholder (`[TBD.]`, `[Instructor
description.]`) may be filled with a marker the author will replace.

## What each page type must contain

Structure from `templates.md`; this is the content checklist. When a required item is
missing, leave its placeholder and report it rather than inventing it.

| Page type | Required content |
|---|---|
| **General content page** | Title; H3 sections with body content |
| **Front page** | Course code and number; course name; schedule; location; instructor name; in-person office hours + location; optional online office hours + Zoom link; optional welcome video; course description (**never invented**); SLOs (**never invented**) |
| **Announcement** | Title; body sections only. Do not add elements beyond what was given |
| **Meet your instructor** | Name; optional photo URL (omit entirely if none — do not generate one); short bio; 3 fun facts; preferred contact method (institutional email or Canvas Inbox); response-time expectation; in-person office hours + location; optional online hours + Zoom link |
| **Module overview** | Topic name; overview; objectives; agenda split into Read / Watch / Complete |
| **Assignment instructions** | Description tied to course SLOs; step-by-step instructions; due date; page length or word count; formatting requirements (MLA/APA); technical requirements; grading method (rubric or stated criteria); weight toward final grade |
| **Discussion** | Topic name; summary; numbered discussion questions; first-response due date; whether peer replies are required and their due date |
| **Quiz instructions** | Goal and purpose tied to course objectives; number of attempts; timed or untimed, with the limit |

Missing values become `[TBD.]` — except course descriptions and SLOs, which stay
unfilled and get reported.
