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


def activate(ctx):
    ctx.define_config(
        toes.ConfigOption("enabled", "Word count", "bool", default=True,
                          help="Show the word count on every page."),
        toes.ConfigOption("wpm", "Reading speed (wpm)", "int", default=200,
                          help="Words per minute used for the reading-time "
                               "estimate."),
        toes.ConfigOption("show_time", "Show reading time", "bool",
                          default=True,
                          help="Include the estimated reading time."),
    )
    _ENABLED[0] = bool(ctx.config_value("enabled"))
    _CONFIG["wpm"] = ctx.config_value("wpm")
    _CONFIG["show_time"] = ctx.config_value("show_time")
    ctx.on("buttons", lambda: [toes.ButtonDef("wordcount", "W", "Word Count")])
    ctx.on("on_click", lambda btn_id: _toggle(ctx, btn_id))
    ctx.on("on_load", on_load)
    ctx.on("extra_css", extra_css)


def _toggle(ctx, btn_id):
    if btn_id != "wordcount":
        return
    _ENABLED[0] = not ctx.config_value("enabled")
    ctx.set_config("enabled", _ENABLED[0])
    ctx.set_status("Word count is ON." if _ENABLED[0]
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
    minutes = n / max(1, _CONFIG.get("wpm", 200))
    if minutes < 1:
        time_label = "under a minute"
    else:
        time_label = f"about {round(minutes)} min"
    if _CONFIG.get("show_time", True):
        line = (f'<div class="toe-word-count">'
                f'Toes counted {n} words on this page '
                f'({time_label} to read).</div>')
    else:
        line = (f'<div class="toe-word-count">'
                f'Toes counted {n} words on this page.</div>')
    return body.replace("</body>", line + "</body>", 1)


# Module-level flag mirrored from settings so on_load (which gets no ctx)
# can see the toggle.
_ENABLED = [True]
_CONFIG = {"wpm": 200, "show_time": True}


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
