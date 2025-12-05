"""
Image Utilities Module
Handles image loading and placeholder generation
"""

from PIL import Image, ImageDraw, ImageFont
import os


def create_placeholder_image(name, size=(300, 300), color=(100, 150, 200)):
    """
    Create a placeholder image when the actual image is not available.
    
    Args:
        name: Astrologer's name for the placeholder
        size: Image size (width, height)
        color: Background color (RGB tuple)
    
    Returns:
        PIL Image object
    """
    img = Image.new('RGB', size, color=color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font, fallback to default if not available
    try:
        font = ImageFont.truetype("sans serif.ttf", 30)
        small_font = ImageFont.truetype("sans serif.ttf", 16)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw text in the center
    text = name.split()[0]  # Use first name only
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    draw.text((x, y), text, fill=(255, 255, 255), font=font)
    
    # Add "Astrologer" label
    label_bbox = draw.textbbox((0, 0), "Astrologer", font=small_font)
    label_width = label_bbox[2] - label_bbox[0]
    label_x = (size[0] - label_width) // 2
    
    draw.text((label_x, y + text_height + 20), "Astrologer", fill=(200, 200, 200), font=small_font)
    
    return img


def load_image(image_path, size=(300, 300)):
    """
    Load an image from file, or create a placeholder if not found.
    
    Args:
        image_path: Path to the image file
        size: Desired image size (width, height)
    
    Returns:
        PIL Image object
    """
    try:
        if os.path.exists(image_path):
            img = Image.open(image_path)
            img = img.resize(size, Image.Resampling.LANCZOS)
            return img
        else:
            # Extract name from path for placeholder
            name = os.path.splitext(os.path.basename(image_path))[0]
            return create_placeholder_image(name, size)
    except Exception as e:
        print(f"Error loading image {image_path}: {str(e)}")
        return create_placeholder_image("Unknown", size)
