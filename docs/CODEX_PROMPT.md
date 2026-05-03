# Vstudiolight Developer Prompt

This prompt is intended for developers working on the Vstudiolight repository.

## Key constraints

- Preserve the baseline renderer behavior and visual output.
- Do not modify `Best video script.txt`.
- Any refactor or enhancement should keep the current POC intact.

## Baseline markers

The baseline is defined by the existing renderer script. Changes should preserve the following markers in `Best video script.txt`:

- `CELL 1`
- `SCENES`
- `make_bg`
- `compose`
- `gTTS`
- `shorts_fixed_final.mp4`

## Developer guidance

- Use `studio.html` for UI and code generation tweaks.
- Use `scripts/validate_baseline.py` to verify the baseline script remains intact.
- Add new renderer logic only after documenting the change and preserving compatibility with the current visual output.

## Project intent

Vstudiolight is a proof of concept for browser-driven short video creation via Google Colab. The repository should remain easy to understand, with clear docs and a stable baseline.
