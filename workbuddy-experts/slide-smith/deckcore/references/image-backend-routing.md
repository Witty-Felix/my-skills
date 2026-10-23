> **⚠️ 内嵌副本 · 生图规则已被宿主覆盖**
> 本文件随专家包分发。**所有 AI 生图一律使用宿主内置的 ImageGen 工具**，
> 包内不提供生图脚本，也不提供任何外部生图后端；不要读 `.env`，不要探测后端。
> 本文其余内容只讲宿主 ImageGen 的用法、图片规格与失败处理，不涉及任何外部生图后端。
> 依据：`SKILL.md` → Hard rule — image generation。

# Image Generation — host ImageGen only

**Rule — every `Acquire Via: ai` image is produced by the host's built-in ImageGen
tool.** That is the whole policy: no model choice, no provider table, no cascade,
no quota arithmetic. This package bundles no Cloudflare or ModelScope backend,
keeps no image credentials in `.env`, never probes a provider, and does no
free-quota scheduling; an older note describing a multi-model free tier is
obsolete.

## 1. What the tool needs from the plan

| Field | Rule |
|---|---|
| `items[].prompt` | The assembled prose paragraph from [`image-generator.md`](./image-generator.md) §4, passed unchanged |
| `items[].aspect_ratio` | Ask for the closest ratio the host supports — `1:1`, `4:3`, `3:4`, `16:9`, `9:16` |
| `items[].image_size` | `512px` / `1K` / `2K` / `4K` — the planned on-slide size, or one step above |
| `items[].text_policy` | `embedded` only when lettering must sit inside the picture; otherwise keep text native |
| CJK lettering | Long CJK strings render less reliably than latin; keep the sentence native and generate the visual only |

Resolutions come back at whatever the host emits: backfill the real pixels into
`Dimensions`; never upscale to fake a planned size.

## 2. Local post-processing stays in the pipeline

`image_treat.py --fit WxH` downscales an oversized render to its planned on-slide
size (never upscales); `slice_images.py --trim --alpha --bg` still cuts
illustration and icon sheets; native treatments (crop, shadow, opacity, scrim)
stay in SVG, per [`image-base.md`](./image-base.md).

## 3. When a generation fails

There is no external provider to fall back to, and falling back is not allowed.
Work the problem in this order:

1. **Reword the prompt** — fix the one dimension that is actually wrong (subject,
   composition, material, light), then call the tool again.
2. **Change the composition** — if the frame keeps breaking, move to a primitive or
   layout pattern that suits the subject ([`image-layout-patterns.md`](./image-layout-patterns.md),
   [`image-type-templates/`](./image-type-templates/)).
3. **Use a placeholder** — draw a dashed placeholder at the planned size, mark the
   row `Needs-Manual`, and state the reason in the completion report.

Never reach for an external image API, and never claim an image exists without a
file at its manifest path.
