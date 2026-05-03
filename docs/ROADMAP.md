# Vstudiolight Roadmap

## Vision

Vstudiolight is a lightweight browser-driven video studio that exports Google Colab code for generating vertical short-form videos. The focus is on preserving the existing visual baseline while enabling future improvements in renderer quality, workflow, and user experience.

## Current baseline

- `studio.html` is the current proof of concept.
- `Best video script.txt` is the baseline renderer reference.
- The visual output produced by the existing renderer is the project baseline.

## Short-term goals

- Maintain the original renderer and visual output as the baseline.
- Add project structure, documentation, and validation tooling.
- Improve project hygiene with `.gitignore` and a clear repo layout.
- Add automated checks ensuring baseline markers remain present.

## Medium-term goals

- Stabilize the Colab export flow and improve editor usability.
- Add examples and sample scene presets.
- Enhance docs with usage guides and troubleshooting.
- Introduce CI checks for baseline validation and project formatting.

## Long-term goals

- Plan a renderer refactor only after the baseline is fully documented.
- Add support for user-supplied fonts, custom assets, and more layout styles.
- Create an interactive preview mode that closely matches the Colab renderer.
- Explore additional export targets beyond Colab.
