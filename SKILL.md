---
name: canvas-accessible-content
description: Use when creating, editing, or reviewing Canvas LMS course content — pages, front pages, announcements, assignments, discussions, quizzes, module overviews — or when checking Canvas HTML for accessibility, ADA, or WCAG AA compliance, contrast ratios, alt text, or heading structure. Also use when driving canvas-pp-cli or the Canvas API to read or write course content.
---

# Canvas accessible content

Author and remediate Canvas LMS content to WCAG 2.1 Level AA, and get the change to
actually land.

**Core principle: stored HTML is not rendered output.** Canvas silently strips markup
it disallows, supplies its own theme colors for anything you did not style inline, and
answers a write it ignored with HTTP 200. Every one of those failures looks like
success from the API. Measure what you cannot see, and confirm what rendered — not what
you sent.

## When to use

- Creating any Canvas page, announcement, assignment, discussion, or quiz
- Fixing low contrast, missing alt text, bad heading order, or a table without headers
- An accessibility or ADA review of existing course HTML
- Any read or write of Canvas content through `canvas-pp-cli` or the API

**Not for:** Canvas administration that does not touch content HTML — enrollments,
grading, roster or at-risk reporting. Use `canvas-pp-cli` directly for those.

## Workflow

**1. Read the current state.** Fetch the live body with `--no-cache`. If you are
starting a new page, take the matching structure from `references/templates.md` instead
of inventing layout.

**2. Diagnose before changing anything.** If the task is "fix the contrast" or "this
text is too light", find out *which* text actually fails:

```bash
python3 scripts/contrast.py /tmp/page.html
```

The script prints every text run with its computed ratio. Fix what it reports. If it
reports nothing and the user still sees a problem, the cause is Canvas's theme or the
page chrome, not the page body — say so and ask which element they mean rather than
editing at random.

**3. Edit against the rules.** `references/style-rules.md` is normative;
`references/html-allowlist.md` says what Canvas will keep.

**4. Write it back.** Prefer a named flag. Use `--stdin` only where no flag exists, and
nest the JSON under the resource key. See `references/cli-workflow.md`.

**5. Verify all three ways.** Re-read the stored body to see what the sanitizer kept,
re-run the contrast check on what came back, and **look at the rendered page**. Report
success only after step 5.

## Non-negotiables

- **Never `<h1>`.** Canvas renders the page title as the H1. Start at `<h2>`.
- **Measure contrast, never estimate.** 4.5:1 normal text, 3:1 large.
- **Never invent course descriptions or Student Learning Outcomes.** Leave the
  placeholder and report what is missing. Every other placeholder may be filled with
  `[TBD.]`.
- **Never restyle a template.** Fill placeholders, delete unneeded sections.
- **Alt text on every image**, under 80 characters. Existing alt text reading
  `decorative` becomes `alt=""`.
- **Descriptive link text.** Never "click here" or a bare URL.

## Common mistakes

These are drawn from a real session where an agent reported a contrast fix that never
reached the page.

| Mistake | What happens | Instead |
|---|---|---|
| Guessing which text is "too light" | Fixes an element that already passed; the real problem remains | Run `contrast.py` and fix what it reports |
| Confirming the stored HTML contains your change | The markup is there, the page still renders wrong | Open the rendered page; read computed style, not markup |
| Treating HTTP 200 as proof | Canvas accepts and ignores unknown parameters | Re-read the resource; keep `--verify-writes=on` |
| Inventing a `--stdin` key like `wiki_page_body` | 200, page unchanged | Nest it: `{"wiki_page": {"body": "..."}}`, or use `--wiki-page-body` |
| Using `--compact` to fetch a body | The body field is stripped | `--json --no-cache`, read `.results.body` |
| Adding a `<style>` block | Canvas strips it entirely | Inline `style` attributes only |
| Assuming the DOM color is what paints | `opacity`, `filter`, and `-webkit-text-fill-color` override it | Screenshot it |

## Red flags — stop

- About to say "the change is live" without having looked at the page
- About to pick a color because it "looks dark enough"
- About to write a course description or SLO that the user did not supply
- About to retry a failed `--stdin` write with the same body shape
- The CLI printed `the write did not apply` and you are treating it as a warning

## Reference

| File | Contents |
|---|---|
| `references/style-rules.md` | Normative style rules; required content per page type |
| `references/html-allowlist.md` | Tags, attributes, protocols, and style properties Canvas keeps |
| `references/templates.md` | 8 ready page templates + brand color rules |
| `references/cli-workflow.md` | Verified `canvas-pp-cli` read/write/verify commands |
| `scripts/contrast.py` | WCAG AA contrast checker; exit 1 on any failure |
