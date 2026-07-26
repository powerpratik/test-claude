# Module 14 — Multimodal Models

Frontier "language" models stopped being text-only around 2023. This module
covers how images, audio, and video enter (and exit) the same Transformer — and
why the LLM turned out to be the universal hub.

## 14.1 The unifying trick: everything becomes tokens

The Transformer (module 3) doesn't care what its vectors mean. Multimodality is
mostly the art of **encoding other media into the same residual stream**:

- **Images in**: split the image into patches (e.g. 14×14 pixels); a **vision
  encoder** (a Vision Transformer, usually contrastively pretrained à la CLIP —
  matching images to captions across hundreds of millions of pairs) turns
  patches into embeddings; a small **projector** maps them into the LLM's
  embedding space. To the LLM, an image is now "a few hundred to a few thousand
  soft tokens" interleaved with text. (LLaVA showed how little glue this needs;
  frontier models refine the same shape and often train the whole stack jointly,
  natively interleaved from early in pretraining — GPT-4o/Gemini-style — rather
  than bolting vision on after.)
- **Audio in**: spectrogram → encoder → same story. Speech-native models skip
  the transcribe-first pipeline, which is why modern voice modes catch tone and
  interruptions.
- **Video in**: frames × time, aggressively subsampled/compressed — long-context
  machinery (module 6.4) is what makes hour-long video possible (Gemini's 1M+
  contexts earn their keep here).

**Cost intuition**: one image ≈ hundreds–thousands of tokens of context; video ≈
that × frames. Multimodal pricing and latency follow directly (module 8 logic
applies unchanged).

## 14.2 Generation on the way out

- **Text out** is unchanged — vision-language models are still next-token
  predictors that happen to *condition* on images ("describe, reason about,
  extract from" — not edit).
- **Images out**, two families:
  - **Diffusion** (Stable Diffusion, Midjourney, Flux): start from noise,
    iteratively denoise toward an image, guided by a text embedding; the
    denoiser is a U-Net or (now standard) a **diffusion transformer (DiT)**.
    Latent diffusion does this in a compressed latent space for efficiency.
  - **Autoregressive** image generation inside the LLM (GPT-4o-style native
    image output, late-2024 onward): predict image tokens like text tokens —
    weaker at photoreal texture than the best diffusion, dramatically better at
    following complex instructions and **rendering text in images**, because
    the full language model is doing the composing.
- **Video generation** (Sora, Veo): diffusion transformers over spacetime
  patches — impressive, compute-hungry, physics still imperfect.
- **Speech out**: neural codec tokens predicted autoregressively — voice is
  "just" another token stream, enabling real-time speech-to-speech models with
  emotional prosody.

## 14.3 What vision-language models are actually good at (early 2026)

Strong: OCR and document understanding (invoices, forms, papers — a quietly
huge industry), chart/diagram reading, screenshot understanding (the substrate
of computer-use agents, module 12.5), visual Q&A, spatial descriptions.

Weaker / gotchas: precise counting, fine-grained spatial relations, reading
analog clocks, small text at low resolution (know your model's image-resolution
limits — big images get downscaled or tiled), and **visual hallucination**:
asked a leading question about an object that isn't there, models often play
along (module 9.4's sycophancy, now with eyes).

## 14.4 Why it matters beyond the demos

1. **Agents need eyes**: computer use = screenshots in, clicks out. Document
   workflows = PDFs in, structured data out. Most real-world agent inputs are
   not clean text.
2. **Data wall relief** (module 5.6): video/audio are effectively unlimited
   training data and may teach world dynamics text can't.
3. **One model, one interface**: the 2026 default frontier model takes
   text+image+audio in one conversation; unimodal LLMs are becoming the special
   case.

## Mental models to carry forward

1. **Everything is tokens in the residual stream** — modality lives in the
   encoder/decoder at the edges, not in the core.
2. Understanding (encode → reason → text) and generation (diffusion or AR
   decoding) are **separate capabilities** with separate maturity curves.
3. Images are *expensive context*; budget them like the tokens they secretly
   are.
4. Trust-but-verify applies double: VLMs inherit hallucination and add visual
   confabulation.

## Exercises

1. Feed the same photo to a frontier VLM: ask (a) a neutral "describe this,"
   (b) a leading "why is the man angry?" when no one is angry. Observe 14.3's
   failure mode.
2. Give it a dense table screenshot → extract to JSON (schema from module 9).
   Then a rotated/blurry version. Find the breaking point.
3. Count tokens: send a small vs large image through an API and compare billed
   input tokens; reconcile with the provider's documented image-token formula.
4. Generate the same prompt in a diffusion tool and a native-AR image model
   (include required text in the image, e.g. a sign saying "OPEN 24 HOURS").
   Compare instruction-following vs texture quality (14.2's trade).

## Further reading

- Radford et al., *CLIP* (2021); Dosovitskiy et al., *ViT* (2020).
- Liu et al., *LLaVA* (2023) — the minimal VLM recipe, readable in an evening.
- Rombach et al., *Latent Diffusion* (2022); Peebles & Xie, *DiT* (2023).
- Any current frontier model card's multimodal section (GPT-4o/Gemini/Claude)
  for the state of the art at the time you read this.
