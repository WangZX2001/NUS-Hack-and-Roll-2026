import torch
from torchvision import models

def load_trash_model(weights_path: str = None):
    """Load the trash classification CNN model (MobileNetV2) with 4 output classes.
    If weights_path is provided, load the trained weights from that file."""
    # Initialize MobileNetV2 architecture, pretrained on ImageNet
    model = models.mobilenet_v2(weights=None)  # not loading ImageNet weights directly
    # Replace the classifier's final layer to output 4 classes instead of 1000
    model.classifier[1] = torch.nn.Linear(model.last_channel, 4)
    # Load trained weights if available
    if weights_path:
        model.load_state_dict(torch.load(weights_path, map_location='cpu'))
    # Set model to evaluation mode (disable dropout, batchnorm updates, etc.)
    model.eval()
    return model

# If this module is run directly, load the model (assuming weights file is in the working directory)
if __name__ == "__main__":
    model = load_trash_model("trash_classifier.pth")
    print("Model loaded and ready for inference.")
