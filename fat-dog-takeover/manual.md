# Fat Dog Takeover

A port of the [Fat Dog Takeover](https://github.com/20plays/fatdogtakeover)
browser extension to a FeetBrowser toe.

Every image on every page — banners, avatars, thumbnails, video posters,
SVG images — becomes the iconic Fat Dog, stretched to fill whatever shape
the original occupied. The page layout is untouched: the toe reads where
each image was drawn on the canvas and paints the dog over exactly that box.

## Controls

- Toolbar button **DOG**: toggle the takeover on/off (persists; the current
  page reloads so the change is immediate).
- **`toehub://config/fat-dog-takeover`**: pick the stretch mode and a
  minimum image size.

## Stretch modes

| Mode | Effect |
|------|--------|
| Fill | Stretch the dog to the exact box (the signature effect; a banner stays a banner) |
| Cover | Scale up to cover the box, then crop to it — no distortion |
| Contain | Scale down to fit inside the box, centered; the original shows in the letterbox |

## How it works

FeetBrowser draws every image at its real displayed size, so the toe leaves
the HTML alone and, on each repaint, overlays the dog stretched over each
image's canvas box. The dog is bundled inside `toe.py` as base64 (96x128
PNG), decoded once, and resized per unique box size with the resized copies
cached — a repaint draws, it never rescales.

Not every image gets dogged: images that fail to decode render as their alt
text (no canvas image to cover), and you can set a minimum box area to leave
tiny icons alone.