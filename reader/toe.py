"""reader toe: extract the article text and render it clean.

`on_load` rewrites the raw HTML: it strips script/style/nav/footer/aside
and re-emits the article's headings, paragraphs, lists, blockquotes, links,
and images inside a single clean document that FeetBrowser renders with its
own layout engine. Links and image srcs are preserved (rewritten to
absolute when possible), so reading still lets you click through.
`extra_css` gives the result a serif, comfortable reading page.

Toggle on/off with the "R" toolbar button; the current page reloads so the
change takes effect immediately.
"""

import html as _html
import re
from urllib.parse import urljoin

from feetbrowser import toes

READER_CSS = """
body { font-family: Georgia, serif; max-width: 700px; margin: 40px auto;
       color: #222; line-height: 1.6; }
h1 { font-size: 28px; }
h2 { font-size: 22px; }
h3 { font-size: 18px; }
img { max-width: 100%; }
a { color: #1a73e8; }
blockquote { border-left: 3px solid #ccc; margin-left: 0; padding-left: 16px; }
"""

# Tags we keep, with a handler. Everything else's content is dropped.
_KEEP_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "blockquote",
              "a", "img", "ul", "ol", "br", "em", "strong", "b", "i", "code"}


def activate(ctx):
    ctx.settings.setdefault("enabled", True)
    _ENABLED[0] = bool(ctx.settings["enabled"])
    ctx.save_settings()
    ctx.on("buttons", lambda: [toes.ButtonDef("reader", "R", "Reader")])
    ctx.on("on_click", lambda btn_id: _toggle(ctx, btn_id))
    ctx.on("on_load", on_load)
    ctx.on("extra_css", extra_css)


_ENABLED = [True]


def _toggle(ctx, btn_id):
    if btn_id != "reader":
        return
    ctx.settings["enabled"] = not ctx.settings.get("enabled", True)
    _ENABLED[0] = bool(ctx.settings["enabled"])
    ctx.save_settings()
    ctx.set_status("Reader mode is ON. Clutter, begone!"
                   if _ENABLED[0] else "Reader mode is OFF.")
    tab = ctx.current_tab()
    if tab and tab.url and not str(tab.url).startswith(("toe://", "toehub://")):
        tab.load(tab.url, push=False)


def on_load(url, body):
    if not _ENABLED[0]:
        return None
    base = str(url)
    return _extract(body, base)


def extra_css(url):
    return READER_CSS


def _extract(body, base=""):
    # Strip script/style/nav/footer/aside/form/iframe entirely.
    body = re.sub(
        r"<(script|style|nav|header|footer|aside|form|iframe|svg|canvas)[^>]*>.*?</\1>",
        "", body, flags=re.DOTALL | re.IGNORECASE)

    # Pull the title.
    m = re.search(r"<title[^>]*>(.*?)</title>", body,
                  re.DOTALL | re.IGNORECASE)
    title_text = _html.unescape(m.group(1)).strip() if m else "Reader"

    # Walk the DOM textually: keep allowed tags and their text, drop the rest.
    cleaned = _clean_tags(body, base)

    # Find the "article": the <p>/<h*>/<li> runs, as a plain concatenation.
    keep = re.findall(r"<(h[1-6]|p|li|blockquote)[^>]*>"
                      r"(.*?)</\1>",
                      cleaned, flags=re.DOTALL | re.IGNORECASE)
    parts = []
    for tag, inner in keep:
        inner = inner.strip()
        if not inner:
            continue
        parts.append(f"<{tag}>{inner}</{tag}>")
    if not parts:
        return body  # Nothing article-like; leave the page alone.

    # Deduplicate: the regex above already consumed inner tags, so re-joining
    # with the block tags is fine. Wrap in a clean document.
    return ("<!doctype html><html><head><title>" + _html.escape(title_text) +
            "</title></head><body><h1>" + _html.escape(title_text) + "</h1>"
            + "".join(parts) + "</body></html>")


def _clean_tags(body, base):
    """Return `body` with only _KEEP_TAGS retained; everything else's content
    is kept as text but its tags are dropped. Links/images keep attributes."""
    # Replace disallowed open tags with nothing but keep their text.
    # Allowed tags are walked separately for their attributes.
    out = []
    i = 0
    n = len(body)
    while i < n:
        if body[i] == "<":
            end = body.find(">", i)
            if end == -1:
                out.append(_html.escape(body[i:]))
                break
            raw_tag = body[i + 1:end].strip()
            m = re.match(r"^/?([A-Za-z0-9]+)", raw_tag)
            if not m:
                out.append(_html.escape(body[i]))
                i += 1
                continue
            tag = m.group(1).lower()
            if tag in ("a", "img"):
                # Preserve with attributes.
                attrs = _attrs(raw_tag, base)
                if tag == "a" and "href" in attrs:
                    out.append(f'<a href="{attrs["href"]}">')
                elif tag == "img" and "src" in attrs:
                    out.append(f'<img src="{attrs["src"]}" '
                               f'alt="{attrs.get("alt", "")}">')
                else:
                    pass  # drop link/img without usable attr
            elif tag in _KEEP_TAGS:
                out.append(f"<{tag}>")
            elif tag.startswith("/") is False:
                pass  # drop disallowed tag, keep text
            i = end + 1
        else:
            out.append(body[i])
            i += 1
    return "".join(out)


def _attrs(raw_tag, base):
    """Parse attributes out of a raw tag; absolutize href/src against base."""
    attrs = {}
    for m in re.finditer(r'([A-Za-z_:][-A-Za-z0-9_:.]*)\s*=\s*'
                         r'(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+))', raw_tag):
        name = m.group(1).lower()
        val = m.group(2) or m.group(3) or m.group(4) or ""
        if name in ("href", "src") and base:
            val = urljoin(base, val)
        attrs[name] = _html.escape(val)
    return attrs
