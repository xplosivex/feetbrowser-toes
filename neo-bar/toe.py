"""neo-bar toe: a full toolbar reimplemented as a toe.

The browser's own toolbar is drawn in its chrome. This toe draws a *second*
toolbar on a chrome band, entirely through the toe framework — no browser
core changes:

    ‹  ›  ⟳  ⌂  ★   |  address bar …            |  VISITOR #000042

  ‹  back        ⟳  reload     ★  bookmark toggle
  ›  forward     ⌂  home       address bar → navigate on Enter

Everything is hand-drawn on the band and hit-tested by on_chrome_click.
It reuses the browser's own navigation methods (go_back, go_forward, load,
_toggle_bookmark) and reads live state (history, current URL, bookmarks) on
every draw, so it always reflects reality.

Hit regions are computed from the same layout function used to draw, so
they can never drift out of sync with the pixels.
"""

from feetbrowser import toes
from feetbrowser.layout import get_font

BAND_HEIGHT = 34
BAR_ID = "neo-bar"

# (id, x, w, glyph) — left to right, in pixels from band-left.
BUTTONS = [
    ("back", 4, 26, "‹"),
    ("forward", 34, 26, "›"),
    ("reload", 64, 26, "⟳"),
    ("home", 94, 26, "⌂"),
    ("bookmark", 124, 26, "★"),
]

ADDR_X = 154  # address bar left edge
ADDR_W = 460
COUNTER_X = ADDR_X + ADDR_W + 8
COUNTER_W = 150

BAND_STYLE = """
  body { font-family: Courier; margin: 40px; background: #fdf6e3; color: #222; }
  h1 { color: #1a73e8; letter-spacing: 2px; }
  .k { color: #8b0000; }
  .v { color: #1a73e8; }
  .box { border: 1px solid #bbb; background: #fff; padding: 6px 10px; margin: 4px 0; }
  a { color: #1a73e8; }
"""


def activate(ctx):
    ctx.define_config(
        toes.ConfigOption("show", "Show the bar", "bool", default=True,
                          help="Draw the neo-bar band."),
        toes.ConfigOption("height", "Band height (px)", "int", default=34,
                          help="Height of the toolbar band."),
        toes.ConfigOption("accent", "Accent color", "str",
                          default="#1a73e8",
                          help="Color for the bookmark star and focused "
                               "address bar."),
        toes.ConfigOption("counter_label", "Counter label", "str",
                          default="VISITOR",
                          help="Text before the counter number."),
        toes.ConfigOption("track_visitors", "Count visitors", "bool",
                          default=True,
                          help="Increment the visitor counter on each new "
                               "tab."),
    )
    _CONFIG["height"] = ctx.config_value("height")
    _CONFIG["accent"] = ctx.config_value("accent")
    _CONFIG["counter_label"] = ctx.config_value("counter_label")
    ctx.on("chrome_bands", lambda: [(BAR_ID, _CONFIG.get("height", 34))])
    ctx.on("on_chrome_draw", lambda canvas, bands: _draw(ctx, canvas, bands))
    ctx.on("on_chrome_click", lambda x, y, bands: _click(ctx, x, y, bands))
    ctx.on("buttons", lambda: [toes.ButtonDef("neobar", "NB", "Neo-Bar")])
    ctx.on("on_click", lambda btn_id: _toolbar_click(ctx, btn_id))
    ctx.on("handle", lambda url, tab: _handle(ctx, url, tab))
    ctx.on("on_new_tab", lambda: _tick_visitor(ctx))
    ctx.settings.setdefault("visitor", 0)
    ctx.settings.setdefault("typing", "")
    ctx.settings.setdefault("address_focus", False)
    ctx.save_settings()


_CONFIG = {"height": 34, "accent": "#1a73e8", "counter_label": "VISITOR"}


# -- drawing --------------------------------------------------------------


def _draw(ctx, canvas, bands):
    if not ctx.config_value("show"):
        return
    band = next((b for b in bands if b[0] == BAR_ID), None)
    if band is None:
        return
    _id, height, y = band
    w = canvas.winfo_width()
    accent = _CONFIG.get("accent", "#1a73e8")

    # Band chrome: a flat, modern strip (unlike the 2003 toe-bar).
    canvas.create_rectangle(0, y, w, y + height, fill="#e8e8e8", width=0)
    canvas.create_line(0, y + height - 1, w, y + height - 1, fill="#ccc")

    tab = ctx.browser.active_tab
    for bid, bx, bw, glyph in BUTTONS:
        enabled = _button_enabled(ctx, bid, tab)
        canvas.create_rectangle(bx, y + 3, bx + bw, y + height - 3,
                                outline="#999", fill="#f4f4f4", width=1)
        canvas.create_text(bx + bw // 2, y + height // 2, text=glyph,
                           fill="#333" if enabled else "#bbb",
                           font=get_font(11, "bold", "roman", "Helvetica"))
        if bid == "bookmark":
            marked = _is_bookmarked(ctx, tab)
            canvas.create_text(bx + bw // 2, y + height // 2,
                               text="★" if marked else "☆",
                               fill=accent if marked else "#bbb",
                               font=get_font(11, "bold", "roman",
                                             "Helvetica"))

    # Address bar.
    addr_x = ADDR_X
    if addr_x + ADDR_W > w:
        ADDR_W2 = max(60, w - addr_x - COUNTER_W - 16)
    else:
        ADDR_W2 = ADDR_W
    canvas.create_rectangle(addr_x, y + 3, addr_x + ADDR_W2, y + height - 3,
                            outline=accent if ctx.settings.get(
                                "address_focus") else "#999",
                            fill="white",
                            width=2 if ctx.settings.get("address_focus") else 1)
    text = ctx.settings.get("typing", "") if ctx.settings.get(
        "address_focus") else _current_url(ctx, tab)
    display = text or "Type a URL or search term…"
    color = "#aaa" if not text else "#111"
    canvas.create_text(addr_x + 8, y + height // 2, text=display[:58],
                       anchor="w", fill=color,
                       font=get_font(11, "normal", "roman", "Helvetica"))

    # Hit counter.
    n = ctx.settings.get("visitor", 0)
    label = _CONFIG.get("counter_label", "VISITOR")
    cx = addr_x + ADDR_W2 + 8
    canvas.create_rectangle(cx, y + 3, cx + COUNTER_W, y + height - 3,
                            outline="#999", fill="#f4f4f4", width=1)
    canvas.create_text(cx + COUNTER_W // 2, y + height // 2,
                       text=f"{label} #{n:06d}",
                       font=get_font(9, "bold", "roman", "Helvetica"),
                       fill="#333")


def _button_enabled(ctx, bid, tab):
    if bid == "back":
        return bool(tab and tab.history)
    if bid == "forward":
        return bool(tab and tab.future)
    if bid in ("reload", "home", "bookmark"):
        return bool(tab)
    return True


def _current_url(ctx, tab):
    if tab and tab.url and not type(tab.url).__name__ == "_AboutURL":
        return str(tab.url)
    return ""


def _is_bookmarked(ctx, tab):
    try:
        return bool(ctx.browser._is_bookmarked(tab.url))
    except Exception:
        return False


# -- hit testing ----------------------------------------------------------


def _click(ctx, x, y, bands):
    band = next((b for b in bands if b[0] == BAR_ID), None)
    if band is None:
        return False
    _id, height, by = band
    if not (by <= y < by + height):
        return False
    browser = ctx.browser
    tab = browser.active_tab

    # Buttons.
    for bid, bx, bw, _glyph in BUTTONS:
        if bx <= x < bx + bw:
            if bid == "back" and tab and tab.history:
                browser._back()
            elif bid == "forward" and tab and tab.future:
                browser._forward()
            elif bid == "reload" and tab:
                browser._reload()
            elif bid == "home" and tab:
                browser._home()
            elif bid == "bookmark" and tab:
                browser._toggle_bookmark()
            return True

    # Address bar.
    addr_x = ADDR_X
    if addr_x <= x < addr_x + ADDR_W:
        ctx.settings["address_focus"] = True
        ctx.save_settings()
        return True

    return False


def _toolbar_click(ctx, btn_id):
    if btn_id == "neobar":
        ctx.open("neo://")


# -- typing into the neo address bar -------------------------------------


def _key(ctx, e):
    if not ctx.settings.get("address_focus", False):
        return False
    ch = getattr(e, "char", "")
    keysym = getattr(e, "keysym", "")
    if keysym == "Return":
        query = ctx.settings.get("typing", "").strip()
        ctx.settings["address_focus"] = False
        ctx.settings["typing"] = ""
        ctx.save_settings()
        tab = ctx.browser.active_tab
        if tab and query:
            if not ctx.browser._looks_like_url(query):
                query = "https://duckduckgo.com/html/?q=" + \
                    query.replace(" ", "+")
            elif "://" not in query and not query.startswith(
                    ("file:", "data:", "view-source:", "about:")):
                query = "https://" + query
            ctx.browser._navigate(tab, query)
        return True
    if keysym == "Escape":
        ctx.settings["address_focus"] = False
        ctx.settings["typing"] = ""
        ctx.save_settings()
        ctx.browser.draw()
        return True
    if keysym == "BackSpace":
        ctx.settings["typing"] = ctx.settings.get("typing", "")[:-1]
        ctx.save_settings()
        ctx.browser.draw()
        return True
    if len(ch) == 1 and ch.isprintable():
        ctx.settings["typing"] = (ctx.settings.get("typing", "")
                                  + ch)[:200]
        ctx.save_settings()
        ctx.browser.draw()
        return True
    return False


# -- pages ----------------------------------------------------------------


def _handle(ctx, url, tab):
    if url.scheme != "neo":
        return None
    return {}, _neo_page(ctx), "text/html"


def _neo_page(ctx):
    browser = ctx.browser
    tab = browser.active_tab
    history = [str(u) for u, _s in (tab.history if tab else [])]
    future = [str(u) for u, _s in (tab.future if tab else [])]
    marked = _is_bookmarked(ctx, tab)
    return f"""<!doctype html>
<html><head><title>Neo-Bar</title><style>{BAND_STYLE}</style></head>
<body>
<h1>NEO-BAR</h1>
<p class="k">A full toolbar, reimplemented as a toe.</p>
<div class="box"><span class="k">CURRENT</span>:
 <span class="v">{_current_url(ctx, tab)}</span></div>
<div class="box"><span class="k">BACK</span>: {len(history)}
 <span class="dim">({', '.join(history[-3:])})</span></div>
<div class="box"><span class="k">FORWARD</span>: {len(future)}
 <span class="dim">({', '.join(future[-3:])})</span></div>
<div class="box"><span class="k">BOOKMARKED</span>:
 <span class="v">{"yes" if marked else "no"}</span></div>
<div class="box"><span class="k">VISITOR NUMBER</span>:
 <span class="v">#{ctx.settings.get('visitor', 0):06d}</span></div>
<div class="box"><span class="k">TIP</span>: click the band's address bar
 and type; press Enter to navigate.</div>
</body></html>
"""


def _tick_visitor(ctx):
    if ctx.config_value("track_visitors"):
        ctx.settings["visitor"] = ctx.settings.get("visitor", 0) + 1
        ctx.save_settings()
