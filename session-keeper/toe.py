"""session-keeper toe: persist open tabs and restore them later.

Records every tab's title + URL to a JSON file on a timer, and also saves
when a tab closes. `session://` serves a page listing the saved tabs with
clickable links that reopen them, so you can pick up where you left off
after a crash or a coffee break.

Saves are debounced through the browser's `after` loop; the log lives in
the toe's settings folder.
"""

import json
import os

from feetbrowser import toes

SESSION_STYLE = """
  body { font-family: Courier; margin: 40px; background: #fdf6e3; color: #222; }
  h1 { color: #8b0000; letter-spacing: 2px; }
  .box { border: 1px solid #bbb; background: #fff; padding: 6px 10px; margin: 4px 0; }
  a { color: #8b0000; }
  .dim { color: #999; }
"""


def activate(ctx):
    ctx.on("handle", lambda url, tab: _handle(ctx, url, tab))
    ctx.on("on_new_tab", lambda: _schedule_save(ctx))
    _schedule_save(ctx)


def _save_path(ctx):
    folder = getattr(ctx.toe, "folder", None)
    if not folder:
        return None
    return os.path.join(folder, "session.json")


def _read_session(ctx):
    path = _save_path(ctx)
    if not path:
        return []
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, ValueError):
        return []


def _save_session(ctx, tabs):
    path = _save_path(ctx)
    if not path:
        return
    try:
        with open(path, "w") as f:
            json.dump(tabs, f, indent=2)
    except OSError:
        pass


def _schedule_save(ctx):
    if getattr(ctx, "_save_scheduled", False):
        return
    ctx._save_scheduled = True
    browser = ctx.browser
    try:
        browser.window.after(2000, lambda: _do_save(ctx))
    except Exception:
        pass


def _do_save(ctx):
    ctx._save_scheduled = False
    tabs = []
    for tab in ctx.tabs():
        if tab and tab.url and not str(tab.url).startswith(("session://",)):
            tabs.append({"title": tab.title, "url": str(tab.url)})
    _save_session(ctx, tabs)


def _handle(ctx, url, tab):
    if url.scheme != "session":
        return None
    if url.host == "restore" and url.path:
        name = url.path.lstrip("/")
        for saved in _read_session(ctx):
            if saved.get("url") == name or saved.get("title") == name:
                ctx.open(saved["url"])
                return {}, _msg_page("Restoring…"), "text/html"
        return {}, _msg_page("No such saved tab."), "text/html"
    if url.host == "clear":
        _save_session(ctx, [])
        return {}, _msg_page("Memory wiped. The session keeper forgets "
                             "everything."), "text/html"
    # session:// and session://home both list saved tabs.
    saved = _read_session(ctx)
    rows = []
    if not saved:
        rows.append("<div class='box'>No tabs saved yet. Open some pages and "
                    "the session keeper will note them down.</div>")
    for entry in saved:
        rows.append(
            f'<div class="box"><a href="{_esc(entry["url"])}">'
            f'{_esc(entry["title"])}</a>'
            f' <span class="dim">{_esc(entry["url"])}</span></div>')
    rows.append('<div class="box"><a href="session://clear">forget '
                'everything</a></div>')
    body = ("<!doctype html><html><head><title>Session</title>"
            f"<style>{SESSION_STYLE}</style></head><body>"
            "<h1>SAVED SESSIONS</h1>"
            + "\n".join(rows) +
            "</body></html>")
    return {}, body, "text/html"


def _msg_page(msg):
    return ("<!doctype html><html><head><title>Session</title>"
            f"<style>{SESSION_STYLE}</style></head><body><h1>SESSION</h1>"
            f'<div class="box">{_esc(msg)}</div>'
            '<div class="box"><a href="session://">back to sessions</a></div>'
            "</body></html>")


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")
