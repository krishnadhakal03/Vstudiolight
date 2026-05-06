# SVD Colab Motion Test

## Why we tested this

We tested Stable Video Diffusion img2vid as a possible future AI motion asset layer for Vstudiolight.

The goal is not to replace the existing Vstudiolight renderer. The goal is to create short AI-generated motion clips from still keyframes, then use those clips later as scene backgrounds, b-roll, proof clips, or transition assets inside the existing Vstudiolight workflow.

## Approved working setup

This test successfully generated a short AI motion clip in Google Colab using a T4 GPU with reduced-resolution input.

Working settings:

- Image resize: `768x448`
- `num_frames`: `14`
- `num_steps`: `16`
- `fps_id`: `6`
- `motion_bucket_id`: `85`
- `cond_aug`: `0.02`
- `seed`: `42`
- `decoding_t`: `1`

The approved test script is saved at:

```text
experiments/svd_colab_approved_test.py
```

## What failed during testing

These settings were useful discoveries and should not be repeated blindly:

- `1024x576` caused CUDA out-of-memory on T4 during decoding.
- `512x288` caused an internal tensor/feature-map mismatch.
- Changing `num_frames` after loading the model caused frame-count mismatch errors unless the model sampler/guider was also updated.

## Recommended manual test flow

1. Open a fresh Google Colab notebook.
2. Set runtime to T4 GPU or better.
3. Copy the four `CELL_*` strings from `experiments/svd_colab_approved_test.py` into four separate Colab cells.
4. Run the cells in order.
5. Upload a clean cinematic source image, not a text-heavy screenshot.
6. Review the generated MP4 manually.

## Best input images

SVD works better with simple cinematic images than with UI screenshots or text-heavy graphics.

Good examples:

- Car insurance renewal letter on a wooden table.
- Car parked on a wet road at sunset.
- Money, bill, calculator, or credit-card scene.
- Product-style desk scene with one clear subject.

Avoid for first tests:

- Collages.
- UI screenshots.
- Dense text-heavy images.
- Images where exact readable text must stay perfect.

## Future Vstudiolight integration idea

The future workflow could be:

```text
image/keyframe -> SVD motion clip -> Vstudiolight scene background/b-roll -> final branded video
```

Possible future repo structure:

```text
assets/input_keyframes/
assets/generated_motion/
ai_motion/
  manifest_schema.py
  asset_registry.py
  prompts.py
```

Example future manifest:

```json
{
  "scene_id": "scene_02",
  "generator": "svd",
  "source_image": "assets/input_keyframes/scene_02.png",
  "output_video": "assets/generated_motion/scene_02.mp4",
  "duration": 2.3,
  "status": "generated"
}
```

## Current recommendation

Do not integrate SVD into the main renderer yet.

First, generate 3 to 5 test clips from clean images and compare:

- motion quality
- blur/deformation
- usefulness as b-roll
- render time
- stability on T4

If the quality remains good, then create a separate experimental branch for AI motion assets and keep the original renderer untouched.
