"""Pad azimuth/profile PNGs to minimum 4:3; default is read-only."""
import argparse
import hashlib
import os
from pathlib import Path
import shutil
import tempfile

from PIL import Image

IGNORED = {".git", "__pycache__", "output", "outputs", "staging"}


def discover(root):
    files = []
    for directory, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = sorted(name for name in dirs
                         if name.lower() not in IGNORED
                         and "soil" not in name.lower()
                         and not name.lower().endswith(("-staging", "_staging"))
                         and not (Path(directory) / name).is_symlink())
        folder = Path(directory)
        if not {"azimuth", "profile"}.intersection(p.lower() for p in folder.relative_to(root).parts):
            continue
        files.extend(folder / name for name in names
                     if Path(name).suffix.lower() == ".png" and "soil" not in name.lower()
                     and not (folder / name).is_symlink())
    return sorted(files)


def pixels(path):
    with Image.open(path) as image:
        if image.format != "PNG" or getattr(image, "n_frames", 1) != 1:
            raise ValueError("Expected a single-frame PNG")
        if image.mode not in {"1", "L", "LA", "P", "RGB", "RGBA"}:
            raise ValueError(f"Unsupported pixel mode: {image.mode}")
        return image.convert("RGBA")


def padded(original):
    k = max((original.width + 3) // 4, (original.height + 2) // 3)
    canvas = Image.new("RGBA", (4 * k, 3 * k), "white")
    offset = ((canvas.width - original.width) // 2,
              (canvas.height - original.height) // 2)
    canvas.paste(original, offset)  # No mask: preserve alpha and all RGB values.
    return canvas


def validate(target, expected):
    actual = pixels(target)
    if actual.size != expected.size or actual.width * 3 != actual.height * 4:
        raise ValueError("Output dimensions do not match the minimum 4:3 canvas")
    if actual.tobytes() != expected.tobytes():
        raise ValueError("Original pixels or white padding differ")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output", type=Path, help="Separate staging directory")
    parser.add_argument("--expect", type=int, help="Optional expected image count")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Preview only (default)")
    mode.add_argument("--in-place", action="store_true", help="Explicitly allow replacing originals")
    mode.add_argument("--write", action="store_true", help="Create missing staged files only")
    mode.add_argument("--validate", action="store_true", help="Validate staged files against source")
    args = parser.parse_args()
    source = args.source.resolve()
    output = args.output.resolve() if args.output else None
    if not source.is_dir():
        parser.error("Source directory does not exist")
    if args.in_place and output:
        parser.error("--in-place cannot be combined with --output")
    if (args.write or args.validate) and output is None:
        parser.error("--write and --validate require --output")
    if output and (source == output or source in output.parents or output in source.parents):
        parser.error("Staging and source must be separate, non-nested directories")
    files = discover(source)
    if not files or (args.expect is not None and len(files) != args.expect):
        parser.error(f"Found {len(files)} images; expected {args.expect}")
    changed = skipped = failures = 0
    for path in files:
        try:
            original = pixels(path)
            expected = padded(original)
            relative = path.relative_to(source)
            target = output / relative if output else path
            if args.validate or (output and target.exists()):
                validate(target, expected)
                skipped += 1
                action = "VALID"
            elif not output and original.width * 3 == original.height * 4:
                skipped += 1
                action = "SKIP already 4:3"
            elif args.in_place:
                # Validate outside the repository before replacing the original.
                before = hashlib.sha256(path.read_bytes()).digest()
                with tempfile.TemporaryDirectory(prefix="image-4x3-") as temporary:
                    candidate = Path(temporary) / path.name
                    expected.save(candidate, format="PNG", icc_profile=original.info.get("icc_profile"))
                    validate(candidate, expected)
                    if hashlib.sha256(path.read_bytes()).digest() != before:
                        raise ValueError("Source changed during processing")
                    shutil.copyfile(candidate, path)
                validate(path, expected)
                changed += 1
                action = "UPDATED"
            elif args.write:
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open("xb") as stream:
                    expected.save(stream, format="PNG", icc_profile=original.info.get("icc_profile"))
                validate(target, expected)
                changed += 1
                action = "CREATED"
            else:
                action = "WOULD PAD" if not output else "WOULD CREATE"
            print(f"{action} {relative}: {original.size} -> {expected.size}", flush=True)
        except Exception as error:
            failures += 1
            print(f"FAIL {path.relative_to(source)}: {error}", flush=True)
    print(f"Images: {len(files)}; changed: {changed}; skipped/valid: {skipped}; failures: {failures}")
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
