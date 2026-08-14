import sys
import subprocess
import json

_cached_css = None

def get_dynamic_css():
    global _cached_css
    if _cached_css is not None:
        return _cached_css
        
    script = """
import json
try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    Gtk.init(None)
    ctx = Gtk.StyleContext()
    
    def get_color(name, default):
        success, color = ctx.lookup_color(name)
        if success:
            return f"rgb({int(color.red*255)}, {int(color.green*255)}, {int(color.blue*255)})"
        return default
        
    colors = {
        "bg": get_color("theme_bg_color", "#f6f5f4"),
        "fg": get_color("theme_fg_color", "#000000"),
        "base": get_color("theme_base_color", "#ffffff"),
        "text": get_color("theme_text_color", "#000000"),
        "border": get_color("borders", "#cdc7c2"),
    }
    print(json.dumps(colors))
except Exception:
    print("{}")
"""
    try:
        output = subprocess.check_output(["python3", "-c", script], text=True, stderr=subprocess.DEVNULL)
        colors = json.loads(output.strip())
    except Exception:
        colors = {}

    bg = colors.get("bg", "#f6f5f4")
    fg = colors.get("fg", "#000000")
    base = colors.get("base", "#ffffff")
    text = colors.get("text", "#000000")
    border = colors.get("border", "#cdc7c2")
    
    _cached_css = f"""
button, input[type="button"], input[type="submit"] {{
    background: {bg} !important;
    color: {fg} !important;
    border: 1px solid {border} !important;
    border-radius: 4px !important;
    padding: 5px 12px !important;
}}

input[type="text"], input[type="password"], textarea, select {{
    background-color: {base} !important;
    color: {text} !important;
    border: 1px solid {border} !important;
    border-radius: 4px !important;
    padding: 5px 8px !important;
}}

/* Scrollbars */
::-webkit-scrollbar {{
    width: 12px;
    height: 12px;
}}
::-webkit-scrollbar-track {{
    background: {base};
    border-left: 1px solid {border};
}}
::-webkit-scrollbar-thumb {{
    background-color: {bg};
    border-radius: 6px;
    border: 3px solid {base};
}}
"""
    return _cached_css


def activate(ctx):
    if sys.platform != "linux":
        return
    ctx.on("extra_css", extra_css)
    ctx.on("on_load", on_load)

def on_load(url, body):
    if str(url) == "about:blank" and body:
        link = '<li><a href="file:///home/arglinux/test-gtk.html">GTK Theme Tester</a> &mdash; verify your forms and scrollbars match your Linux desktop!</li>'
        return body.replace('</ul>', f'  {link}\\n      </ul>')
    return None

def extra_css(url):
    return get_dynamic_css()
