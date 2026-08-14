# sock-detective

A hard-boiled private investigator for page guts. Devtools with a noir
voice.

## What it does

Two modes of operation:

**Sniff mode** — the interactive part.
- Click the **sock** toolbar button to toggle sniffing.
- Hover the page: a red crime-scene box snaps onto the element under your
  cursor, and the status bar names it (`tag#id.class`, attributes, box
  coordinates).
- `Esc` hangs it up.

**Case files** — `toe://sock` reports, rendered through the real pipeline:

| URL | Case file |
|-----|-----------|
| `toe://sock` | THE CASE FILE — page vitals |
| `toe://sock/dom` | FOOTPRINTS — the DOM tree |
| `toe://sock/layout` | THE BONES — every layout box with geometry |
| `toe://sock/style` | FIBERS — computed styles per element |
| `toe://sock/js` | THE SCRIPTURES — the JavaScript console |
| `toe://sock/toes` | THE FEET — installed toes + enabled/disabled |
| `toe://sock/cases` | THE PAPER TRAIL — every navigation witnessed |
| `toe://sock/errors` | DISTRESS — pages that went wrong |
| `toe://sock/help` | WHERE TO LOOK |

Every navigation is logged (via the `handle` hook, returning `None` so the
browser still fetches normally), which powers the paper trail and distress
reports.

## Using it

- Toggle sniff mode: click the **sock** button, then hover. `Esc` exits.
- Open any case file by typing its `toe://sock/...` URL.

## Hooks used

- `buttons` / `on_click` — the sock button
- `on_motion` / `on_draw` — the hover crime-scene box
- `on_keypress` — `Esc` exits sniff mode
- `handle` — the case-file pages + paper trail logging

## Uninstall

Any time from the ToeHub: open `toe://hub`, find sock-detective, and click
**uninstall**.
