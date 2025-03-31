# Checks if the uploaded image has 16:9 ratio
def check_aspect_ratio(image):
    """
    Checks if image has a 16:9 aspect ratio with ~5% tolerance
    """
    width, height = image.size
    aspect_ratio = width / height
    is_valid = abs(aspect_ratio - (16 / 9)) <= 0.05
    return is_valid, width, height
