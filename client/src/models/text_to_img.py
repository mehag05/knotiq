from pathlib import Path
import modal
from pydantic import BaseModel
import io
import random
import time
from pathlib import Path

import modal

MINUTES = 60

class ImageRequest(BaseModel):
    prompt: str

app = modal.App("example-text-to-image")

CACHE_DIR = "/cache"

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install(
        "accelerate==0.33.0",
        "diffusers==0.31.0",
        "fastapi[standard]==0.115.4",
        "huggingface-hub[hf_transfer]==0.25.2",
        "sentencepiece==0.2.0",
        "torch==2.5.1",
        "torchvision==0.20.1",
        "transformers~=4.44.0",
    )
    .env(
        {
            "HF_HUB_ENABLE_HF_TRANSFER": "1",  # faster downloads
            "HF_HUB_CACHE": CACHE_DIR,
        }
    )
)

with image.imports():
    import diffusers
    import torch
    from fastapi import Response

MODEL_ID = "adamo1139/stable-diffusion-3.5-large-turbo-ungated"
MODEL_REVISION_ID = "9ad870ac0b0e5e48ced156bb02f85d324b7275d2"

cache_volume = modal.Volume.from_name("hf-hub-cache", create_if_missing=True)

@app.cls(
    image=image,
    gpu="H100",
    timeout=10 * MINUTES,
    volumes={CACHE_DIR: cache_volume},
)
class Inference:
    @modal.enter()
    def load_pipeline(self):
        self.pipe = diffusers.StableDiffusion3Pipeline.from_pretrained(
            MODEL_ID,
            revision=MODEL_REVISION_ID,
            torch_dtype=torch.bfloat16,
        ).to("cuda")

    @modal.method()
    def run(
        self, prompt: str, batch_size: int = 1, seed: int = None
    ) -> list[bytes]:
        seed = seed if seed is not None else random.randint(0, 2**32 - 1)
        print("seeding RNG with", seed)
        torch.manual_seed(seed)
        images = self.pipe(
            prompt,
            num_images_per_prompt=batch_size,
            num_inference_steps=4,
            guidance_scale=0.0,
            max_sequence_length=512,
        ).images

        image_output = []
        for image in images:
            with io.BytesIO() as buf:
                image.save(buf, format="PNG")
                image_output.append(buf.getvalue())
        torch.cuda.empty_cache()
        return image_output
    
    
@app.function(
    image=modal.Image.debian_slim(python_version="3.12").pip_install("fastapi[standard]==0.115.4"),
    allow_concurrent_inputs=1000,
)
@modal.asgi_app()
def ui():
    from fastapi import FastAPI, HTTPException, Response
    from fastapi.middleware.cors import CORSMiddleware

    web_app = FastAPI()
    
    # Add CORS middleware to handle preflight requests
    web_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify actual origins
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )
    
    @web_app.post("/api/text_to_image")
    async def generate_image(request: ImageRequest):
        try:
            print(f"Generating image for prompt: {request.prompt}")
            start_time = time.time()
            
            output_dir = Path("/tmp/stable-diffusion")
            output_dir.mkdir(exist_ok=True, parents=True)

            
            inference_service = Inference()
            images = inference_service.run.remote(
                request.prompt,
                batch_size=4
            )
            
            for batch_idx, image_bytes in enumerate(images):
                output_path = (
                    output_dir
                    / f"output_{slugify(request.prompt)[:64]}_{str(1).zfill(2)}_{str(batch_idx).zfill(2)}.png"
                )
                if not batch_idx:
                    print("Saving outputs", end="\n\t")
                print(
                    output_path,
                    end="\n" + ("\t" if batch_idx < len(images) - 1 else ""),
                )
                output_path.write_bytes(image_bytes)
            
            duration = time.time() - start_time
            print(f"Generated image in {duration:.2f} seconds")
            
            return Response(
                content=images[0],
                media_type="image/png"
            )
        except Exception as e:
            print(f"Error generating image: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    return web_app


def slugify(s: str) -> str:
    return "".join(c if c.isalnum() else "-" for c in s).strip("-")
