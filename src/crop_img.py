"""
crop_img.py
-----------
Detects the face in every image inside `images/`, crops it (with padding),
resizes to 216x216, and saves the result to `images/cropped/`.

Uses the same `face_recognition` library already used in this project.

Usage:
    python crop_img.py
"""

import os
from pathlib import Path

import cv2
import face_recognition
from PIL import Image

# ── Configuration ─────────────────────────────────────────────────────────────
INPUT_DIR    = Path("images")
OUTPUT_DIR   = Path("images") / "cropped"
TARGET_SIZE  = (216, 216)
PADDING      = 0.2          # extra margin around the detected face (fraction of face size)
SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff"}
# ──────────────────────────────────────────────────────────────────────────────


def crop_face(img_bgr, padding: float = PADDING):
    """
    Detect the first face in *img_bgr* (BGR numpy array),
    add *padding* around it, and return the cropped BGR region.
    Returns None if no face is found.
    """
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(img_rgb)

    if not face_locations:
        return None

    # face_recognition returns (top, right, bottom, left)
    top, right, bottom, left = face_locations[0]

    h, w = img_bgr.shape[:2]
    face_h = bottom - top
    face_w = right  - left

    pad_h = int(face_h * padding)
    pad_w = int(face_w * padding)

    top    = max(0, top    - pad_h)
    bottom = min(h, bottom + pad_h)
    left   = max(0, left   - pad_w)
    right  = min(w, right  + pad_w)

    return img_bgr[top:bottom, left:right]


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    image_paths = [
        p for p in INPUT_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTS
    ]

    if not image_paths:
        print(f"No supported images found in '{INPUT_DIR}'.")
        return

    print(f"Found {len(image_paths)} image(s). Detecting & cropping faces to {TARGET_SIZE[0]}x{TARGET_SIZE[1]}...")

    ok_count  = 0
    err_count = 0

    for img_path in sorted(image_paths):
        img_bgr = cv2.imread(str(img_path))
        if img_bgr is None:
            print(f"  [ERR] {img_path.name} - could not read file")
            err_count += 1
            continue

        face_crop = crop_face(img_bgr)

        if face_crop is None:
            print(f"  [SKIP] {img_path.name} - no face detected")
            err_count += 1
            continue

        # Resize cropped face to target size
        face_resized = cv2.resize(face_crop, TARGET_SIZE, interpolation=cv2.INTER_LANCZOS4)

        out_path = OUTPUT_DIR / img_path.name
        cv2.imwrite(str(out_path), face_resized)
        print(f"  [OK]  {img_path.name}  ->  {out_path}  ({TARGET_SIZE[0]}x{TARGET_SIZE[1]})")
        ok_count += 1

    print(f"\nDone! {ok_count} saved, {err_count} skipped/failed. Output: '{OUTPUT_DIR}'")


if __name__ == "__main__":
    main()
