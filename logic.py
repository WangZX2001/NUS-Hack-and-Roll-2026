import argparse
from pathlib import Path
from typing import Iterator, List, Tuple

import torch
from PIL import Image
from torchvision import transforms

# Labels and their Arduino command codes.
CLASSES = ["paper", "metal", "plastic", "others"]
LABEL_TO_CMD = {"paper": "P", "metal": "M", "plastic": "L", "others": "O"}

# Image preprocessing (must mirror training pipeline).
TRANSFORM = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)


def iter_images(path: Path) -> Iterator[Path]:
    """Yield valid image files beneath a path."""
    valid_suffixes = {".jpg", ".jpeg", ".png", ".bmp"}
    if path.is_file():
        if path.suffix.lower() in valid_suffixes:
            yield path
        return

    for entry in sorted(path.iterdir()):
        if entry.is_file() and entry.suffix.lower() in valid_suffixes:
            yield entry


def classify_image(model: torch.nn.Module, image_path: Path, device: torch.device) -> Tuple[str, float]:
    """Load an image, run it through the model, and return (label, confidence)."""
    img = Image.open(image_path).convert("RGB")
    img_tensor = TRANSFORM(img).unsqueeze(0).to(device)

    with torch.no_grad():
        logits = model(img_tensor)
        probs = torch.nn.functional.softmax(logits[0], dim=0)

    confidence, pred_idx = torch.max(probs, dim=0)
    return CLASSES[pred_idx.item()], float(confidence.item())


def label_to_command(label: str) -> str:
    """Convert a label into the Arduino command character."""
    return LABEL_TO_CMD.get(label, LABEL_TO_CMD["others"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Classify one image or a folder of images.")
    parser.add_argument("--path", type=Path, required=True, help="Image file or directory.")
    parser.add_argument("--weights", type=str, default="trash_classifier.pth", help="Path to model weights.")
    parser.add_argument("--cpu", action="store_true", help="Force CPU even if CUDA is available.")
    args = parser.parse_args()

    from model import load_trash_model

    device = torch.device("cpu" if args.cpu or not torch.cuda.is_available() else "cuda")
    model = load_trash_model(args.weights).to(device)

    images: List[Path] = list(iter_images(args.path))
    if not images:
        raise SystemExit(f"No images found under {args.path}")

    for image_path in images:
        label, confidence = classify_image(model, image_path, device)
        cmd = label_to_command(label)
        print(f"{image_path}: {label} ({confidence:.2f}) -> cmd {cmd}")


if __name__ == "__main__":
    main()
