# canvas-accessible-content

An [Agent Skill](https://agentskills.io/specification) for authoring and remediating
**Canvas LMS** course content to **WCAG 2.1 Level AA** — and for getting the change to
actually land.

Pairs with [`canvas-pp-cli`](https://github.com/johnnyrobot/canvas-pp-cli), but the
accessibility rules, templates, and contrast checker stand on their own and work
against the Canvas API, the Rich Content Editor, or a plain HTML file.

## Why this exists

Canvas fails quietly in three different ways, and all three look like success:

- It **silently strips** markup outside its allowlist. The write returns 200; your
  element is gone.
- It **supplies its own theme colors** for anything you did not style inline. The
  stored HTML looks right; the rendered page does not.
- It **ignores API parameters it does not recognize** and answers 200 with the
  unmodified resource. The write reports success and changes nothing.

This skill exists because an agent hit all three at once: asked to darken low-contrast
text on a course page, it guessed which text was too light, fixed an element that
already passed, confirmed its own change by re-reading the stored HTML, and reported
the fix as done. The page was untouched.

**Core principle: stored HTML is not rendered output.** Measure what you cannot see,
and verify what rendered — not what you sent.

## Install

Clone into your agent's skills directory:

```bash
git clone https://github.com/johnnyrobot/canvas-accessible-content \
  ~/.claude/skills/canvas-accessible-content
```

`~/.agents/skills/` works as a cross-runtime location for Codex, Copilot CLI, and
Gemini CLI. The skill is plain Markdown plus one stdlib-only Python script — no
install step, no dependencies.

## What's inside

| File | Contents |
|---|---|
| `SKILL.md` | The workflow, non-negotiables, and the mistakes that cause silent failures |
| `references/style-rules.md` | Normative style rules; required content per page type |
| `references/html-allowlist.md` | Tags, attributes, protocols, and style properties Canvas keeps |
| `references/templates.md` | 8 ready page templates + brand color rules |
| `references/cli-workflow.md` | Verified `canvas-pp-cli` read/write/verify commands |
| `scripts/contrast.py` | WCAG AA contrast checker; exits 1 on any failure |

## The contrast checker

Standalone, stdlib only, usable without the rest of the skill:

```bash
python3 scripts/contrast.py page.html
python3 scripts/contrast.py page.html --all      # show passing text too

# straight from a live Canvas page
canvas-pp-cli pages show 88 my-page-slug --json --no-cache \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["results"]["body"])' \
  | python3 scripts/contrast.py -
```

It walks the tree tracking inherited text color and the nearest painted background,
applies the large-text threshold (18pt, or bold 14pt), and reports every failing run
with its computed ratio:

```
FAIL   1.61:1  (needs 4.5:1)  <p> #cccccc on #ffffff  "This light gray text fails badly."
PASS   3.54:1  (needs 3.0:1)  <p> #888888 on #ffffff  "Large gray text, looser threshold."

1 of 6 text runs fail WCAG AA (4.5:1 normal, 3.0:1 large).
```

Exit code 1 on any failure, so it can gate an edit in CI or a pre-commit hook.

**Scope:** it reads inline styles, which is the only styling Canvas keeps. It cannot
see Canvas's own stylesheet, so text with no inline color is reported as inheriting a
default rather than guessed at, and a gradient is approximated by its first color stop.
It narrows where to look; it does not replace looking at the rendered page.

## The 8 templates

General content page · Front page · Announcement · Meet your instructor · Module
overview · Assignment instructions · Discussion board · Quiz instructions

Each is WCAG AA out of the box and parameterized by two brand colors. `{{Color_1}}`
sits behind white text and must clear 4.5:1 — a mid-tone brand color that looks right
in a logo usually fails there, which is exactly what the contrast checker is for.

Fill the placeholders and delete what you don't need. Don't restyle them; the nesting
and heading order are what make them compliant.

## Provenance

Adapted from a set of Canvas course-design guides written for a conversational
assistant. The substance — style rules, HTML allowlist, templates, per-page-type
content requirements — is carried over; the chatbot scaffolding (ask one question,
wait, present a numbered menu) is not, since agents don't work that way.

Two defects in the source templates are corrected here: 27 callout `<div>`s had an
unterminated `style` attribute (`border-radius: 5px;>` with no closing quote), and two
`<h4>` elements were closed with `</h3>`. Both would break rendering in Canvas. All
eight templates now parse clean.

The Canvas HTML allowlist is reproduced from Instructure's published
[Canvas HTML Editor Allowlist](https://community.canvaslms.com/t5/Canvas-Basics-Guide/What-HTML-elements-are-allowed-in-Canvas/ta-p/387066).

## License

Apache-2.0. See [LICENSE](LICENSE).
