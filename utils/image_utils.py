from PIL.Image import Image

# Standard YouTube aspect ratio (16:9)
IDEAL_ASPECT_RATIO = 16 / 9
TOLERANCE = 0.05  # ~5% margin


def check_aspect_ratio(image: Image) -> tuple:
    width, height = image.size
    aspect_ratio = width / height
    is_valid = abs(aspect_ratio - IDEAL_ASPECT_RATIO) <= TOLERANCE
    return is_valid, width, height
