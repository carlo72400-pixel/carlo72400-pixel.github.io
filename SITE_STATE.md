# CHROME DIGICAM — site state (saved Jul 15 2026)

## Live
- Homepage: https://carlo72400-pixel.github.io/  (this is the front door now)
- Repo: carlo72400-pixel/carlo72400-pixel.github.io, source in this folder.
- Deploy: edit `index.html`, `git add -A && git commit && git push`. If Pages sticks on "building", POST to `/pages/builds` via gh.
- Edit the LIVE file `index.html`. `index-kawaii.html` is a kept-identical copy (the old preview link); `cp index.html index-kawaii.html` after changes to keep them matched.

## Alt faces (all reachable, not the front door)
- `/index-camera.html` — the old Camera Interface homepage, preserved.
- `/dream/` — DREAM IN LOG.
- `/steel/` — CHROME & ROSES.

## Register
Pastel decoden / "kawaii AND professional." Ennaria pastels (blush, lilac, mint, baby blue, butter, peach) + silver chrome + white lace. Display font = Fraunces pushed to its Rogue-most axis (SOFT 100 / weight 640-680 / WONK 0). Body Inter, OSD JetBrains Mono. The real Kanye/Alamodome shot leads the hero full-bleed and regrades via the PP chip.

## Sections (nav order)
INFO (Editor first + FIELD KIT camera cards) -> PHOTO MODE (concert stills + A/B grade slider) -> ARCHIVE (SA Current tapes incl. TAPE 04 lucha, STILLS PULL x10, LIT SESSIONS, EDITORIAL PORTRAIT WORK) -> PLAYBACK (VOLUME + 2 BTS, YouTube) -> FEED (2 IG reels + TikTok tile) -> RATES -> STANDBY footer.

## Interactive features (all working, verified)
- Nav: sticky, section-aware; mobile = swipe chip row (all 7 sections).
- Hero: 100svh full-screen, PP chip cycles 6 looks, resize regrades.
- Floating buttons bottom-right: RATES (jumps to #rates) + SHARE.
- SHARE panel order QR -> socials -> rates. QR sticker = decoden camera with QR as the viewfinder; tap to enlarge for scanning. QR -> homepage, jsQR-verified.
- Lightbox: centered, fits full image to screen (fixed the top-left/chopped bug). Stills, LIT, blue grid, and FIELD KIT cards all open full-res.
- Photo A/B grade slider; SA Current + reel videos autoplay on scroll (viewport observer, reduced-motion aware); IG reels link to the real posts.

## Key assets (assets/kawaii/ unless noted)
- Hero photo: assets/hero.jpg (Alamodome). Decoden camera: hero_camera_web.jpg + FIELD KIT cards in kit/.
- Mascots retired (kept in Reference/kawaii-src); current decor = ribbon bow, charm, pixel heart-curtain, f2u/ pastel pixel dividers, lace_trim/doily.
- QR share sticker: qr_sticker.jpg.
- IG reels: reels/reel1_web.mp4 (+_poster), reels/reel2_web.mp4. Originals + all generated source PNGs archived in ~/Desktop/Vamppsych/Reference/kawaii-src/.

## Printable Pokemon card  (~/Desktop/Vamppsych/card/)
- giancarlo_front.png + giancarlo_back.png, 1488x2076 = 2.5x3.5in double-sided hand-out. Back QR scan-verified.
- Reprint/iterate: build_front.py + build_back.py in that folder (run with `CARD_OUT=~/Desktop/Vamppsych/card /usr/bin/python3 build_front.py`). Swap the camera art for a face photo, add moves, or spin the full 4-card FIELD KIT set.

## Still his court (not blocking)
- A/B slider frame pick (letters A-F candidate sheet).
- Releases OK for the two portrait models (blue-hair + rooftop scene-girl) before those stay public.
- Editor REEL: the one real content gap; needs the VMP drive.
- Literal Rogue font: download from his Envato Elements, then a one-line CSS swap.
