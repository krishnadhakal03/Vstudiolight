╔══════════════════════════════════════════════════════════════╗
║              🎬 SHORTS VIDEO STUDIO — README                 ║
║         Local Designer + Google Colab GPU Renderer           ║
╚══════════════════════════════════════════════════════════════╝

WHAT IS THIS?
─────────────
A complete 2-file system for generating YouTube Shorts / TikTok / Reels
videos with GPU-accelerated rendering — no paid tools, no coding needed.

  studio.html     → Open in browser. Design your video visually.
  README.txt      → This file.

The studio generates Colab code that you paste and run to render the
actual MP4 video using Google's free T4 GPU.


─────────────────────────────────────────────────────────────────
STEP-BY-STEP GUIDE
─────────────────────────────────────────────────────────────────

STEP 1 — Open studio.html
  Double-click studio.html (or drag into Chrome/Firefox/Edge).
  No server needed. Works 100% offline.

STEP 2 — Design your video
  • Left sidebar: set resolution, FPS, language, quality, filename
  • Load a template (Finance, Motivation, Tech, Mystery) or start blank
  • Edit each scene: headline, sub text, narration, layout, FX, colour
  • Preview tab: see a phone mockup of each scene
  • Scenes tab: reorder scenes with ↑ ↓ buttons, remove with ✕

STEP 3 — Generate Colab code
  Click ⚡ "Generate All Colab Cells" button (top bar or Colab tab).
  5 code cells appear, each with a 📋 Copy button.
  Or click ⬇ "Download Package" to get a colab_cells.py file.

STEP 4 — Set up Google Colab
  a. Go to: https://colab.research.google.com
  b. Click "New notebook"
  c. Enable GPU: Runtime → Change runtime type → T4 GPU → Save
  d. Create 5 empty code cells (click + Code button)

STEP 5 — Paste and run
  Paste Cell 1 → Cell 2 → Cell 3 → Cell 4 → Cell 5
  Run each with Shift+Enter, top to bottom.

  ⏱ Cell 1: ~2 min (installs packages — only needed once per session)
  ⚡ Cell 2: instant (your config)
  ⚡ Cell 3: instant (background engine)
  ⚡ Cell 4: instant (text layout engine)
  🎬 Cell 5: renders video → auto-downloads to your computer

STEP 6 — Done!
  Your MP4 downloads automatically from Colab.
  Upload directly to YouTube Shorts, TikTok, or Instagram Reels.


─────────────────────────────────────────────────────────────────
MAKING A NEW VIDEO (after first setup)
─────────────────────────────────────────────────────────────────

  1. Go back to studio.html
  2. Edit your scenes (or load a different template)
  3. Click ⚡ Generate → copy only Cell 2 (your config)
  4. In Colab, replace Cell 2 content and re-run from Cell 2 onward
     (Skip Cell 1 — packages stay installed during the session)


─────────────────────────────────────────────────────────────────
SCENE LAYOUT TYPES
─────────────────────────────────────────────────────────────────

  hook      Left-anchored bold text stack with accent bar strip.
            Best for: opening hook, grabbing attention in 2 seconds.

  bigstat   Giant centred number/word with multi-layer glow effect.
            Best for: key statistics, dollar amounts, percentages.

  split     Bold headline + dark pill box with body text.
            Best for: problem reveals, before/after comparisons.

  code      Terminal-style box with traffic light dots.
            Best for: showing AI prompts, steps, formulas.

  cta       Centred text with subtle bounce animation.
            Best for: call-to-action endings, follow/comment asks.


─────────────────────────────────────────────────────────────────
VISUAL FX TYPES
─────────────────────────────────────────────────────────────────

  particles   Floating accent-coloured dots. Great for stat scenes.
  scanlines   Subtle TV scan lines. Cinematic/professional feel.
  glitch      Digital slice shifts + colour fringe. Great for hooks.
  pulse       Expanding ring from centre. Great for CTA scenes.
  none        Clean background only.


─────────────────────────────────────────────────────────────────
RENDER TIME ESTIMATES (Colab Free T4 GPU)
─────────────────────────────────────────────────────────────────

  15s video (5 scenes × 3s)  →  ~2–4 minutes
  28s video (7 scenes × 4s)  →  ~4–7 minutes
  30s video (10 scenes × 3s) →  ~5–8 minutes

  GPU renders at ~80–120 fps.
  CPU fallback (no GPU available) renders at ~15–25 fps.


─────────────────────────────────────────────────────────────────
TROUBLESHOOTING
─────────────────────────────────────────────────────────────────

  "No module named cupy"
  → Normal! CuPy is for GPU. Script automatically falls back to CPU.

  "ImageMagick security policy error"
  → Cell 1 fixes this automatically. If it persists, re-run Cell 1.

  "CUDA out of memory"
  → Reduce resolution (1080×1080 instead of 1080×1920) or fewer scenes.

  "gTTS connection error"
  → Check that Colab has internet access. Try: !ping google.com

  "FileNotFoundError: font"
  → Cell 1 installs fonts. Re-run Cell 1 if this appears.

  Colab disconnects mid-render
  → Re-run Cell 1, then jump straight to Cell 5. No need to redo 2–4.

  Video has no audio
  → Check narration field isn't empty. gTTS needs internet in Colab.


─────────────────────────────────────────────────────────────────
OUTPUT SPECS
─────────────────────────────────────────────────────────────────

  Format    : MP4 (H.264 + AAC audio)
  Default   : 1080×1920 portrait (YouTube Shorts / TikTok / Reels)
  Quality   : CRF 18 (high — near lossless visually)
  Audio     : 192kbps AAC, narration via gTTS
  Flags     : +faststart (instant play on web, no buffering)


─────────────────────────────────────────────────────────────────
TIPS FOR VIRAL SHORTS
─────────────────────────────────────────────────────────────────

  ✅ Hook scene must grab in 2 seconds — use "hook" layout
  ✅ Include a specific number/stat — use "bigstat" layout
  ✅ Narration and captions must match — write what you'd say out loud
  ✅ End with a clear CTA — "Comment X", "Follow for Y"
  ✅ Keep total video under 30 seconds for Shorts algorithm boost
  ✅ Use glitch FX on hook, pulse FX on CTA
  ✅ Accent colour should match your channel brand

─────────────────────────────────────────────────────────────────
