# Reading and writing Canvas content with canvas-pp-cli

Every command here was run against a live Canvas instance. Add `--agent` to any of
them for compact JSON with no prompts.

## Find the content

A Canvas URL tells you the course id and the page slug:

```
https://canvas.example.edu/courses/88/pages/my-page-slug
                                   ^^         ^^^^^^^^^^^^
                                   course     url_or_id
```

```bash
canvas-pp-cli courses index --agent            # courses you can reach
canvas-pp-cli pages index 88 --agent           # pages in a course
canvas-pp-cli which "update a quiz" --json     # find the command for anything else
```

## Read the body

The body lives at `.results.body`. Always `--no-cache` before an edit so you are not
editing a stale copy:

```bash
canvas-pp-cli pages show 88 my-page-slug --json --no-cache \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["results"]["body"])' \
  > /tmp/page.html
```

`--compact` strips the body — do not use it when you need the HTML.

## Write it back

### Prefer a flag

Flags carry the correct API parameter names. This is the safest path:

```bash
canvas-pp-cli pages update 88 my-page-slug \
  --wiki-page-body "$(cat /tmp/page.html)" --agent
```

### Use `--stdin` only when there is no flag, and nest it correctly

`--stdin` sends your JSON to Canvas verbatim. It does not know the endpoint's parameter
names and will not correct them. Canvas is Rails: it reads a **nested** object.

```bash
# CORRECT — nested under the resource key
python3 -c '
import json
json.dump({"wiki_page": {"body": open("/tmp/page.html").read()}}, open("/tmp/body.json","w"))
'
canvas-pp-cli pages update 88 my-page-slug --stdin --agent < /tmp/body.json
```

```bash
# WRONG — flattened key. Canvas ignores it and answers 200 with the page unchanged.
echo '{"wiki_page_body": "..."}' | canvas-pp-cli pages update 88 my-page-slug --stdin
```

The flattened form is the single most common way to "successfully" change nothing.
The CLI now catches it and exits non-zero:

```
Error: PUT /api/v1/courses/88/pages/my-page-slug returned success but the write did not apply
  the request carried "wiki_page_body", and the response object contains none of them
  "wiki_page_body" looks like a flattened Rails bracket name; the API parameter is "wiki_page[body]"
```

If you see that, fix the shape — do not retry the same body.

### `--verify-writes`

| Value | Behavior |
|---|---|
| `on` *(default)* | Fail when a flat `--stdin` body was ignored; warn otherwise |
| `warn` | Never fail; print findings to stderr |
| `off` | Skip the check |

The check proves Canvas *parsed* your parameters. It does not prove the value landed
as you intended — Canvas sanitizes HTML on save. Confirming that still needs a re-read.

## Command map by content type

| Content | Read | Write | Body parameter |
|---|---|---|---|
| Page | `pages show <course> <slug>` | `pages update <course> <slug>` | `--wiki-page-body` |
| Assignment | `assignments show <course> <id>` | `assignments update <course> <id>` | `--assignment-description` |
| Discussion | `discussion-topics show <course> <id>` | `discussion-topics update <course> <id>` | `--message` |
| Announcement | same as discussion | `discussion-topics create <course> --is-announcement` | `--message` |
| Quiz | `quizzes get-quizzes-2 <course> <id>` | `quizzes put-quizzes <course> <id>` | **no flag — `--stdin` with `{"quiz": {"description": "..."}}`** |

Quizzes are the case where `--stdin` is unavoidable. Nest under `quiz`.

For anything else: `canvas-pp-cli which "<what you want>" --json`, then `--help` on the
command it names.

## Verify — all three, in order

A write that returns HTTP 200 proves only that Canvas accepted the request.

### 1. Re-read and confirm your markup survived

Canvas silently strips disallowed tags, attributes, and style properties
(`html-allowlist.md`). The write succeeds; the markup is gone.

```bash
canvas-pp-cli pages show 88 my-page-slug --json --no-cache \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["results"]["body"])' \
  > /tmp/after.html
diff /tmp/page.html /tmp/after.html   # differences here are Canvas's sanitizer
```

### 2. Re-run the contrast check on what came back

Check the stored result, not your local draft:

```bash
python3 scripts/contrast.py /tmp/after.html
```

### 3. Look at the rendered page

**This is the step that gets skipped, and it is the one that catches real problems.**

Stored HTML is not rendered output. Inline styles are the only thing you can see from
the API; Canvas's own theme supplies everything else, including the color of any text
that has no inline `color` of its own. A body that reads correct can render wrong.

Open the page URL and confirm the change visually. If you have browser automation,
read the computed style rather than trusting the markup:

```javascript
const el = document.querySelector('.user_content blockquote p');
getComputedStyle(el).color        // what actually paints
```

Note that `getComputedStyle` reports the `color` property; `opacity`, `filter`, and
`-webkit-text-fill-color` on the element or any ancestor can still change what you see.
When the DOM says one thing and the screen says another, take a screenshot and trust it.

## Undo

Canvas versions page bodies. You do not need to keep your own backup, though keeping
the pre-edit file costs nothing:

```bash
canvas-pp-cli pages revisions 88 my-page-slug --agent
canvas-pp-cli pages revert 88 my-page-slug <revision_id> --agent
```

## Preview before a risky write

```bash
canvas-pp-cli pages update 88 my-page-slug --wiki-page-body "..." --dry-run --agent
```

`--dry-run` prints the request, including the form body and its Content-Type, without
sending it. Write verification does not run on a dry run — nothing was sent.
