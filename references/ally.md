# Anthology Ally: what it flags and how to clear it

Many institutions run Anthology Ally (formerly Blackboard Ally) in Canvas. It scores
every page and file against WCAG 2.2 AA plus its own usability checks, and shows the
results in a course accessibility report and an instructor feedback panel. These notes
come from hands-on tests and from tracing a real course report back to its HTML.

## Ally cannot see the theme

Ally scores the stored page HTML, not the rendered page. Colors that come from the
Canvas theme, a DesignPLUS stylesheet, or any other CSS are invisible to it.

- Text given an inline light color (often `color: #ffffff`) inside a card or banner
  whose dark background comes from a theme class is scored as **white on white**. In
  Ally's preview the text disappears. `scripts/contrast.py` reports the same thing,
  because it also assumes a white background when none is inline.
- **Fix:** remove the inline color so the text takes the normal text or link color, or
  put the dark background inline on the same element or a close ancestor so the pair
  travels together.

## Heading order

The issue reads "The HTML content does not have an appropriate heading structure", and
the panel says a heading "skips a level".

- Ally treats the Canvas page title as the h1. Pages that start at h2 are not flagged.
- Headings inside components count: accordion panel headings, card titles, tab labels,
  and answer choices written as headings. An `<h5>` choice inside an `<h3>` section is
  the most common cause.
- Text pasted from another tool can carry an h1 to h3 in the middle of a block.
- **Fix:** set each heading's level from where it sits. Keep its class. DesignPLUS and
  similar tools find panel headings by class, not by level, so the component keeps
  working. Run `scripts/headings.py` on the stored body.
- Ally does not flag every skipped level every time, so a clean score is not proof of a
  clean outline. Check the HTML.

## Image files are scored on their own

The issue reads "The image does not have a description". The flagged items are image
**files**, not images inside pages.

- Alt text on a page where the image appears clears the file's flag.
- Marking the image decorative in Canvas (`alt=""`) does **not** clear it. Neither does
  leaving the file unused. Hidden files still count.
- Ally's panel offers a description, "Auto-generate description" (where the institution
  turned it on), or "Indicate image is decorative". Those choices are stored in Ally,
  not in Canvas, so no Canvas API write can make them.
- Deleting unused files removes them from the report.
- A course import or copy brings every file along, so expect a batch of these flags
  afterwards.

## Images with text in them

"The image has contrast issues" means text drawn into the image fails contrast. The fix
is a new image, or real text beside a plain image.

## HTML files in Files

An `.html` file uploaded to Files is scored as a document. It needs `<html lang="...">`
and a `<title>`, or it gets "does not have a language set" and "is missing a title".
Do not leave test files in a course.

## Checking

- Ally rescored new or changed content within about 90 seconds in testing.
- Opening the report and the feedback panel changes nothing. The panel's Apply and Add
  buttons do write, to Ally.
