# keyboard-ninja

Vim-style navigation. Hands off the mouse.

## What it does

`on_keypress` intercepts keys when no address bar and no form field has
focus, turning the keyboard into a scroll controller. Ninja mode is
**off** by default so ordinary typing stays normal.

## Keys while ninja mode is on

| Key | Action |
|-----|--------|
| `j` / `k` | scroll down / up one step |
| `h` / `l` | scroll down / up a little (half a step) |
| `d` / `u` | half-page down / up |
| `gg` | jump to top |
| `G` | jump to bottom |
| `g` | toggle ninja mode (a single `g` never triggers `gg`) |

## Using it

- Click the **N** toolbar button, or press `g` from off, to enable ninja
  mode.
- Scroll with `j`/`k`, jump with `gg`/`G`, half-page with `d`/`u`.
- Press `g` again to turn it off.
- The status bar reports the mode and your scroll position.

## Hooks used

- `on_keypress` — the keys
- `buttons` / `on_click` — the N toolbar button

## Settings

| Key | Default | Meaning |
|-----|---------|---------|
| `enabled` | `false` | Whether ninja mode is on |

## Uninstall

Any time from the ToeHub: open `toe://hub`, find keyboard-ninja, and click
**uninstall**.
