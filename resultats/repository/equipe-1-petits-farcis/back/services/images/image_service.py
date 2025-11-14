"""
Image processing service for handling puzzle images with tile-based reveal system.
Uses Pillow for image manipulation and base64 for encoding/decoding.
"""
import base64
import io
import os
import re
from typing import List, Tuple, Union
from PIL import Image, ImageDraw
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Data directory for storing images - go up two levels from services/images to app root
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
IMAGES_DIR = os.path.join(DATA_DIR, 'images')



def ensure_images_directory():
    """Ensure the images directory exists."""
    os.makedirs(IMAGES_DIR, exist_ok=True)
    logger.info(f"Images directory: {IMAGES_DIR}")


def decode_base64_image(image_b64: str) -> Image.Image:
    """
    Convert base64 string to Pillow Image object.
    
    Args:
        image_b64: Base64 encoded image string (with or without data URI prefix)
        
    Returns:
        Pillow Image object
        
    Raises:
        ValueError: If image cannot be decoded
    """
    try:
        # Remove data URI prefix if present
        if image_b64.startswith('data:image'):
            image_b64 = re.sub(r'^data:image\/[^;]+;base64,', '', image_b64)
        
        # Decode base64 to bytes
        image_bytes = base64.b64decode(image_b64)
        
        # Create Image from bytes
        image = Image.open(io.BytesIO(image_bytes))
        logger.info(f"Decoded image: {image.size}, mode: {image.mode}")
        return image
        
    except Exception as e:
        logger.error(f"Error decoding base64 image: {e}")
        raise ValueError(f"Invalid base64 image data: {e}")


def encode_image_to_base64(image: Image.Image, format: str = 'PNG') -> str:
    """
    Convert Pillow Image object to base64 string with data URI prefix.
    
    Args:
        image: Pillow Image object
        format: Image format (PNG, JPEG, etc.)
        
    Returns:
        Base64 encoded image string with data URI prefix
    """
    try:
        # Save image to bytes buffer
        buffer = io.BytesIO()
        image.save(buffer, format=format)
        buffer.seek(0)
        
        # Encode to base64
        image_b64 = base64.b64encode(buffer.read()).decode('utf-8')
        
        # Add data URI prefix
        mime_type = f"image/{format.lower()}"
        data_uri = f"data:{mime_type};base64,{image_b64}"
        
        logger.info(f"Encoded image to base64: {len(data_uri)} chars")
        return data_uri
        
    except Exception as e:
        logger.error(f"Error encoding image to base64: {e}")
        raise ValueError(f"Failed to encode image: {e}")


def load_image_from_file(filename: str) -> Image.Image:
    """
    Load an image from the data/images directory.
    
    Args:
        filename: Name of the image file (e.g., 'puzzle_image.jpg')
        
    Returns:
        Pillow Image object
        
    Raises:
        ValueError: If image file cannot be loaded
    """
    ensure_images_directory()
    
    try:
        # Construct full path
        image_path = os.path.join(IMAGES_DIR, filename)
        
        if not os.path.exists(image_path):
            raise ValueError(f"Image file not found: {filename}")
        
        # Load image
        image = Image.open(image_path)
        logger.info(f"Loaded image from file: {filename} ({image.size})")
        return image
        
    except Exception as e:
        logger.error(f"Error loading image from file '{filename}': {e}")
        raise ValueError(f"Failed to load image file: {e}")


def load_image(image_source: str) -> Image.Image:
    """
    Load an image from either a base64 string or a file path.
    Automatically detects the source type.
    
    Args:
        image_source: Either a base64 string (with data URI) or a filename
        
    Returns:
        Pillow Image object
        
    Raises:
        ValueError: If image cannot be loaded
    """
    # Check if it's a base64 string
    if image_source.startswith('data:image'):
        return decode_base64_image(image_source)
    
    # Check if it looks like base64 without prefix
    try:
        if len(image_source) > 100 and '/' not in image_source and '\\' not in image_source:
            return decode_base64_image(image_source)
    except:
        pass
    
    # Treat as filename
    return load_image_from_file(image_source)


def parse_tile_coordinate(tile_str: str) -> Tuple[int, int]:
    """
    Parse tile coordinate string to row, col tuple.
    
    Args:
        tile_str: Tile coordinate in format "row_col" (e.g., "0_0", "2_3")
        
    Returns:
        Tuple of (row, col)
        
    Raises:
        ValueError: If tile format is invalid
    """
    try:
        parts = tile_str.split('_')
        if len(parts) != 2:
            raise ValueError(f"Invalid tile format: {tile_str}")
        return int(parts[0]), int(parts[1])
    except Exception as e:
        logger.error(f"Error parsing tile coordinate '{tile_str}': {e}")
        raise ValueError(f"Invalid tile coordinate: {tile_str}")


def generate_revealed_image(image_source: str, unlocked_tiles: List[str], 
                           grid_size: int) -> Tuple[Image.Image, int]:
    """
    Generate an image with revealed tiles and black boxes over unrevealed tiles.
    
    Args:
        image_source: Base64 encoded image string OR filename in data/images/ directory
        unlocked_tiles: List of unlocked tile coordinates (e.g., ["0_0", "0_1", "1_2"])
        grid_size: Size of the grid (e.g., 4 for 4x4 grid, 10 for 10x10 grid)
        
    Returns:
        Tuple of (revealed Image object, total number of tiles)
        
    Raises:
        ValueError: If image processing fails
    """
    try:
        # Load the original image (from base64 or file)
        original_image = load_image(image_source)
        
        # Convert to RGB if necessary
        if original_image.mode != 'RGB':
            original_image = original_image.convert('RGB')
        
        # Create a copy to work with
        revealed_image = original_image.copy()
        draw = ImageDraw.Draw(revealed_image)
        
        # Calculate tile dimensions
        img_width, img_height = original_image.size
        tile_width = img_width // grid_size
        tile_height = img_height // grid_size
        
        # Convert unlocked tiles to set of tuples for fast lookup
        unlocked_set = set()
        for tile in unlocked_tiles:
            try:
                unlocked_set.add(parse_tile_coordinate(tile))
            except ValueError as e:
                logger.warning(f"Skipping invalid tile: {e}")
        
        # Draw black boxes over locked tiles
        locked_count = 0
        for row in range(grid_size):
            for col in range(grid_size):
                if (row, col) not in unlocked_set:
                    # Calculate tile boundaries
                    x1 = col * tile_width
                    y1 = row * tile_height
                    x2 = x1 + tile_width
                    y2 = y1 + tile_height
                    
                    # Draw black rectangle
                    draw.rectangle([x1, y1, x2, y2], fill='black')
                    locked_count += 1
        
        total_tiles = grid_size * grid_size
        revealed_tiles = len(unlocked_set)
        
        logger.info(f"Generated revealed image: {revealed_tiles}/{total_tiles} tiles revealed")
        return revealed_image, total_tiles
        
    except Exception as e:
        logger.error(f"Error generating revealed image: {e}")
        raise ValueError(f"Failed to generate revealed image: {e}")


def generate_image_with_hidden_tiles(image_source: str, unrevealed_tiles: List[str],
                                    grid_size: int) -> Tuple[Image.Image, int, int]:
    """
    Generate an image with black boxes over specified unrevealed tiles.
    This is the inverse of generate_revealed_image - it hides specific tiles.
    
    Args:
        image_source: Base64 encoded image string OR filename in data/images/ directory
        unrevealed_tiles: List of tile coordinates to hide (e.g., ["2_2", "3_3"])
        grid_size: Size of the grid (e.g., 4 for 4x4 grid, 10 for 10x10 grid)
        
    Returns:
        Tuple of (revealed Image object, total tiles, revealed tiles count)
        
    Raises:
        ValueError: If image processing fails
    """
    try:
        # Load the original image (from base64 or file)
        original_image = load_image(image_source)
        
        # Convert to RGBA to support transparency
        if original_image.mode != 'RGBA':
            original_image = original_image.convert('RGBA')
        
        # Create a copy to work with
        revealed_image = original_image.copy()
        
        # Load the lock icon
        lock_icon_path = os.path.join(IMAGES_DIR, 'lock.png')
        if not os.path.exists(lock_icon_path):
            raise ValueError("Lock icon not found at: " + lock_icon_path)
        
        lock_icon = Image.open(lock_icon_path).convert('RGBA')
        
        # Load the user logo for revealed tiles
        user_logo_path = os.path.join(IMAGES_DIR, 'user_1.png')
        if not os.path.exists(user_logo_path):
            raise ValueError("User logo not found at: " + user_logo_path)
        
        user_logo = Image.open(user_logo_path).convert('RGBA')
        
        # Calculate tile dimensions
        img_width, img_height = original_image.size
        tile_width = img_width // grid_size
        tile_height = img_height // grid_size
        
        # Convert unrevealed tiles to set of tuples
        unrevealed_set = set()
        for tile in unrevealed_tiles:
            try:
                unrevealed_set.add(parse_tile_coordinate(tile))
            except ValueError as e:
                logger.warning(f"Skipping invalid tile: {e}")
        
        total_tiles = grid_size * grid_size
        revealed_tiles = total_tiles - len(unrevealed_set)
        
        # If all tiles are revealed, return the original image without grid or logos
        if len(unrevealed_set) == 0:
            logger.info(f"All tiles revealed: returning full original image without grid or logos")
            return original_image.convert('RGB'), total_tiles, revealed_tiles
        
        # Create an overlay layer for locked tiles
        overlay = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # Process each unrevealed tile
        for row, col in unrevealed_set:
            # Calculate tile boundaries
            x1 = col * tile_width
            y1 = row * tile_height
            x2 = x1 + tile_width
            y2 = y1 + tile_height
            
            # Draw solid dark gray overlay (completely opaque)
            overlay_draw.rectangle([x1, y1, x2, y2], fill=(180, 185, 195, 255))
            
            # Resize and place lock icon in the center of the tile
            lock_size = min(tile_width, tile_height) // 2  # Lock icon is half the tile size
            resized_lock = lock_icon.resize((lock_size, lock_size), Image.LANCZOS)
            
            # Calculate center position for the lock
            lock_x = x1 + (tile_width - lock_size) // 2
            lock_y = y1 + (tile_height - lock_size) // 2
            
            # Paste the lock icon onto the overlay
            overlay.paste(resized_lock, (lock_x, lock_y), resized_lock)
        
        # Composite the overlay onto the original image
        revealed_image = Image.alpha_composite(revealed_image, overlay)
        
        # Convert back to RGB for final output
        revealed_image = revealed_image.convert('RGB')
        
        # Draw white grid lines to show tile boundaries
        grid_draw = ImageDraw.Draw(revealed_image)
        grid_line_width = 2  # Width of grid lines
        
        # Draw vertical lines
        for col in range(1, grid_size):
            x = col * tile_width
            grid_draw.line([(x, 0), (x, img_height)], fill='white', width=grid_line_width)
        
        # Draw horizontal lines
        for row in range(1, grid_size):
            y = row * tile_height
            grid_draw.line([(0, y), (img_width, y)], fill='white', width=grid_line_width)
        
        # Add user logo to revealed tiles (bottom right corner)
        user_logo_size = min(tile_width, tile_height) // 2  # Logo is 1/2 of tile size
        resized_user_logo = user_logo.resize((user_logo_size, user_logo_size), Image.LANCZOS)
        
        # Make the user logo slightly transparent
        alpha = resized_user_logo.split()[3]  # Get alpha channel
        alpha = alpha.point(lambda p: int(p * 0.9))  # 70% opacity
        resized_user_logo.putalpha(alpha)
        
        # Create overlay for user logos on revealed tiles
        user_logo_overlay = Image.new('RGBA', (img_width, img_height))
        
        # Place user logo on each revealed tile
        for row in range(grid_size):
            for col in range(grid_size):
                if (row, col) not in unrevealed_set:  # This is a revealed tile
                    # Calculate tile boundaries
                    x1 = col * tile_width
                    y1 = row * tile_height
                    
                    # Position logo at bottom right of tile with small padding
                    logo_x = x1 + tile_width - user_logo_size - 5
                    logo_y = y1 + tile_height - user_logo_size - 5
                    
                    # Paste the user logo
                    user_logo_overlay.paste(resized_user_logo, (logo_x, logo_y), resized_user_logo)
        
        # Convert revealed_image back to RGBA to composite the user logos
        revealed_image = revealed_image.convert('RGBA')
        revealed_image = Image.alpha_composite(revealed_image, user_logo_overlay)
        revealed_image = revealed_image.convert('RGB')
        
        logger.info(f"Generated image with locked tiles: {revealed_tiles}/{total_tiles} tiles revealed, {len(unrevealed_set)} locked")
        return revealed_image, total_tiles, revealed_tiles
        
    except Exception as e:
        logger.error(f"Error generating image with hidden tiles: {e}")
        raise ValueError(f"Failed to generate image with hidden tiles: {e}")


def create_revealed_image_from_puzzle(image_source: str, unrevealed_tiles: List[str],
                                     grid_size: int) -> dict:
    """
    High-level function to create a revealed image and return response data.
    Uses unrevealed_tiles to determine which tiles should be hidden with black boxes.
    
    Args:
        image_source: Base64 encoded image string OR filename in data/images/ directory
        unrevealed_tiles: List of tile coordinates to hide (e.g., ["2_2", "3_3"])
        grid_size: Size of the grid (e.g., 4 for 4x4 grid, 10 for 10x10 grid)
        
    Returns:
        Dictionary with revealed_image_b64
        
    Raises:
        ValueError: If image processing fails
    """
    revealed_image, total_tiles, revealed_count = generate_image_with_hidden_tiles(
        image_source, unrevealed_tiles, grid_size
    )
    revealed_image_b64 = encode_image_to_base64(revealed_image)
    
    return {
        'revealed_image_b64': revealed_image_b64,
        'total_tiles': total_tiles,
        'revealed_tiles': revealed_count
    }

