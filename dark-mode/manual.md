# dark-mode

A dark theme for every page. Injects a stylesheet that flips the page to
dark.

## What it does

Injects an author stylesheet (after the UA sheet, before page styles) that:

- paints backgrounds dark (`#1e1e1e`)
- lightens text (`#d0d0d0`), headings (`#f0f0f0`), and links (`#7aa2f7`)
- styles code/pre blocks, blockquotes, and `hr`
- dims images slightly (85% opacity)
- darkens form controls

Author rules still win when a page sets explicit colors, so pages that
style themselves heavily may not go fully dark — but most inherit enough.

## Using it

- **Toggle**: click the **D** toolbar button to turn dark mode on/off. The
  current page reloads so the change takes effect immediately.
- **Default**: ON.

## Hooks used

- `extra_css` — the injected stylesheet
- `buttons` / `on_click` — the D toolbar button

## Settings

| Key | Default | Meaning |
|-----|---------|---------|
| `enabled` | `true` | Whether dark mode applies |

## Uninstall

Any time from the ToeHub: open `toe://hub`, find dark-mode, and click
**uninstall**.
