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
    ctx.on("on_load", on_load)

def on_load(url, body):
    if str(url) == "about:blank" and body:
        link = '<li><a href="file:///home/arglinux/test-gtk.html">GTK Theme Tester</a> &mdash; verify your forms and scrollbars match your Linux desktop!</li>'
        return body.replace('</ul>', f'  {link}\n      </ul>')
    return None

def extra_css(url):
    return GTK_CSS

GTK_CSS = """
/* Adwaita/GTK-like advanced styling for web elements */
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



input[type="text"], input[type="password"], input[type="email"], input[type="search"], textarea, select {
    background-color: #ffffff !important;
    color: #2e3436 !important;
    border: 1px solid #cdc7c2 !important;
    border-radius: 4px !important;
    padding: 5px 8px !important;
    font-family: system-ui, sans-serif !important;
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

GTK_TEST_HTML = """<!DOCTYPE html>
<html>
<head>
    <title>GTK Theme Test</title>
</head>
<body style="padding: 20px; font-family: sans-serif;">
    <h1>Testing GTK Theme Toe</h1>
    <p>This is a simple test page with standard HTML form elements.</p>
    
    <div style="margin-bottom: 15px;">
        <label>Text Input:</label><br>
        <input type="text" placeholder="Type something here...">
    </div>
    
    <div style="margin-bottom: 15px;">
        <label>Select Dropdown:</label><br>
        <select>
            <option>Option 1</option>
            <option>Option 2</option>
            <option>Option 3</option>
        </select>
    </div>
    
    <div style="margin-bottom: 15px;">
        <label>Buttons:</label><br>
        <button>Standard Button</button>
        <input type="submit" value="Submit Input">
        <input type="button" value="Normal Input">
    </div>

    <div style="margin-bottom: 15px;">
        <label>Textarea:</label><br>
        <textarea rows="4" cols="30">Scrollbars might appear here if you type a lot!</textarea>
    </div>

    <div style="height: 2000px; padding-top: 50px;">
        <p><i>(Scroll down to see the styled GTK Adwaita scrollbar in action!)</i></p>
    </div>
</body>
</html>
"""
