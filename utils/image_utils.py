def check_aspect_ratio(image, target_ratio: float = 16/9, tolerance: float = 0.05) -> tuple:
    """
    Determines if the provided image adheres to the specified aspect ratio within an acceptable tolerance.
    """
    width, height = image.size

    try:
        actual_ratio = width / height
    except ZeroDivisionError:
        return False, width, height

    is_valid = abs(actual_ratio - target_ratio) <= tolerance

    return is_valid, width, height
