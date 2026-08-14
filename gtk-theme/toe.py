import sys

import os
import re

def get_gtk_color(name, default):
    try:
        theme_name = "Breeze"
        settings_path = os.path.expanduser("~/.config/gtk-3.0/settings.ini")
        if os.path.exists(settings_path):
            with open(settings_path, "r") as f:
                match = re.search(r"gtk-theme-name=(.+)", f.read())
                if match:
                    theme_name = match.group(1).strip()
        
        colors_path = os.path.expanduser("~/.config/gtk-3.0/colors.css")
        if os.path.exists(colors_path):
            with open(colors_path, "r") as f:
                content = f.read()
                suffix = theme_name.lower().replace("-", "")
                match = re.search(fr"@define-color\s+{name}(_{suffix})?\s+(#[0-9a-fA-F]+);", content)
                if match:
                    hex_val = match.group(2).lstrip('#')
                    r, g, b = tuple(int(hex_val[i:i+2], 16) for i in (0, 2, 4))
                    return f"rgb({r}, {g}, {b})"
                    
        import gi
        gi.require_version('Gtk', '3.0')
        from gi.repository import Gtk
        success, color = Gtk.StyleContext().lookup_color(name)
        if success:
            return f"rgb({int(color.red*255)}, {int(color.green*255)}, {int(color.blue*255)})"
            
    except Exception:
        pass
    return default

def generate_css():
    bg = get_gtk_color("theme_bg_color", "#f6f5f4")
    fg = get_gtk_color("theme_fg_color", "#000000")
    base = get_gtk_color("theme_base_color", "#ffffff")
    text = get_gtk_color("theme_text_color", "#000000")
    border = get_gtk_color("borders", "#cdc7c2")
    
    return f"""
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
    return generate_css()
