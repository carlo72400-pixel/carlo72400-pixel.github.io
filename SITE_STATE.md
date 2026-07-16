# CHROME DIGICAM — site state (saved Jul 15 2026, updated late)

> NEW SESSION START HERE: read this file + the job-hunt-2026 memory. Site is LIVE and current. Edit `index.html`, then `cp index.html index-kawaii.html`, commit, push. Verify visual changes with HEADLESS Chrome (see Gotchas), not just the preview pane.

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

## Interactive features (all working)
- Nav: sticky, section-aware; mobile = swipe chip row (all 7 sections). Nav tabs + in-page links route to the section's PAGE-BREAK BAND (JS in the last <script>), so tapping a tab lands on that chapter card.
- PAGE-BREAK BANDS: bold dark "film-slate" divider before each section (built by JS from a PAGES array: REEL 0N/07 + name + descriptor + lace trim). This is the "sections feel like pages" treatment (he chose full-screen breaks + keep-scroll). Band height clamp(300px,46svh,460px). NO scroll-snap (it hung the preview renderer; removed).
- Back-to-top: `#toTop` circle at top of the floating stack, `.show` toggles when scrollY > 85% of viewport.
- Hero: 100svh full-screen, PP chip cycles 6 looks, resize regrades. Hint wraps clear of the RATES/SHARE buttons on mobile; datestamp hidden < 640px.
- Floating buttons bottom-right: back-to-top + RATES (jumps to #rates) + SHARE.
- SHARE panel order QR -> socials -> rates. QR sticker = decoden camera with QR as the viewfinder; tap to enlarge for scanning. QR -> homepage, jsQR-verified.
- Lightbox: centered, fits full image to screen (fixed the *{margin:0} top-left/chopped bug via margin:auto). Stills, LIT, blue grid, FIELD KIT cards open full-res.
- Photo A/B grade slider; SA Current + reel videos autoplay on scroll (viewport observer, reduced-motion aware); IG reels link to the real posts.
- `<meta color-scheme:light>` set so phone dark-mode stops darkening the pastel design.

## Key assets (assets/kawaii/ unless noted)
- Hero photo: assets/hero.jpg (Alamodome). Decoden camera: hero_camera_web.jpg + FIELD KIT cards in kit/.
- Mascots retired (kept in Reference/kawaii-src); current decor = ribbon bow, charm, pixel heart-curtain, f2u/ pastel pixel dividers, lace_trim/doily.
- QR share sticker: qr_sticker.jpg.
- IG reels: reels/reel1_web.mp4 (+_poster), reels/reel2_web.mp4. Originals + all generated source PNGs archived in ~/Desktop/Vamppsych/Reference/kawaii-src/.
- CONTACT CARD (added Jul 16): `assets/kawaii/card/card_{front,back}_full.png` (lightbox, PNG so QR scans) + `_web.jpg` (display). Shown in the #contact footer ("Let's cut something") as 2 washi-taped `.polaroid` + `.kitzoom` lightbox cards. Full-art highlighter style; built by `~/Desktop/Vamppsych/contact-card/build_fullart_card.py` (that folder has the source PNGs). Front QR uses ERROR_CORRECT_L so it scans small.

## Printable Pokemon card  (~/Desktop/Vamppsych/card/)
- giancarlo_front.png + giancarlo_back.png, 1488x2076 = 2.5x3.5in double-sided hand-out. Back QR scan-verified.
- Reprint/iterate: build_front.py + build_back.py in that folder (run with `CARD_OUT=~/Desktop/Vamppsych/card /usr/bin/python3 build_front.py`). Swap the camera art for a face photo, add moves, or spin the full 4-card FIELD KIT set.

## Gotchas / how to verify (IMPORTANT for next session)
- The Claude Browser PREVIEW PANE could not execute programmatic scroll this session (window.scrollTo stayed 0, computer-scroll timed out) — confirmed it also fails on the LIVE site, so it is a PANE limitation, not the code. For any scroll-dependent check (page-break landing, back-to-top appearing, section reveals), use HEADLESS Chrome screenshots + PIL crops, or verify on a real device. Headless renders the full page reliably.
- Headless + `svh` units: in a very tall headless window (e.g. 412x24000) `svh` resolves to the WINDOW height, inflating svh-based sizes. Band height is clamped so it stays sane; if adding svh sizing, clamp it or capture at a normal window height.
- Screenshot recipe: `"/Applications/Google Chrome.app/.../Google Chrome" --headless --disable-gpu --hide-scrollbars --window-size=412,24000 --screenshot=out.png --virtual-time-budget=16000 "http://localhost:8931/index.html?proof"` then PIL-crop. `?proof` force-reveals scroll sections.
- Local server: `cd portfolio-site && python3 -m http.server 8931`.

## His source files (organized Jul 15)
- Shoot originals moved out of Downloads into `~/Desktop/Vamppsych/Shoots/`: blue-hair-editorial (20), lit-portraits (12), top-shelf-night (5), gear-flatlay (4), generated-art (2), footage (1), misc-photos (5).
- `~/Desktop/Vamppsych/Reference/` loose files sorted into photos/, aesthetic-saves/, product-refs/, tutorial-grabs/; `vamppsych_holic_default_register.png` kept at Reference root.
- Site source assets + reel originals archived in `Reference/kawaii-src/` (+ reels-src/).

## Still his court (not blocking)
- A/B slider frame pick (letters A-F candidate sheet).
- Releases OK for the two portrait models (blue-hair + rooftop scene-girl) before those stay public.
- Editor REEL: the one real content gap; needs the VMP drive.
- Literal Rogue font: download from his Envato Elements, then a one-line CSS swap.
