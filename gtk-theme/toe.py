"""gtk-theme toe: GTK Adwaita styling for web pages.

Injects GTK-like CSS to style forms, buttons, and basic elements to match
your Linux desktop environment. Only active on Linux to avoid breaking future
Windows or macOS versions.
"""

import sys

def activate(ctx):
    if sys.platform != "linux":
        return
    ctx.on("extra_css", extra_css)

def extra_css(url):
    return GTK_CSS

GTK_CSS = """
/* Adwaita/GTK-like basic styling for web elements */
button, input[type="button"], input[type="submit"], input[type="reset"] {
    background: linear-gradient(to bottom, #f6f5f4, #edebe9) !important;
    color: #2e3436 !important;
    border: 1px solid #cdc7c2 !important;
    border-radius: 4px !important;
    padding: 5px 10px !important;
    font-family: system-ui, sans-serif !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
    cursor: default !important;
}

button:hover, input[type="button"]:hover, input[type="submit"]:hover {
    background: linear-gradient(to bottom, #ffffff, #f6f5f4) !important;
}

button:active, input[type="button"]:active, input[type="submit"]:active {
    background: #d6d1ce !important;
    box-shadow: inset 0 1px 2px rgba(0,0,0,0.1) !important;
}

input[type="text"], input[type="password"], input[type="email"], input[type="search"], textarea, select {
    background-color: #ffffff !important;
    color: #2e3436 !important;
    border: 1px solid #cdc7c2 !important;
    border-radius: 4px !important;
    padding: 5px 8px !important;
    font-family: system-ui, sans-serif !important;
}

input[type="text"]:focus, input[type="password"]:focus, textarea:focus, select:focus {
    border-color: #3584e4 !important;
    outline: 1px solid #3584e4 !important;
    box-shadow: 0 0 0 2px rgba(53, 132, 228, 0.3) !important;
}

/* Scrollbars - if supported by the engine */
::-webkit-scrollbar {
    width: 12px;
    height: 12px;
}
::-webkit-scrollbar-track {
    background: #f6f5f4;
    border-left: 1px solid #e1dedb;
}
::-webkit-scrollbar-thumb {
    background-color: #c0bfbc;
    border-radius: 6px;
    border: 3px solid #f6f5f4;
}
::-webkit-scrollbar-thumb:hover {
    background-color: #9a9996;
}
"""
