"""Compose a Discord cover + icon from the official Secret Hitler print-and-play pages.

Usage: python3 -I compose.py <hires_pages_dir> <out_dir> [preview]
Art: Secret Hitler print-and-play (c) Goat, Wolf & Cabbage, CC BY-NC-SA 4.0.
"""
import os, subprocess, sys

PAGES = os.path.abspath(sys.argv[1])
OUT = os.path.abspath(sys.argv[2])
PREVIEW = len(sys.argv) > 3
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
os.makedirs(OUT, exist_ok=True)

SIZES = {"page-01.png": (3191, 2479)}
DEFAULT = (3168, 2448)

# Crop rectangles (x, y, w, h) in high-res page pixels.
CROPS = {
    "logo":    ("page-01.png", 830, 640, 1540, 1020),
    "liberal": ("page-07.png", 210, 268, 640, 920),
    "hitler":  ("page-08.png", 1636, 268, 655, 920),
    "fascist": ("page-08.png", 2356, 268, 640, 920),
    "face":    ("page-08.png", 1640, 540, 630, 630),
}


def crop_div(name, w, extra=""):
    page, x, y, cw, ch = CROPS[name]
    pw, ph = SIZES.get(page, DEFAULT)
    s = w / cw
    h = ch * s
    return (f'<div style="width:{w:.0f}px;height:{h:.0f}px;'
            f'background:url(file://{PAGES}/{page}) {-x * s:.1f}px {-y * s:.1f}px / {pw * s:.1f}px {ph * s:.1f}px no-repeat;'
            f'mix-blend-mode:multiply;{extra}"></div>')


def shoot(html, name, w, h, scale=1):
    src = os.path.join(OUT, name + ".html")
    with open(src, "w") as f:
        f.write(html)
    png = os.path.join(OUT, name + ".png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--force-device-scale-factor={scale}", "--allow-file-access-from-files",
                    f"--window-size={w},{h}", f"--screenshot={png}", f"file://{src}"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, timeout=90)
    print("wrote", png)


HEAD = '<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;overflow:hidden}</style></head><body>'
FONT = "Futura, 'Avenir Next Condensed', 'Helvetica Neue', sans-serif"

if PREVIEW:
    cells = "".join(f'<div style="background:#fff;padding:6px"><b>{n}</b>{crop_div(n, 250)}</div>' for n in CROPS)
    shoot(HEAD + f'<div style="display:flex;gap:8px;background:#888;padding:8px;align-items:flex-start">{cells}</div></body></html>',
          "preview", 1650, 520)
    sys.exit()

CREAM, ORANGE, INK = "#f6e3c3", "#e3643f", "#33302c"

card = lambda n: (f'<div style="background:{CREAM};padding:10px;border-radius:14px;'
                  f'box-shadow:0 14px 34px rgba(0,0,0,.35)">{crop_div(n, 250)}</div>')

cover = HEAD + f"""
<div style="position:relative;width:1920px;height:1080px;background:{CREAM};font-family:{FONT};overflow:hidden">
  <div style="position:absolute;right:0;top:0;width:960px;height:1080px;background:{ORANGE}"></div>
  <div style="position:absolute;left:90px;top:205px">{crop_div('logo', 760, 'filter:brightness(1.12) contrast(1.15);')}</div>
  <div style="position:absolute;left:120px;top:770px;color:{INK};font-size:28px;font-weight:700;letter-spacing:7px">
    5–10 PLAYERS · DISCORD ACTIVITY</div>
  <div style="position:absolute;left:1010px;top:280px;display:flex;gap:26px">
    <div style="transform:rotate(-5deg) translateY(30px)">{card('liberal')}</div>
    <div style="transform:translateY(-10px)">{card('hitler')}</div>
    <div style="transform:rotate(5deg) translateY(30px)">{card('fascist')}</div>
  </div>
  <div style="position:absolute;right:28px;bottom:20px;color:{INK};opacity:.8;font-size:18px;letter-spacing:1px">
    Art adapted from Secret Hitler print-and-play © Goat, Wolf &amp; Cabbage · CC BY-NC-SA 4.0</div>
</div></body></html>"""

icon = HEAD + f"""
<div style="position:relative;width:512px;height:512px;background:{ORANGE};overflow:hidden">
  <div style="position:absolute;left:26px;top:26px;width:460px;height:460px;border-radius:50%;background:{CREAM};overflow:hidden">
    <div style="position:absolute;left:0;top:0">{crop_div('face', 460)}</div>
  </div>
</div></body></html>"""

shoot(cover, "cover", 1920, 1080)
shoot(icon, "icon", 512, 512, scale=2)  # 1024x1024 output, as Discord recommends
