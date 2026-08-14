# toe-latin

Renders every page in Pig Latin. Educational AND unhinged.

## What it does

`on_load` walks the raw HTML and translates each run of alphabetic text:
- words starting with a consonant shift the leading consonant cluster to
  the end plus "ay" (`toe` → `oetay`)
- words starting with a vowel get "yay" (`echo` → `echoyay`)

Tags and attributes are preserved untouched, so the page still renders and
links still work. Capitalization is preserved.

## Using it

Nothing to do — the toe is always on. Navigate anywhere and read the
results. (That's the joke.)

## Hooks used

- `on_load` — the translation

## Uninstall

Any time from the ToeHub: open `toe://hub`, find toe-latin, and click
**uninstall**. Your pages will speak English again.
