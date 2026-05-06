"""
Vstudiolight approved Stable Video Diffusion img2vid Colab test.

Purpose
-------
Save the working SVD img2vid workflow that successfully generated a short AI
motion clip in Google Colab on T4 GPU. This is a reference experiment for a
future Vstudiolight AI motion asset layer.

Working settings from the approved test:
- image resize: 768x448
- num_frames: 14
- num_steps: 16
- fps_id: 6
- motion_bucket_id: 85
- cond_aug: 0.02
- seed: 42
- decoding_t: 1

Known failed settings:
- 1024x576 caused T4 CUDA out-of-memory during decoding.
- 512x288 caused internal tensor/feature-map mismatch.

Usage
-----
Open a fresh Google Colab notebook, set Runtime to T4 GPU or better, then copy
CELL_1_INSTALL, CELL_2_MODEL_AND_FUNCTIONS, CELL_3_UPLOAD_IMAGE, and
CELL_4_GENERATE_VIDEO into four separate Colab cells and run in order.

Do not mix with older failed SVD cells in the same runtime.
"""

CELL_1_INSTALL = r'''
!nvidia-smi

!apt-get -y install aria2 ffmpeg -qq

!rm -rf /content/generative-models
!rm -rf /content/outputs
!mkdir -p /content/checkpoints /content/outputs /content/scripts/util/detection

!git clone -q -b dev https://github.com/camenduru/generative-models /content/generative-models

!pip install -q \
  pytorch-lightning \
  omegaconf \
  einops \
  open-clip-torch \
  kornia \
  invisible-watermark \
  safetensors \
  transformers \
  accelerate \
  scipy \
  matplotlib \
  fire \
  gradio \
  imageio \
  imageio-ffmpeg \
  moviepy \
  xformers

!pip install -q -e /content/generative-models
!pip install -q -e git+https://github.com/Stability-AI/datapipelines@main#egg=sdata

!aria2c --console-log-level=error -c -x 8 -s 8 -k 1M \
  "https://huggingface.co/vdo/stable-video-diffusion-img2vid-xt/resolve/main/svd_xt.safetensors?download=true" \
  -d /content/checkpoints -o svd_xt.safetensors

!ln -sf /content/generative-models/scripts/util/detection/p_head_v1.npz /content/scripts/util/detection/p_head_v1.npz
!ln -sf /content/generative-models/scripts/util/detection/w_head_v1.npz /content/scripts/util/detection/w_head_v1.npz

import torch, xformers, pytorch_lightning
print("✅ Cell 1 complete")
print("CUDA:", torch.cuda.is_available())
print("Torch:", torch.__version__)
print("xformers:", xformers.__version__)
'''

CELL_2_MODEL_AND_FUNCTIONS = r'''
import os, sys, math, gc, cv2, torch
import numpy as np
from glob import glob
from PIL import Image
from einops import rearrange, repeat
from omegaconf import OmegaConf
from torchvision.transforms import ToTensor

sys.path.append("/content/generative-models")

import xformers
import xformers.ops
from sgm.util import instantiate_from_config

device = "cuda" if torch.cuda.is_available() else "cpu"
print("Device:", device)

def load_model(config_path: str, device: str, num_frames: int, num_steps: int):
    config = OmegaConf.load(config_path)
    config.model.params.conditioner_config.params.emb_models[0].params.open_clip_embedding_config.params.init_device = device
    config.model.params.sampler_config.params.num_steps = num_steps
    config.model.params.sampler_config.params.guider_config.params.num_frames = num_frames

    print("Loading model...")
    model = instantiate_from_config(config.model).to(device).eval().requires_grad_(False)
    model.conditioner.cpu()
    model.first_stage_model.cpu()
    model.model.to(dtype=torch.float16)
    torch.cuda.empty_cache()
    gc.collect()
    print("✅ Model loaded")
    return model

model_config = "/content/generative-models/scripts/sampling/configs/svd_xt.yaml"
MODEL_FRAMES = 14
MODEL_STEPS = 12
model = load_model(model_config, device, MODEL_FRAMES, MODEL_STEPS)

def get_unique_embedder_keys_from_conditioner(conditioner):
    return list(set([x.input_key for x in conditioner.embedders]))

def get_batch(keys, value_dict, N, T, device, dtype=None):
    batch = {}
    batch_uc = {}
    for key in keys:
        if key == "fps_id":
            batch[key] = torch.tensor([value_dict["fps_id"]]).to(device, dtype=dtype).repeat(int(math.prod(N)))
        elif key == "motion_bucket_id":
            batch[key] = torch.tensor([value_dict["motion_bucket_id"]]).to(device, dtype=dtype).repeat(int(math.prod(N)))
        elif key == "cond_aug":
            batch[key] = repeat(torch.tensor([value_dict["cond_aug"]]).to(device, dtype=dtype), "1 -> b", b=math.prod(N))
        elif key == "cond_frames":
            batch[key] = repeat(value_dict["cond_frames"], "1 ... -> b ...", b=N[0])
        elif key == "cond_frames_without_noise":
            batch[key] = repeat(value_dict["cond_frames_without_noise"], "1 ... -> b ...", b=N[0])
        else:
            batch[key] = value_dict[key]
    if T is not None:
        batch["num_video_frames"] = T
    for key in batch.keys():
        if key not in batch_uc and isinstance(batch[key], torch.Tensor):
            batch_uc[key] = torch.clone(batch[key])
    return batch, batch_uc

def prepare_image_low_vram(input_path: str):
    # Approved working setting: 768x448.
    # 512x288 caused feature-map mismatch; 1024x576 caused T4 decoding OOM.
    with Image.open(input_path) as image:
        if image.mode == "RGBA":
            image = image.convert("RGB")
        image = image.resize((768, 448))
        image = ToTensor()(image)
        image = image * 2.0 - 1.0
        image = image.unsqueeze(0).to(device)
    return image

def sample_video_low_vram(
    input_path: str,
    num_frames: int = 14,
    num_steps: int = 16,
    fps_id: int = 6,
    motion_bucket_id: int = 85,
    cond_aug: float = 0.02,
    seed: int = 42,
    decoding_t: int = 1,
    output_folder: str = "/content/outputs"
):
    if num_frames != MODEL_FRAMES:
        raise ValueError(f"Keep num_frames={MODEL_FRAMES}. You passed {num_frames}.")

    torch.manual_seed(seed)
    torch.cuda.empty_cache()
    gc.collect()
    model.sampler.guider.num_frames = num_frames

    image = prepare_image_low_vram(input_path)
    H, W = image.shape[2:]
    shape = (num_frames, 4, H // 8, W // 8)

    value_dict = {
        "motion_bucket_id": motion_bucket_id,
        "fps_id": fps_id,
        "cond_aug": cond_aug,
        "cond_frames_without_noise": image,
        "cond_frames": image + cond_aug * torch.randn_like(image),
    }

    model.conditioner.cpu()
    model.first_stage_model.cpu()
    torch.cuda.empty_cache()
    gc.collect()
    model.sampler.verbose = True

    with torch.no_grad():
        with torch.autocast("cuda"):
            print("Conditioning...")
            model.conditioner.to(device)
            batch, batch_uc = get_batch(
                get_unique_embedder_keys_from_conditioner(model.conditioner),
                value_dict,
                [1, num_frames],
                T=num_frames,
                device=device,
            )
            c, uc = model.conditioner.get_unconditional_conditioning(
                batch,
                batch_uc=batch_uc,
                force_uc_zero_embeddings=["cond_frames", "cond_frames_without_noise"],
            )
            model.conditioner.cpu()
            torch.cuda.empty_cache()
            gc.collect()

            for k in ["crossattn", "concat"]:
                uc[k] = repeat(uc[k], "b ... -> b t ...", t=num_frames)
                uc[k] = rearrange(uc[k], "b t ... -> (b t) ...")
                c[k] = repeat(c[k], "b ... -> b t ...", t=num_frames)
                c[k] = rearrange(c[k], "b t ... -> (b t) ...")
            for k in uc.keys():
                uc[k] = uc[k].to(dtype=torch.float16)
                c[k] = c[k].to(dtype=torch.float16)

            randn = torch.randn(shape, device=device, dtype=torch.float16)
            additional_model_inputs = {
                "image_only_indicator": torch.zeros(2, num_frames).to(device, dtype=torch.float16),
                "num_video_frames": batch["num_video_frames"],
            }

            def denoiser(input, sigma, cond):
                return model.denoiser(model.model, input, sigma, cond, **additional_model_inputs)

            print("Sampling...")
            samples_z = model.sampler(denoiser, randn, cond=c, uc=uc)
            samples_z = samples_z.to(dtype=model.first_stage_model.dtype)
            torch.cuda.empty_cache()
            gc.collect()

            print("Decoding with decoding_t=1...")
            model.en_and_decode_n_samples_a_time = decoding_t
            model.first_stage_model.to(device)
            samples_x = model.decode_first_stage(samples_z)
            samples = torch.clamp((samples_x + 1.0) / 2.0, min=0.0, max=1.0)
            model.first_stage_model.cpu()
            torch.cuda.empty_cache()
            gc.collect()

    os.makedirs(output_folder, exist_ok=True)
    video_path = os.path.join(output_folder, f"{len(glob(os.path.join(output_folder, '*.mp4'))):06d}.mp4")
    writer = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*"mp4v"), fps_id + 1, (samples.shape[-1], samples.shape[-2]))
    vid = ((rearrange(samples, "t c h w -> t h w c") * 255).cpu().numpy().astype(np.uint8))
    for frame in vid:
        writer.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    writer.release()
    print("✅ Saved:", video_path)
    return video_path

print("✅ Cell 2 complete — generator ready")
'''

CELL_3_UPLOAD_IMAGE = r'''
from google.colab import files
import os

uploaded = files.upload()
input_name = next(iter(uploaded.keys()))
input_path = f"/content/{input_name}"

print("✅ Uploaded:", input_path)
print("Size MB:", os.path.getsize(input_path) / 1024 / 1024)
'''

CELL_4_GENERATE_VIDEO = r'''
from IPython.display import Video, display
from google.colab import files
import os, gc, torch

torch.cuda.empty_cache()
gc.collect()

video_path = sample_video_low_vram(
    input_path=input_path,
    num_frames=14,
    num_steps=16,
    fps_id=6,
    motion_bucket_id=85,
    cond_aug=0.02,
    seed=42,
    decoding_t=1
)

print("Video path:", video_path)
print("File size MB:", os.path.getsize(video_path) / 1024 / 1024)

display(Video(video_path, embed=True, width=360))
files.download(video_path)
'''

print("Approved SVD Colab test script loaded. Copy each CELL_* string into separate Colab cells.")
