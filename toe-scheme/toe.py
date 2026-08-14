"""toe-scheme toe: register a custom URL scheme with the handle hook.

The framework already owns the reserved `toe://` hosts (hub, gallery,
hello), so this toe demonstrates the `handle` hook with its own scheme:

    echo://hello           a greeting page
    echo://<anything>      echoes back whatever you typed
    echo://links           shows how toe:// links behave (clickable, history)

Pages come back as ordinary HTML and flow through the normal pipeline, so
links are clickable, `view-source:` works, and history behaves like any
other page.
"""

import html as _html


def activate(ctx):
    ctx.on("handle", handle)


def handle(url, tab):
    if url.scheme != "echo":
        return None
    host = url.host or "echo"
    if host == "hello":
        return {}, _hello(), "text/html"
    if host == "links":
        return {}, _links(), "text/html"
    return {}, _echo(host), "text/html"


def _hello():
    return """
<!doctype html>
<html><head><title>echo://hello</title>
<style>
  body { font-family: Helvetica; margin: 60px; color: #222; }
  h1 { color: #1a73e8; font-size: 40px; }
  .sub { color: #666; }
  a { color: #1a73e8; }
</style></head>
<body>
  <h1>echo://hello</h1>
  <p class="sub">This page was rendered by a custom scheme handled by a toe.
  Type <b>echo://anything</b> in the address bar and it will echo back.</p>
  <p><a href="echo://links">echo://links</a> ·
     <a href="toe://hub">the ToeHub</a></p>
</body></html>
"""


def _echo(host):
    return f"""<!doctype html>
<html><head><title>echo://{host}</title>
<style>
  body {{ font-family: Helvetica; margin: 60px; color: #222; }}
  h1 {{ color: #1a73e8; font-size: 34px; }}
  .sub {{ color: #666; }}
  a {{ color: #1a73e8; }}
</style></head>
<body>
  <h1>echo://{_html.escape(host)}</h1>
  <p class="sub">Echo. The scheme handled it; the browser rendered it.</p>
  <p><a href="echo://hello">echo://hello</a> ·
     <a href="echo://links">echo://links</a></p>
</body></html>
"""


def _links():
    return """
<!doctype html>
<html><head><title>echo://links</title>
<style>
  body { font-family: Helvetica; margin: 60px; color: #222; }
  h1 { color: #1a73e8; }
  a { color: #1a73e8; }
</style></head>
<body>
  <h1>echo://links</h1>
  <p>Custom-scheme links work like any other link: clickable, history-aware,
  and view-source-able.</p>
  <ul>
    <li><a href="echo://hello">echo://hello</a></li>
    <li><a href="echo://one">echo://one</a></li>
    <li><a href="echo://two">echo://two</a></li>
  </ul>
</body></html>
"""
