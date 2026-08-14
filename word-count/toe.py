"""word-count toe: prove the on_load and extra_css hooks.

After every navigation this toe parses the raw HTML, counts the words in
*visible* text (skipping <script>/<style> blocks so code doesn't inflate
the count), and injects a small status line with an estimated reading time
before the browser ever parses it. A bit of injected CSS keeps the status
line looking like it belongs.

Toggle on/off with the "W" toolbar button; the toggle persists and the
current page reloads so the change takes effect immediately.
"""

import re

from feetbrowser import toes

# Rough reading speed, words per minute.
_WPM = 200.0


def activate(ctx):
    ctx.settings.setdefault("enabled", True)
    _ENABLED[0] = bool(ctx.settings["enabled"])
    ctx.save_settings()
    ctx.on("buttons", lambda: [toes.ButtonDef("wordcount", "W", "Word Count")])
    ctx.on("on_click", lambda btn_id: _toggle(ctx, btn_id))
    ctx.on("on_load", on_load)
    ctx.on("extra_css", extra_css)


def _toggle(ctx, btn_id):
    if btn_id != "wordcount":
        return
    ctx.settings["enabled"] = not ctx.settings.get("enabled", True)
    _ENABLED[0] = bool(ctx.settings["enabled"])
    ctx.save_settings()
    ctx.set_status("Word count is ON." if ctx.settings["enabled"]
                   else "Word count is OFF.")
    tab = ctx.current_tab()
    if tab and tab.url and not str(tab.url).startswith(("toe://", "toehub://")):
        tab.load(tab.url, push=False)


def on_load(url, body):
    if not ctx_settings_enabled():
        return None
    text = _strip_tags_and_scripts(body)
    words = re.findall(r"[A-Za-z0-9]+", text)
    if not words:
        return None
    n = len(words)
    minutes = n / _WPM
    if minutes < 1:
        time_label = "under a minute"
    else:
        time_label = f"about {round(minutes)} min"
    line = (f'<div class="toe-word-count">'
            f'Toes counted {n} words on this page ({time_label} to read).</div>')
    return body.replace("</body>", line + "</body>", 1)


# Module-level flag mirrored from settings so on_load (which gets no ctx)
# can see the toggle.
_ENABLED = [True]


def ctx_settings_enabled():
    return _ENABLED[0]


def extra_css(url):
    return """
.toe-word-count {
  margin: 14px 8px;
  padding: 6px 10px;
  border: 1px dashed #888;
  color: #666;
  font-size: 13px;
  font-style: italic;
}
"""


def _strip_tags_and_scripts(body):
    # Drop script/style contents entirely, then tags, then decode entities.
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", "",
                  body, flags=re.DOTALL | re.IGNORECASE)
    body = re.sub(r"<[^>]+>", " ", body)
    import html as _html
    return _html.unescape(body)
