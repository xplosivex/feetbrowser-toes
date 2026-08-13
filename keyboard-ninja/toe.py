"""keyboard-ninja toe: vim-style navigation.

`on_keypress` intercepts keys when no address bar and no form field has
focus, turning the keyboard into a scroll controller:

    j / k     scroll down / up one step
    gg        jump to top
    G         jump to bottom
    g         toggle ninja mode (so ordinary typing stays normal)

Ninja mode is off by default; press "g" to enable it. While enabled, the
status bar reports where you are in the page.
"""

from feetbrowser import toes


def activate(ctx):
    ctx.on("on_keypress", lambda e: _key(ctx, e))
    ctx.on("buttons", lambda: [toes.ButtonDef("ninja", "N", "Ninja")])
    ctx.on("on_click", lambda btn_id: _click(ctx, btn_id))


def _click(ctx, btn_id):
    if btn_id != "ninja":
        return
    ctx.settings["ninja_on"] = not ctx.settings.get("ninja_on", False)
    ctx.save_settings()
    ctx.set_status("Ninja mode ON. j/k to scroll, gg/G to jump."
                   if ctx.settings["ninja_on"] else "Ninja mode OFF.")
    ctx.browser.draw()


def _key(ctx, e):
    if not ctx.settings.get("ninja_on", False):
        return False
    ch = getattr(e, "char", "")
    tab = ctx.current_tab()
    if not tab:
        return False
    if ch == "g":
        # gg = jump to top, single g toggles ninja mode.
        ctx._g_count = getattr(ctx, "_g_count", 0) + 1
        if ctx._g_count >= 2:
            ctx._g_count = 0
            tab.scroll = 0
            tab._clamp_scroll()
            ctx.browser.draw()
            return True
        ctx.browser.window.after(400, lambda: _reset_g(ctx))
        return True
    ctx._g_count = 0
    if ch == "G":
        tab.scroll_by(10 ** 9)
        ctx.browser.draw()
        return True
    if ch == "j":
        tab.scroll_by(80)
        ctx.browser.draw()
        return True
    if ch == "k":
        tab.scroll_by(-80)
        ctx.browser.draw()
        return True
    return False


def _reset_g(ctx):
    ctx._g_count = 0
