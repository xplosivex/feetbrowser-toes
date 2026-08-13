# 🦶 FeetBrowser Toes

The official toe catalog for [FeetBrowser](https://github.com/JuiceyDew/FeetBrowser)'s
Toes extension system.

FeetBrowser ships with **no toes by default**. To install some, open the
browser and navigate to **`toe://hub`** (or `toehub://`) — the ToeHub reads
this catalog and lets you install and uninstall toes from inside the browser.

## Adding a toe

A toe is a folder with a `toe.json` manifest and an entry `.py` module that
exposes `activate(ctx)`:

```
name-of-toe/
    toe.json     # { "name", "version", "description", "entry" }
    toe.py       # the code, exposing activate(ctx)
```

To ship a new toe here:

1. Create the folder with `toe.json` + `toe.py`. See any existing toe for
   the shape — each is a single-file module using only the framework hooks
   (`on_load`, `extra_css`, `handle`, `on_draw`, `buttons`, `on_click`,
   `on_keypress`, `on_motion`, `chrome_bands`, `on_chrome_draw`,
   `on_chrome_click`, `on_new_tab`) plus the context helpers
   (`ctx.open`, `ctx.popup`, `ctx.set_status`, `ctx.settings`).
2. Add a matching entry to `index.json` (`files` lists the files the hub
   should download; keep it single-file where possible).
3. Open a PR.

The catalog URL in `index.json` is what the browser's ToeHub fetches; keep
`files` in sync with what's actually in the repo.

## Catalog

| Toe | Description |
|-----|-------------|
| word-count | Counts the words on every page |
| toe-scheme | Registers the `toe://` scheme (`toe://hello`, `toe://gallery`) |
| sock-detective | Foot-themed devtools: sniff mode + `toe://sock` case files |
| toe-bar | A 2003-style toolbar: marquee, ads, popups, web ring |
| dark-mode | A dark theme for every page |
| reader | Strips pages down to article text |
| session-keeper | Remembers and restores open tabs via `session://` |
| toe-latin | Renders every page in Pig Latin |
| keyboard-ninja | Vim-style `j`/`k`/`gg`/`G` scrolling |

## Installing manually

Drop any toe folder into FeetBrowser's `toes/` directory and restart the
browser. Or use the CLI:

```bash
python3 -m feetbrowser --toe-install dark-mode
python3 -m feetbrowser --toe-uninstall toe-bar
python3 -m feetbrowser --toes
```
