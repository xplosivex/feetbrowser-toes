# session-keeper

Remembers your open tabs and lets you restore them later — or forget them.

## What it does

- Records every open tab's title + URL to a JSON file (debounced through
  the browser's `after` loop), so a crash or a coffee break doesn't cost
  you your session.
- `session://` serves a page listing the saved tabs with clickable links
  that reopen them.
- `session://clear` wipes the saved session.

## Using it

- Open `session://` to see your saved tabs; click one to restore it.
- Open `session://clear` to forget everything.
- Tabs on `session://` itself are never recorded.

## Hooks used

- `handle` — the `session://` pages
- `on_new_tab` — re-snapshot the session

## Files

The session log lives in the toe's folder as `session.json`.

## Uninstall

Any time from the ToeHub: open `toe://hub`, find session-keeper, and click
**uninstall**.
