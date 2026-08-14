# 🦶 FeetBrowser Toes

The official toe catalog for [FeetBrowser](https://github.com/JuiceyDew/FeetBrowser)'s
Toes extension system.

FeetBrowser ships with **no toes by default**. To install some, open the
browser and navigate to **`toe://hub`** (or `toehub://`) — the ToeHub reads
this catalog and lets you install, uninstall, enable, and disable toes from
inside the browser.

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
| word-count | Counts words (skipping scripts), estimates reading time |
| toe-scheme | Registers an `echo://` custom scheme (`echo://hello`, `echo://links`) |
| sock-detective | Foot-themed devtools: sniff mode + `toe://sock` case files (`/dom`, `/layout`, `/style`, `/js`, `/toes`, `/cases`, `/errors`) |
| toe-bar | A 2003-style toolbar: marquee, ads, popups, web ring |
| neo-bar | A full toolbar reimplemented as a toe: back/forward/reload/home/bookmark/address bar + visitor counter |
| dark-mode | A dark theme for every page, toggleable |
| reader | Strips pages down to article text, keeping links and images |
| session-keeper | Remembers and restores open tabs via `session://`, can forget |
| toe-latin | Renders every page in Pig Latin |
| keyboard-ninja | Vim-style `j`/`k`/`h`/`l`/`d`/`u`/`gg`/`G` scrolling |
| pseudo-toe | Pseudo-site hub: turns GitHub repo links into lightweight scrollable sites via `gh://` |

## Installing manually

Drop any toe folder into FeetBrowser's `toes/` directory and restart the
browser. Or use the CLI:

```bash
python3 -m feetbrowser --toe-install dark-mode
python3 -m feetbrowser --toe-uninstall toe-bar
python3 -m feetbrowser --toes
```
