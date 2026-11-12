# Art credits and license

## Images in this folder

- `secret-hitler-cover.png` — Discord Activity cover image (1920×1080)
- `secret-hitler-icon.png` — Discord app icon (512×512)

These images are adapted from the free **Secret Hitler print-and-play** edition:

- **Source:** https://www.secrethitler.com (`Secret_Hitler_Print_and_Play.pdf`)
- **Publisher / copyright holder:** © Goat, Wolf & Cabbage
- **Game design:** Max Temkin, Mike Boxleiter, Tommy Maranges
- **Illustration:** Mackenzie Schubert
- **License:** [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

### Changes we made

The logo and the Liberal, Fascist and Hitler role-card illustrations were cropped
from the PDF pages, resized, tinted onto a cream and orange background, and laid out
as a cover image and app icon. A credit line was added to the cover. The original
artwork itself was not redrawn.

### License for these adapted images

As required by ShareAlike, the adapted images in this folder are licensed under
**CC BY-NC-SA 4.0**, the same license as the original. You may share and adapt them
for **non-commercial** purposes only, with the same credit and license.

This license covers the artwork only. It does not apply to the source code in this
repository. This project is not affiliated with or endorsed by Goat, Wolf & Cabbage.

## Regenerating the images

`tools/` contains the scripts used to make them (macOS, needs Google Chrome):

1. Download `Secret_Hitler_Print_and_Play.pdf` from https://www.secrethitler.com
   into a folder outside the repo. The PDF is not committed here.
2. Render its pages: `swift tools/render.swift <pdf> <pages_dir> 4`
3. Compose the images: `python3 tools/compose.py <pages_dir> <out_dir>`
