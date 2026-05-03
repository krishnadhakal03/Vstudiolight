from pathlib import Path
import sys

BASELINE_FILE = Path(__file__).resolve().parents[1] / 'Best video script.txt'
REQUIRED_MARKERS = [
    'CELL 1',
    'SCENES',
    'make_bg',
    'compose',
    'gTTS',
    'shorts_fixed_final.mp4',
]


def main() -> int:
    if not BASELINE_FILE.exists():
        print(f'ERROR: Baseline file not found: {BASELINE_FILE}')
        return 1

    text = BASELINE_FILE.read_text(encoding='utf-8', errors='ignore')
    missing = [marker for marker in REQUIRED_MARKERS if marker not in text]

    if missing:
        print('ERROR: Baseline validation failed. Missing markers:')
        for marker in missing:
            print(f'  - {marker}')
        return 1

    print('Baseline validation passed.')
    print(f'Found baseline file: {BASELINE_FILE.name}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
