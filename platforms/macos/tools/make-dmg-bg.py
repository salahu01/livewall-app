"""Draws the DMG window background (660x420 @1x and @2x) for tools/make-dmg.sh."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def draw(scale):
    W, H = 660 * scale, 420 * scale
    im = Image.new("RGB", (W, H))
    px = im.load()
    # Dark vertical gradient: the desktop a wallpaper sits on.
    for y in range(H):
        t = y / H
        c = (int(22 + 10 * t), int(24 + 8 * t), int(38 + 14 * t))
        for x in range(W):
            px[x, y] = c
    d = ImageDraw.Draw(im)

    def font(sz, bold=False):
        for f in (["/System/Library/Fonts/SFNSRounded.ttf"] if bold else []) + [
            "/System/Library/Fonts/SFNS.ttf", "/System/Library/Fonts/Helvetica.ttc"]:
            try:
                return ImageFont.truetype(f, sz * scale)
            except OSError:
                pass
        return ImageFont.load_default()

    t = "Drag LiveWall into Applications"
    f = font(22, True)
    d.text(((W - d.textlength(t, font=f)) / 2, 46 * scale), t, font=f, fill=(236, 238, 248))
    s = "then open it from Launchpad — it lives in your menu bar"
    f2 = font(13)
    d.text(((W - d.textlength(s, font=f2)) / 2, 82 * scale), s, font=f2, fill=(150, 156, 184))
    # Dashed arrow between the icon slots (icons at x=170 and x=490, y=230).
    y = 230 * scale
    col = (110, 130, 220)
    for x in range(255 * scale, 395 * scale, 18 * scale):
        d.rounded_rectangle((x, y - 3 * scale, x + 10 * scale, y + 3 * scale), 3 * scale, fill=col)
    d.polygon([(400 * scale, y - 14 * scale), (420 * scale, y), (400 * scale, y + 14 * scale)], fill=col)
    return im


os.makedirs(f"{ROOT}/build/dmg", exist_ok=True)
draw(1).save(f"{ROOT}/build/dmg/bg.png")
draw(2).save(f"{ROOT}/build/dmg/bg@2x.png")
