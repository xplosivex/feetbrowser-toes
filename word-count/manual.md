# word-count

Counts the words on every page (skipping `<script>` and `<style>` contents)
and injects a small status line with an estimated reading time.

## What it does

- After each navigation, counts visible words in the page.
- Injects a line before `</body>`:
  `Toes counted N words on this page (about X min to read).`
- Styled by an injected stylesheet (`toe-word-count`).

## Using it

- **Toggle**: click the **W** toolbar button to turn the word count on/off.
  The current page reloads so the change takes effect immediately.
- **Default**: ON.

## Hooks used

- `on_load` — rewrite the body to add the status line
- `extra_css` — style the status line
- `buttons` / `on_click` — the W toolbar button

## Settings

| Key | Default | Meaning |
|-----|---------|---------|
| `enabled` | `true` | Whether the word count runs |

## Uninstall

Any time from the ToeHub: open `toe://hub`, find word-count, and click
**uninstall**.
