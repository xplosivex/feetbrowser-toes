# reader

Strips a page down to its article text, keeping links and images. Reading,
without the clutter.

## What it does

`on_load` rewrites the raw HTML: it strips `script`, `style`, `nav`,
`header`, `footer`, `aside`, `form`, and `iframe` content, keeps the
article's headings, paragraphs, lists, blockquotes, links, and images, and
re-emits them in a clean document that FeetBrowser renders with its own
layout engine. Link and image `src`s are preserved (absolutized when
possible), so reading still lets you click through.

## Using it

- **Toggle**: click the **R** toolbar button to turn reader mode on/off. The
  current page reloads so the change takes effect immediately.
- **Default**: OFF. When on, pages without anything article-like are left
  untouched.

## Hooks used

- `on_load` — extract and re-emit the article
- `extra_css` — the serif reading style
- `buttons` / `on_click` — the R toolbar button

## Settings

| Key | Default | Meaning |
|-----|---------|---------|
| `enabled` | `false` | Whether reader mode applies |

## Uninstall

Any time from the ToeHub: open `toe://hub`, find reader, and click
**uninstall**.
