# Vstudiolight

Vstudiolight is a browser-based video studio proof of concept for generating short-form vertical videos via Google Colab.

## What it is

- A local `studio.html` interface for designing scenes, narration, and visual style.
- A Colab-oriented code generator that produces Python cells for rendering video.
- A baseline proof of concept that preserves the original visual output and renderer behavior.

## Repository structure

- `studio.html` — main browser UI for scene design and Colab code export
- `Best video script.txt` — baseline reference renderer and Colab script
- `legacy/Best video script.txt` — preserved copy of the original baseline script
- `docs/ROADMAP.md` — planned roadmap for the project
- `docs/CODEX_PROMPT.md` — developer prompt for future code changes
- `scripts/validate_baseline.py` — baseline validation utility

## How to use

1. Open `studio.html` in a browser.
2. Design or edit your scenes.
3. Generate the Colab cells and paste them into a Google Colab notebook.
4. Run the generated Colab code to render video.

## Notes

- This repository preserves the current proof of concept and baseline renderer.
- The original `Best video script.txt` is intentionally not modified.
- Future development should keep the visual output baseline intact until an explicit renderer rewrite is planned.
