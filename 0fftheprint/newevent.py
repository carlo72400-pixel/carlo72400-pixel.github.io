#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
0FF THE PRINT — event photo dump builder.

Point it at a folder of photos (and optional videos), it builds a shareable
gallery page under events/<slug>/ and adds it to the events index.

    /usr/bin/python3 newevent.py "/path/to/shoot" \
        --venue "Paper Tiger" --title "Blade Rave" --date 2026-08-14 \
        --limit 60

    # include short clips too (compressed to 720p)
    /usr/bin/python3 newevent.py "/path/to/shoot" --venue "The Mix" \
        --date 2026-08-16 --videos "/path/to/clips" --limit 50

Then: git add . && git commit && git push.

WHY IT COMPRESSES SO HARD: GitHub Pages wants the repo under ~1GB. Raw shoot
folders run 0.5-4GB each. Every image ships as a small grid thumb plus a
web-size full view, so a 60-photo event costs ~15MB instead of gigabytes.
"""
import argparse, json, os, re, shutil, subprocess, sys
from datetime import datetime

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("needs Pillow:  /usr/bin/python3 -m pip install --user Pillow")

Image.MAX_IMAGE_PIXELS = None
ROOT = os.path.dirname(os.path.abspath(__file__))
EVENTS = os.path.join(ROOT, "events")
PHOTO_EXT = {".jpg", ".jpeg", ".png", ".heic", ".HEIC", ".webp"}
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".MP4", ".MOV"}

THUMB_W, THUMB_Q = 520, 72          # grid tile
FULL_W,  FULL_Q  = 1600, 82         # lightbox view
VIDEO_H, VIDEO_CRF = 720, 30        # compressed clip


def slugify(s):
    return re.sub(r"(^-|-$)", "", re.sub(r"[^a-z0-9]+", "-", s.lower()))


def human(n):
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.0f}{u}"
        n /= 1024
    return f"{n:.1f}TB"


def dir_size(p):
    return sum(os.path.getsize(os.path.join(dp, f))
               for dp, _, fs in os.walk(p) for f in fs)


def pick(files, limit):
    """Evenly sample across the shoot so the night's arc survives the cull."""
    if not limit or limit >= len(files):
        return files
    step = len(files) / limit
    return [files[int(i * step)] for i in range(limit)]


def load_image(path):
    im = Image.open(path)
    im = ImageOps.exif_transpose(im)          # phones lie about orientation
    return im.convert("RGB")


def build_photos(src, out_dir, limit):
    files = sorted(f for f in os.listdir(src)
                   if os.path.splitext(f)[1] in PHOTO_EXT and not f.startswith("."))
    if not files:
        sys.exit(f"no photos found in {src}")
    chosen = pick(files, limit)
    os.makedirs(out_dir, exist_ok=True)
    items = []
    for i, fn in enumerate(chosen, 1):
        try:
            im = load_image(os.path.join(src, fn))
        except Exception as e:
            print(f"  skip {fn}: {e}")
            continue
        stem = f"{i:03d}"
        full = im.copy()
        full.thumbnail((FULL_W, FULL_W), Image.LANCZOS)
        full.save(os.path.join(out_dir, f"{stem}.jpg"), quality=FULL_Q, optimize=True)
        th = im.copy()
        th.thumbnail((THUMB_W, THUMB_W), Image.LANCZOS)
        th.save(os.path.join(out_dir, f"{stem}_t.jpg"), quality=THUMB_Q, optimize=True)
        items.append({"type": "photo", "src": f"media/{stem}.jpg",
                      "thumb": f"media/{stem}_t.jpg",
                      "w": full.width, "h": full.height})
        print(f"  [{i}/{len(chosen)}] {fn}", end="\r")
    print(f"  {len(items)} photos" + " " * 40)
    return items


def build_videos(src, out_dir, limit):
    if not shutil.which("ffmpeg"):
        print("  ffmpeg not found, skipping videos")
        return []
    files = sorted(f for f in os.listdir(src)
                   if os.path.splitext(f)[1] in VIDEO_EXT and not f.startswith("."))
    chosen = pick(files, limit)
    items = []
    for i, fn in enumerate(chosen, 1):
        stem = f"v{i:02d}"
        outv = os.path.join(out_dir, f"{stem}.mp4")
        subprocess.run([
            "ffmpeg", "-y", "-i", os.path.join(src, fn),
            "-vf", f"scale=-2:{VIDEO_H}", "-c:v", "libx264", "-crf", str(VIDEO_CRF),
            "-preset", "veryfast", "-c:a", "aac", "-b:a", "96k",
            "-movflags", "+faststart", outv,
        ], capture_output=True)
        if not os.path.exists(outv):
            print(f"  video failed: {fn}")
            continue
        size = os.path.getsize(outv)
        if size > 90 * 1024 * 1024:           # GitHub hard-rejects >100MB
            print(f"  {fn} still {human(size)} after compression, left out")
            os.remove(outv)
            continue
        poster = os.path.join(out_dir, f"{stem}_t.jpg")
        subprocess.run(["ffmpeg", "-y", "-i", outv, "-vf",
                        f"thumbnail,scale={THUMB_W}:-2", "-frames:v", "1", poster],
                       capture_output=True)
        items.append({"type": "video", "src": f"media/{stem}.mp4",
                      "thumb": f"media/{stem}_t.jpg"})
        print(f"  [{i}/{len(chosen)}] {fn} -> {human(size)}")
    return items


PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>__TITLE__ · __VENUE__ · 0FF THE PRINT</title>
<meta name="description" content="__COUNT__ frames from __TITLE__ at __VENUE__, __DATELONG__. Shot by 0FF THE PRINT.">
<meta name="theme-color" content="#0a0a0d">
<meta property="og:type" content="website">
<meta property="og:title" content="__TITLE__ · __VENUE__">
<meta property="og:description" content="__COUNT__ frames, __DATELONG__. Shot by 0FF THE PRINT.">
<meta property="og:image" content="https://carlo72400-pixel.github.io/0fftheprint/events/__SLUG__/preview.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://carlo72400-pixel.github.io/0fftheprint/events/__SLUG__/preview.jpg">
<link rel="icon" type="image/svg+xml" href="../../assets/favicon.svg">
<link href="https://fonts.googleapis.com/css2?family=Saira+Condensed:wght@900&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{--bg:#0a0a0d;--panel:#121218;--line:#23222b;--ink:#f4eef2;--muted:#9a93a3;
--pink:#f7b9dd;--pink-deep:#f48fc8;--pink-glow:#ff79c6;--dye-blue:#2f6bff;
--f-display:'Saira Condensed',sans-serif;--f-body:'Inter',system-ui,sans-serif;--f-mono:'JetBrains Mono',monospace;}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font-family:var(--f-body);font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}
.leopard-bar{height:14px;background:linear-gradient(90deg,var(--pink-deep),var(--pink) 25%,var(--dye-blue) 50%,var(--pink-deep) 75%,var(--pink))}
.wrap{max-width:1400px;margin:0 auto;padding:26px 18px 70px}
.back{font-family:var(--f-mono);font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);text-decoration:none;display:inline-block;margin-bottom:22px}
.back:hover{color:var(--pink-glow)}
h1{font-family:var(--f-display);font-style:italic;font-weight:900;text-transform:uppercase;
font-size:clamp(34px,7vw,76px);line-height:.94;letter-spacing:-.01em;
background:linear-gradient(180deg,#fff 10%,var(--pink) 45%,#8f8a97 60%,var(--pink-deep) 96%);
-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 4px 24px rgba(255,121,198,.22))}
.meta{font-family:var(--f-mono);font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:var(--muted);margin-top:10px}
.meta b{color:var(--pink-glow);font-weight:500}
.grid{columns:4 260px;column-gap:12px;margin-top:26px}
.tile{break-inside:avoid;margin:0 0 12px;position:relative;display:block;width:100%;
border:1px solid var(--line);border-radius:8px;overflow:hidden;background:var(--panel);cursor:zoom-in}
.tile img{width:100%;height:auto;display:block;transition:transform .35s ease,filter .35s ease}
.tile:hover img{transform:scale(1.03);filter:brightness(1.08)}
.tile.vid::after{content:'▶';position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
width:52px;height:52px;border-radius:50%;background:rgba(10,10,13,.72);border:1px solid var(--pink-deep);
color:var(--pink-glow);display:flex;align-items:center;justify-content:center;font-size:17px;padding-left:3px}
.foot{margin-top:44px;padding-top:20px;border-top:1px solid var(--line);
font-family:var(--f-mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.foot a{color:var(--pink-glow);text-decoration:none}
/* lightbox */
.lb{position:fixed;inset:0;z-index:200;background:rgba(6,6,9,.96);display:none;
align-items:center;justify-content:center;padding:26px}
.lb.open{display:flex}
.lb img,.lb video{max-width:100%;max-height:88vh;border-radius:8px;box-shadow:0 20px 70px rgba(0,0,0,.7)}
.lb-x,.lb-n,.lb-p{position:absolute;background:rgba(18,18,24,.9);border:1px solid var(--line);
color:var(--ink);width:46px;height:46px;border-radius:50%;cursor:pointer;font-size:18px}
.lb-x{top:18px;right:18px}
.lb-p{left:18px;top:50%;transform:translateY(-50%)}
.lb-n{right:18px;top:50%;transform:translateY(-50%)}
.lb-x:hover,.lb-n:hover,.lb-p:hover{border-color:var(--pink-deep);color:var(--pink-glow)}
.lb-count{position:absolute;bottom:18px;left:50%;transform:translateX(-50%);
font-family:var(--f-mono);font-size:11px;letter-spacing:.2em;color:var(--muted)}
@media (max-width:640px){.grid{columns:2 150px;column-gap:8px}.tile{margin-bottom:8px}
.lb-p,.lb-n{width:40px;height:40px}}
</style>
</head>
<body>
<div class="leopard-bar"></div>
<div class="wrap">
  <a class="back" href="../">&larr; All events</a>
  <h1>__TITLE__</h1>
  <div class="meta"><b>__VENUE__</b> &nbsp;·&nbsp; __DATELONG__ &nbsp;·&nbsp; __COUNT__ frames</div>
  <div class="grid" id="grid"></div>
  <div class="foot">Shot by 0FF THE PRINT &nbsp;·&nbsp;
    <a href="https://instagram.com/vamppsych" target="_blank" rel="noopener">@vamppsych</a>
    &nbsp;·&nbsp; Tagged in one of these? DM for the full-res file.</div>
</div>
<div class="lb" id="lb">
  <button class="lb-x" id="lbx" aria-label="Close">&times;</button>
  <button class="lb-p" id="lbp" aria-label="Previous">&#8249;</button>
  <button class="lb-n" id="lbn" aria-label="Next">&#8250;</button>
  <div id="lbstage"></div>
  <div class="lb-count" id="lbc"></div>
</div>
<script>
const MEDIA = __MEDIA__;
const grid = document.getElementById('grid');
grid.innerHTML = MEDIA.map((m,i) =>
  `<a class="tile${m.type==='video'?' vid':''}" data-i="${i}" href="${m.src}">
     <img src="${m.thumb}" alt="Frame ${i+1}" loading="lazy" decoding="async">
   </a>`).join('');
const lb=document.getElementById('lb'), stage=document.getElementById('lbstage'), count=document.getElementById('lbc');
let cur=0;
function show(i){
  cur=(i+MEDIA.length)%MEDIA.length;
  const m=MEDIA[cur];
  stage.innerHTML = m.type==='video'
    ? `<video src="${m.src}" controls autoplay playsinline></video>`
    : `<img src="${m.src}" alt="Frame ${cur+1}">`;
  count.textContent=`${cur+1} / ${MEDIA.length}`;
  lb.classList.add('open'); document.body.style.overflow='hidden';
}
function close(){lb.classList.remove('open');stage.innerHTML='';document.body.style.overflow='';}
grid.addEventListener('click',e=>{const t=e.target.closest('.tile');if(!t)return;e.preventDefault();show(+t.dataset.i);});
document.getElementById('lbx').onclick=close;
document.getElementById('lbn').onclick=()=>show(cur+1);
document.getElementById('lbp').onclick=()=>show(cur-1);
lb.addEventListener('click',e=>{if(e.target===lb)close();});
document.addEventListener('keydown',e=>{
  if(!lb.classList.contains('open'))return;
  if(e.key==='Escape')close(); if(e.key==='ArrowRight')show(cur+1); if(e.key==='ArrowLeft')show(cur-1);
});
</script>
</body>
</html>
"""


def make_og(first_photo, out_path, title, venue, datelong):
    """Event OG card: the night's own frame, darkened, so links unfurl."""
    im = load_image(first_photo)
    W, H = 1200, 630
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    im = im.crop(((im.width - W) // 2, (im.height - H) // 2,
                  (im.width - W) // 2 + W, (im.height - H) // 2 + H))
    from PIL import ImageDraw, ImageEnhance
    im = ImageEnhance.Brightness(im).enhance(0.52)
    d = ImageDraw.Draw(im)
    d.rectangle([0, H - 14, W, H], fill=(244, 143, 200))
    try:
        big = ImageFontTruetype("/System/Library/Fonts/Supplemental/Impact.ttf", 96)
    except Exception:
        big = None
    d.text((54, H - 190), title.upper(), fill=(255, 255, 255), font=big)
    d.text((56, H - 96), f"{venue.upper()}   ·   {datelong.upper()}", fill=(247, 185, 221))
    d.text((56, 44), "0FF THE PRINT", fill=(255, 121, 198))
    im.save(out_path, quality=88)


def ImageFontTruetype(path, size):
    from PIL import ImageFont
    return ImageFont.truetype(path, size)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source", help="folder of photos")
    ap.add_argument("--venue", required=True)
    ap.add_argument("--title", help="event name (defaults to the venue)")
    ap.add_argument("--date", required=True, help="YYYY-MM-DD")
    ap.add_argument("--videos", help="folder of clips (optional)")
    ap.add_argument("--limit", type=int, default=60, help="max photos (0 = all)")
    ap.add_argument("--video-limit", type=int, default=6)
    ap.add_argument("--slug", help="override the url slug")
    a = ap.parse_args()

    title = a.title or a.venue
    dt = datetime.strptime(a.date, "%Y-%m-%d")
    datelong = dt.strftime("%b %-d, %Y")
    dateshort = dt.strftime("%m.%d.%y")
    slug = a.slug or f"{a.date}-{slugify(title)}"
    out = os.path.join(EVENTS, slug)
    media_dir = os.path.join(out, "media")
    os.makedirs(media_dir, exist_ok=True)

    print(f"\nBuilding {slug}")
    items = build_photos(a.source, media_dir, a.limit)
    if a.videos:
        items += build_videos(a.videos, media_dir, a.video_limit)

    # OG card from the first frame of the night
    first = os.path.join(media_dir, "001.jpg")
    if os.path.exists(first):
        make_og(first, os.path.join(out, "preview.jpg"), title, a.venue, datelong)

    page = (PAGE.replace("__MEDIA__", json.dumps(items))
                .replace("__TITLE__", title)
                .replace("__VENUE__", a.venue)
                .replace("__DATELONG__", datelong)
                .replace("__COUNT__", str(len(items)))
                .replace("__SLUG__", slug))
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(page)
    json.dump({"slug": slug, "title": title, "venue": a.venue, "date": a.date,
               "date_short": dateshort, "count": len(items), "media": items},
              open(os.path.join(out, "data.json"), "w"), indent=2)

    # update the index
    idx_path = os.path.join(EVENTS, "events.json")
    idx = json.load(open(idx_path)) if os.path.exists(idx_path) else {"items": []}
    idx["items"] = [e for e in idx["items"] if e["slug"] != slug]
    idx["items"].append({"slug": slug, "title": title, "venue": a.venue,
                         "date": a.date, "date_short": dateshort,
                         "count": len(items), "cover": f"{slug}/media/001_t.jpg"})
    idx["items"].sort(key=lambda e: e["date"], reverse=True)
    json.dump(idx, open(idx_path, "w"), indent=2, ensure_ascii=False)

    size = dir_size(out)
    print(f"\n  {out}")
    print(f"  {len(items)} items, {human(size)}")
    if size > 40 * 1024 * 1024:
        print("  heads up: over 40MB. Lower --limit to keep the repo lean.")
    print(f"\n  live at /0fftheprint/events/{slug}/ once pushed")
    print("  git add -A && git commit -m 'event: " + slug + "' && git push\n")


if __name__ == "__main__":
    main()
