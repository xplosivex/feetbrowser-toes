# toe-scheme

Registers a custom `echo://` URL scheme that the browser renders through its
normal pipeline.

## What it does

The framework reserves the `toe://` hosts (`hub`, `gallery`, `hello`), so
this toe demonstrates custom schemes with its own namespace:

- `echo://hello` — a greeting page
- `echo://<anything>` — echoes back whatever you typed
- `echo://links` — shows how custom-scheme links behave (clickable, history
  aware, view-source-able)

## Using it

Type `echo://hello` (or anything else) into the address bar and press Enter.
Pages flow through the normal HTML/CSS/layout pipeline, so links work,
`view-source:echo://hello` shows the source, and history behaves normally.

## Hooks used

- `handle` — intercept `echo://` before fetching

## Uninstall

Any time from the ToeHub: open `toe://hub`, find toe-scheme, and click
**uninstall**.
