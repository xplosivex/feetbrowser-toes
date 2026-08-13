"""reader toe: extract the article text and render it clean.

`on_load` rewrites the raw HTML: it strips script/style/nav/footer, keeps
headings and paragraphs, and re-emits them inside a single clean document
that FeetBrowser renders with its own layout engine. `extra_css` gives the
result a serif, comfortable reading page.

Toggle on/off with the "R" toolbar button; the current page reloads so the
change takes effect immediately.
"""

import html as _html
import re

from feetbrowser import toes

READER_CSS = """
body { font-family: Georgia, serif; max-width: 700px; margin: 40px auto;
       color: #222; line-height: 1.6; }
h1 { font-size: 28px; }
h2 { font-size: 22px; }
a { color: #1a73e8; }
"""


def activate(ctx):
    # Seed the module flag from persisted settings so on_load sees it.
    _READER["on"] = bool(ctx.settings.get("reader_on", False))
    ctx.on("buttons", lambda: [toes.ButtonDef("reader", "R", "Reader")])
    ctx.on("on_click", lambda btn_id: _toggle(ctx, btn_id))
    ctx.on("on_load", on_load)
    ctx.on("extra_css", extra_css)


def _toggle(ctx, btn_id):
    if btn_id != "reader":
        return
    _READER["on"] = not _READER["on"]
    ctx.settings["reader_on"] = _READER["on"]
    ctx.save_settings()
    ctx.set_status("Reader mode is ON. Clutter, begone!"
                   if _READER["on"] else "Reader mode is OFF.")
    tab = ctx.current_tab()
    if tab and tab.url and not str(tab.url).startswith("toe://"):
        tab.load(tab.url, push=False)


def on_load(url, body):
    if not _READER["on"]:
        return None
    return _extract(body)


_READER = {"on": False}


def extra_css(url):
    return READER_CSS


def _extract(body):
    body = re.sub(
        r"<(script|style|nav|header|footer|aside|form|iframe)[^>]*>.*?</\1>",
        "", body, flags=re.DOTALL | re.IGNORECASE)
    keep = re.findall(r"<(h[1-6]|p|li|blockquote)[^>]*>(.*?)</\1>",
                      body, flags=re.DOTALL | re.IGNORECASE)
    parts = []
    for tag, inner in keep:
        text = re.sub(r"<[^>]+>", "", inner)
        text = _html.unescape(text).strip()
        if not text:
            continue
        parts.append(f"<{tag}>{_html.escape(text)}</{tag}>")
    title = re.search(r"<title[^>]*>(.*?)</title>", body,
                      re.DOTALL | re.IGNORECASE)
    title_text = _html.unescape(title.group(1)).strip() if title else "Reader"
    if not parts:
        return body
    return ("<!doctype html><html><head><title>" + title_text +
            "</title></head><body><h1>" + title_text + "</h1>" +
            "".join(parts) + "</body></html>")
