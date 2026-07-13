from app.core.logging import logger

def optimize_image_dimensions(width: int, height: int, max_size: int = 1920) -> tuple[int, int]:
    if width <= max_size and height <= max_size:
        return width, height
    if width > height:
        ratio = max_size / width
        return max_size, int(height * ratio)
    else:
        ratio = max_size / height
        return int(width * ratio), max_size

def watermark_image(image_path: str) -> None:
    logger.info(f"Watermarking image file at: {image_path}")
