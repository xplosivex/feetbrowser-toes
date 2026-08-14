# neo-bar

A full toolbar reimplemented as a toe: back, forward, reload, home,
bookmark star, an address bar, and a live visitor counter — all drawn on a
chrome band by the toe itself.

## What it does

A 34px chrome band that reimplements the browser's own toolbar entirely
through the toe framework. It reads live browser state on every draw, so it
always reflects reality:

- **‹** back (enabled when there's history)
- **›** forward (enabled when there's future)
- **⟳** reload the current page (bypassing cache)
- **⌂** go home
- **★ / ☆** toggle the bookmark on the current page
- **address bar** — click it and type; press Enter to navigate, Esc to
  cancel
- **VISITOR #NNNNNN** — increments on each new tab

## Using it

- Click any button to act on the current page.
- Click the address bar, type a URL (or search terms), press Enter.
- `neo://` opens an info page showing current URL, history, bookmarks, and
  the visitor number.

## Hooks used

- `chrome_bands` / `on_chrome_draw` / `on_chrome_click` — the band
- `on_keypress` — typing into the band's address bar
- `buttons` / `on_click` — the NB toolbar button
- `handle` — the `neo://` info page
- `on_new_tab` — the visitor counter

## Uninstall

Any time from the ToeHub: open `toe://hub`, find neo-bar, and click
**uninstall**.
