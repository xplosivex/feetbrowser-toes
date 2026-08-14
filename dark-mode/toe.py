"""dark-mode toe: a dark theme for every page.

Injects an author stylesheet that flips the page to dark. The cascade
engine applies it after the UA sheet and before page styles, so author
rules still win when they set explicit colors — but most pages inherit
enough to go dark. Pure `extra_css`, no DOM rewriting.

Toggle on/off with the "D" toolbar button; the toggle persists and the
current page reloads so the change takes effect immediately.
"""

from feetbrowser import toes


def activate(ctx):
    ctx.define_config(
        toes.ConfigOption("enabled", "Dark mode", "bool", default=True,
                          help="Apply the dark theme to every page."),
        toes.ConfigOption("background", "Background color", "str",
                          default="#1e1e1e",
                          help="Hex color used for page backgrounds."),
        toes.ConfigOption("accent", "Accent color", "choice",
                          default="#7aa2f7",
                          options=[("#7aa2f7", "blue"),
                                   ("#9ece6a", "green"),
                                   ("#f7768e", "red"),
                                   ("#e0af68", "amber")],
                          help="Link/accent color."),
        toes.ConfigOption("dim_images", "Dim images", "bool", default=True,
                          help="Render images at 85% opacity."),
    )
    _sync_config(ctx)
    _ENABLED[0] = bool(_CONFIG.get("enabled", True))
    ctx.on("buttons", lambda: [toes.ButtonDef("darkmode", "D", "Dark Mode")])
    ctx.on("on_click", lambda btn_id: _toggle(ctx, btn_id))
    ctx.on("extra_css", extra_css)


_ENABLED = [True]


def _sync_config(ctx):
    """Copy declared config values to the module-level _CONFIG mirror so
    extra_css (which gets no ctx) can read them."""
    for key, opt in ctx.config_options():
        _CONFIG[key] = ctx.config_value(key)


def _toggle(ctx, btn_id):
    if btn_id != "darkmode":
        return
    _ENABLED[0] = not _CONFIG.get("enabled", True)
    ctx.set_config("enabled", _ENABLED[0])
    _sync_config(ctx)
    ctx.set_status("Dark mode is ON." if _ENABLED[0]
                   else "Dark mode is OFF. The light returns.")
    tab = ctx.current_tab()
    if tab and tab.url and not str(tab.url).startswith(("toe://", "toehub://")):
        tab.load(tab.url, push=False)


def extra_css(url):
    if not _ENABLED[0]:
        return None
    bg = _CONFIG.get("background", "#1e1e1e")
    accent = _CONFIG.get("accent", "#7aa2f7")
    img = "img { opacity: 0.85 !important; }" if _CONFIG.get(
        "dim_images", True) else ""
    return (DARK_CSS_TEMPLATE.replace("__BG__", bg)
            .replace("__ACCENT__", accent)
            .replace("__IMG__", img))


DARK_CSS_TEMPLATE = """
html { background: __BG__ !important; }
body, div, article, section, nav, header, footer, main, aside, p, ul, ol,
li, dl, dt, dd, table, tr, td, th, thead, tbody, tfoot, caption, form,
blockquote, pre, figure, figcaption, address, hr, details, summary {
  background-color: __BG__ !important;
  color: #d0d0d0 !important;
}
h1, h2, h3, h4, h5, h6 { color: #f0f0f0 !important; }
a { color: __ACCENT__ !important; }
a:visited { color: __ACCENT__ !important; }
code, pre, kbd, samp, tt { background-color: #161616 !important; color: #9ece6a !important; }
em, strong, b, i { color: inherit !important; }
blockquote, figure { border-left: 3px solid #444 !important; }
hr { border-color: #444 !important; }
input, textarea, select, button {
  background-color: #2a2a2a !important;
  color: #d0d0d0 !important;
  border-color: #444 !important;
}
__IMG__
"""


# Mirror of the config values so extra_css (which has no ctx) can read them.
_CONFIG = {}
