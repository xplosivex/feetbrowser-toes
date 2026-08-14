"""keyboard-ninja toe: vim-style navigation.

`on_keypress` intercepts keys when no address bar and no form field has
focus, turning the keyboard into a scroll controller. Ninja mode is
disabled by default so ordinary typing stays normal; press "g" to toggle
it, or click the "N" toolbar button.

Keys while ninja mode is on:

    j / k       scroll down / up one step
    h / l       scroll down / up a little (half a step)
    d / u       half-page down / up
    gg          jump to top
    G           jump to bottom
    g           toggle ninja mode (a single g never triggers gg)
"""

from feetbrowser import toes

STEP = 80


def activate(ctx):
    ctx.settings.setdefault("enabled", False)
    ctx.save_settings()
    ctx.on("on_keypress", lambda e: _key(ctx, e))
    ctx.on("buttons", lambda: [toes.ButtonDef("ninja", "N", "Ninja")])
    ctx.on("on_click", lambda btn_id: _click(ctx, btn_id))


def _click(ctx, btn_id):
    if btn_id != "ninja":
        return
    _toggle(ctx)


def _toggle(ctx):
    _set_mode(ctx, not ctx.settings.get("enabled", False))


def _set_mode(ctx, on):
    ctx.settings["enabled"] = bool(on)
    ctx.save_settings()
    _status(ctx)


def _key(ctx, e):
    ch = getattr(e, "char", "")
    enabled = ctx.settings.get("enabled", False)

    # "g" always works. From OFF a single g turns ninja mode on right away.
    # From ON, a single g turns it off — but gg (two g's within the window)
    # jumps to the top instead, so the OFF toggle waits briefly to see if a
    # second g arrives.
    if ch == "g":
        tab = ctx.current_tab()
        ctx._g_count = getattr(ctx, "_g_count", 0) + 1
        if ctx._g_count >= 2:
            ctx._g_count = 0
            if tab:
                tab.scroll = 0
                tab._clamp_scroll()
                ctx.browser.draw()
            _status(ctx)
            return True
        if not enabled:
            _g_timeout(ctx, was_on=False, jump_ready=False)
            _set_mode(ctx, True)
            return True
        _g_timeout(ctx, was_on=True, jump_ready=True)
        return True

    if not enabled:
        return False
    ctx._g_count = 0
    tab = ctx.current_tab()
    if not tab:
        return False

    if ch == "G":
        tab.scroll_by(10 ** 9)
        ctx.browser.draw()
        _status(ctx)
        return True
    if ch == "j":
        tab.scroll_by(STEP)
        ctx.browser.draw()
        _status(ctx)
        return True
    if ch == "k":
        tab.scroll_by(-STEP)
        ctx.browser.draw()
        _status(ctx)
        return True
    if ch == "h":
        tab.scroll_by(-STEP // 2)
        ctx.browser.draw()
        return True
    if ch == "l":
        tab.scroll_by(STEP // 2)
        ctx.browser.draw()
        return True
    if ch == "d":
        tab.scroll_by(STEP * 5)
        ctx.browser.draw()
        _status(ctx)
        return True
    if ch == "u":
        tab.scroll_by(-STEP * 5)
        ctx.browser.draw()
        _status(ctx)
        return True
    return False


def _status(ctx):
    tab = ctx.current_tab()
    if tab:
        total = max(1, tab.content_height())
        pct = int(100 * tab.scroll / total)
    else:
        pct = 0
    on = "ON" if ctx.settings.get("enabled", False) else "OFF"
    ctx.set_status(f"Ninja mode {on} · position {pct}%")


def _g_timeout(ctx, was_on, jump_ready):
    """Called after the first g. If a second g arrives we hit the gg branch
    (which clears _g_count). If the window closes with only one g:
      - from OFF: ninja mode was already turned on,
      - from ON (jump_ready): ninja mode turns off.
    """
    browser = ctx.browser
    try:
        browser.window.after(500, lambda: _g_settle(ctx, was_on, jump_ready))
    except Exception:
        pass


def _g_settle(ctx, was_on, jump_ready):
    if ctx._g_count == 1 and not was_on:
        # Single g from OFF: mode was enabled immediately; nothing more.
        pass
    elif ctx._g_count == 1 and jump_ready:
        # Single g from ON: turn it off.
        _set_mode(ctx, False)
    ctx._g_count = 0
