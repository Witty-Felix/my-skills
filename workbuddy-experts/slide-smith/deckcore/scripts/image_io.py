#!/usr/bin/env python3
"""
Image download/save helpers shared by image_search.py.

Extracted verbatim from the retired external image-generation backend helper
module so the image-search pipeline keeps byte-identical download and
format-normalization behaviour without those backends.
"""

import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from console_encoding import configure_utf8_stdio  # noqa: E402

configure_utf8_stdio()

if __name__ == "__main__":
    print(__doc__)
    print("This is an internal helper module used by image_search.py.")
    raise SystemExit(0 if any(arg in {"-h", "--help", "help"} for arg in sys.argv[1:]) else 1)

import io  # noqa: E402
import os  # noqa: E402

import requests  # noqa: E402

try:
    from PIL import Image as PILImage, ImageOps as PILImageOps
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


class _RetryableBackendError(RuntimeError):
    """A backend failure whose enclosing operation should be repeated."""


CONTENT_TYPE_TO_EXT = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/webp": ".webp",
    "image/gif": ".gif",
    "image/bmp": ".bmp",
    "image/tiff": ".tiff",
}

EXT_TO_PIL_FORMAT = {
    ".png": "PNG",
    ".jpg": "JPEG",
    ".jpeg": "JPEG",
    ".webp": "WEBP",
    ".gif": "GIF",
    ".bmp": "BMP",
    ".tiff": "TIFF",
    ".tif": "TIFF",
}


def detect_image_extension(image_bytes: bytes, content_type: str = None) -> str | None:
    """Best-effort detection of the real image format."""
    if image_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if image_bytes.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if image_bytes.startswith(b"GIF87a") or image_bytes.startswith(b"GIF89a"):
        return ".gif"
    if image_bytes.startswith(b"RIFF") and image_bytes[8:12] == b"WEBP":
        return ".webp"
    if image_bytes.startswith(b"BM"):
        return ".bmp"
    if image_bytes.startswith((b"II*\x00", b"MM\x00*")):
        return ".tiff"
    if content_type:
        clean_type = content_type.split(";", 1)[0].strip().lower()
        if clean_type in CONTENT_TYPE_TO_EXT:
            return CONTENT_TYPE_TO_EXT[clean_type]
    return None


def _normalize_extension(ext: str) -> str:
    """Normalize equivalent image extensions to a canonical form."""
    ext = ext.lower()
    if ext == ".jpeg":
        return ".jpg"
    if ext == ".tif":
        return ".tiff"
    return ext


def report_resolution(path: str) -> None:
    """Try to report image resolution using PIL."""
    if HAS_PIL:
        try:
            img = PILImage.open(path)
            print(f"  Resolution:   {img.size[0]}x{img.size[1]}")
        except Exception:
            pass


def save_image_bytes(image_bytes: bytes, path: str, content_type: str = None) -> str:
    """
    Save image bytes to disk while keeping the file extension and the real bytes aligned.

    If the target extension differs from the actual bytes, transcode through Pillow when
    available. Otherwise fail loudly instead of writing a misleading file.
    """
    target_ext = _normalize_extension(os.path.splitext(path)[1])
    actual_ext = _normalize_extension(detect_image_extension(image_bytes, content_type) or "")

    if not target_ext:
        raise ValueError(f"Output path must include an image extension: {path}")

    if actual_ext and target_ext == actual_ext:
        with open(path, "wb") as f:
            f.write(image_bytes)
        print(f"  File saved to: {path}")
        report_resolution(path)
        return path

    if not HAS_PIL:
        actual_label = actual_ext or "unknown"
        raise RuntimeError(
            f"Image format mismatch for {path}: target extension is {target_ext}, "
            f"but the actual image bytes are {actual_label}. "
            "Install Pillow to enable automatic format conversion."
        )

    target_format = EXT_TO_PIL_FORMAT.get(target_ext)
    if not target_format:
        raise ValueError(f"Unsupported output image extension: {target_ext}")

    with PILImage.open(io.BytesIO(image_bytes)) as source:
        image = PILImageOps.exif_transpose(source)
        try:
            if target_format == "JPEG":
                has_alpha = (
                    image.mode in ("RGBA", "LA")
                    or "transparency" in getattr(image, "info", {})
                )
                if has_alpha:
                    rgba = image.convert("RGBA")
                    alpha = rgba.getchannel("A")
                    rgb = rgba.convert("RGB")
                    converted = PILImage.new("RGB", image.size, (255, 255, 255))
                    converted.paste(rgb, mask=alpha)
                    rgb.close()
                    alpha.close()
                    rgba.close()
                    if image is not source:
                        image.close()
                    image = converted
                elif image.mode != "RGB":
                    converted = image.convert("RGB")
                    if image is not source:
                        image.close()
                    image = converted
            image.save(path, format=target_format)
        finally:
            if image is not source:
                image.close()

    if actual_ext and actual_ext != target_ext:
        print(f"  Converted:    {actual_ext} -> {target_ext}")
    print(f"  File saved to: {path}")
    report_resolution(path)
    return path


def download_image(url: str, path: str, headers: dict = None, timeout: int = 180) -> str:
    """Download an image URL and save it to disk."""
    try:
        response = requests.get(url, headers=headers or {}, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise _RetryableBackendError(f"Image download failed: {exc}") from exc
    return save_image_bytes(
        response.content,
        path,
        content_type=response.headers.get("Content-Type"),
    )
