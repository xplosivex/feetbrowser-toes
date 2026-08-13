"""dark-mode toe: a dark theme for every page.

Injects an author stylesheet that flips the page to dark. The cascade
engine applies it after the UA sheet and before page styles, so author
rules still win when they set explicit colors — but most pages inherit
enough to go dark. Pure `extra_css`, no DOM rewriting.
"""

DARK_CSS = """
html { background: #1e1e1e !important; }
body, div, article, section, nav, header, footer, main, aside, p, ul, ol,
li, table, tr, td, th, form, blockquote, pre, figure, hr {
  background-color: #1e1e1e !important;
  color: #d0d0d0 !important;
}
h1, h2, h3, h4, h5, h6 { color: #f0f0f0 !important; }
a { color: #7aa2f7 !important; }
code, pre, kbd, samp, tt { background-color: #161616 !important; color: #9ece6a !important; }
hr { border-color: #444 !important; }
"""


def activate(ctx):
    ctx.on("extra_css", extra_css)


def extra_css(url):
    return DARK_CSS
