def check_aspect_ratio(image, target_ratio: float = 16/9, tolerance: float = 0.05) -> tuple:
    width, height = image.size

    if height == 0:
        return False, width, height

    actual_ratio = width / height
    is_valid = abs(actual_ratio - target_ratio) <= tolerance

    return is_valid, width, height