# toe-bar

A wide, cluttered, early-2000s toolbar drawn as a chrome band above the
tabs: scrolling marquee, rotating banner ads, a hit counter, a web ring,
and popup windows. Best viewed in 800x600.

## What it does

A 30px chrome band across the top of the browser:

- **TOE BAR** button — toggles the whole band on/off
- **Marquee** — scrolling green-on-black ticker
- **Banner ads** — rotate every few seconds; clicking spawns a **real
  popup window** (not a redirect)
- **Hit counter** — `YOU ARE VISITOR #000042`, increments per navigation
- **Web ring** — `← PREV | TOE RING | NEXT →`, cycles through the other
  toes' pages

Popups are separate Tk windows with their own canvas, title bar, and
scrollbar. Ads have **CLOSE** and **MORE FREE TOES** (the classic popup
chain). **"You've got toes!"** pops up on startup and every 10 navigations.

## Using it

- Click **TOE BAR** to show/hide the band.
- Click a banner ad to spawn a popup.
- Click the web ring to hop between toe pages.

## Settings page

`toe://toebar` — bar on/off, popup blocker, visitor counter (and reset),
the ads, and the ring.

## Hooks used

- `chrome_bands` / `on_chrome_draw` / `on_chrome_click` — the band
- `buttons` / `on_click` — the TB toolbar button
- `handle` — the settings + ad pages
- `on_new_tab` — the periodic popup
- `ctx.popup` — the adware

## Uninstall

Any time from the ToeHub: open `toe://hub`, find toe-bar, and click
**uninstall**.
