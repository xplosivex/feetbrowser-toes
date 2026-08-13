"""toe-latin toe: render every page in Pig Latin.

`on_load` walks the raw HTML, finds runs of alphabetic text outside of tags,
and translates each word: words starting with a consonant shift the leading
consonant cluster to the end plus "ay"; words starting with a vowel get
"yay". Tags and attributes are preserved untouched, so the page still
renders and links still work.
"""

import re

_VOWELS = "aeiouAEIOU"


def activate(ctx):
    ctx.on("on_load", on_load)


def on_load(url, body):
    return _pig_latin_html(body)


def _pig_latin_html(body):
    out = []
    i = 0
    n = len(body)
    while i < n:
        c = body[i]
        if c == "<":
            # Copy the tag (and any raw-text content) verbatim.
            if body[i:i + 7].lower() == "<script" or \
                    body[i:i + 6].lower() == "<style":
                end = body.find("</", i + 1)
                close = body.find(">", i)
                if end == -1:
                    out.append(body[i:])
                    i = n
                else:
                    # Find the matching close tag.
                    close_end = body.find(">", end)
                    if close_end == -1:
                        out.append(body[i:])
                        i = n
                    else:
                        out.append(body[i:close_end + 1])
                        i = close_end + 1
                continue
            close = body.find(">", i)
            if close == -1:
                out.append(body[i:])
                i = n
            else:
                out.append(body[i:close + 1])
                i = close + 1
            continue
        # Plain text: translate word-by-word until the next '<'.
        nxt = body.find("<", i)
        seg = body[i:nxt] if nxt != -1 else body[i:]
        out.append(_pig_words(seg))
        i = nxt if nxt != -1 else n
    return "".join(out)


def _pig_words(text):
    return re.sub(r"[A-Za-z]+", lambda m: _translate(m.group(0)), text)


def _translate(word):
    low = word.lower()
    if low[0] in _VOWELS:
        result = low + "yay"
    else:
        idx = 1
        while idx < len(low) and low[idx] not in _VOWELS and low[idx] != "y":
            idx += 1
        if idx >= len(low):
            result = low + "ay"
        else:
            result = low[idx:] + low[:idx] + "ay"
    if word.isupper():
        return result.upper()
    if word[:1].isupper() and word[1:].islower():
        return result.capitalize()
    return result
