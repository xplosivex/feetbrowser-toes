"""dark-mode toe: a dark theme for every page.

Injects an author stylesheet that flips the page to dark. The cascade
engine applies it after the UA sheet and before page styles, so author
rules still win when they set explicit colors — but most pages inherit
enough to go dark. Pure `extra_css`, no DOM rewriting.

Toggle on/off with the "D" toolbar button; the toggle persists and the
current page reloads so the change takes effect immediately.
"""

from feetbrowser import toes

DARK_CSS = """
html { background: #1e1e1e !important; }
body, div, article, section, nav, header, footer, main, aside, p, ul, ol,
li, dl, dt, dd, table, tr, td, th, thead, tbody, tfoot, caption, form,
blockquote, pre, figure, figcaption, address, hr, details, summary {
  background-color: #1e1e1e !important;
  color: #d0d0d0 !important;
}
h1, h2, h3, h4, h5, h6 { color: #f0f0f0 !important; }
a { color: #7aa2f7 !important; }
a:visited { color: #b48ead !important; }
code, pre, kbd, samp, tt { background-color: #161616 !important; color: #9ece6a !important; }
em, strong, b, i { color: inherit !important; }
blockquote, figure { border-left: 3px solid #444 !important; }
hr { border-color: #444 !important; }
input, textarea, select, button {
  background-color: #2a2a2a !important;
  color: #d0d0d0 !important;
  border-color: #444 !important;
}
img { opacity: 0.85 !important; }
"""


def activate(ctx):
    ctx.settings.setdefault("enabled", True)
    _ENABLED[0] = bool(ctx.settings["enabled"])
    ctx.save_settings()
    ctx.on("buttons", lambda: [toes.ButtonDef("darkmode", "D", "Dark Mode")])
    ctx.on("on_click", lambda btn_id: _toggle(ctx, btn_id))
    ctx.on("extra_css", extra_css)


_ENABLED = [True]


def _toggle(ctx, btn_id):
    if btn_id != "darkmode":
        return
    ctx.settings["enabled"] = not ctx.settings.get("enabled", True)
    _ENABLED[0] = bool(ctx.settings["enabled"])
    ctx.save_settings()
    ctx.set_status("Dark mode is ON." if _ENABLED[0]
                   else "Dark mode is OFF. The light returns.")
    tab = ctx.current_tab()
    if tab and tab.url and not str(tab.url).startswith(("toe://", "toehub://")):
        tab.load(tab.url, push=False)


def extra_css(url):
    if not _ENABLED[0]:
        return None
    return DARK_CSS
