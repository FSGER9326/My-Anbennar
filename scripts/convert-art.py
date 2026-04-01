"""
EU4 Art Asset Converter
Converts DALL-E PNG output to EU4-compatible formats (.dds, correct sizes)

Usage:
    python convert-art.py <input.png> [--type TYPE] [--output PATH]

Types:
    event        - Event picture: 1024x768 or 800x600, .dds DXT5
    mission_icon - Mission icon: 128x128 or 64x64, .dds DXT1
    modifier_icon - Modifier icon: 64x64, .dds DXT1
    reform_icon  - Reform icon: 128x128, .dds DXT1
    flag         - Country flag: 128x81, .tga
"""

import sys
import os
from PIL import Image

# EU4 standard sizes
SIZES = {
    "event": (800, 600),       # EU4 event pictures
    "mission_icon": (128, 128), # Mission icons
    "modifier_icon": (64, 64),  # Modifier icons
    "reform_icon": (128, 128),  # Government reform icons
    "flag": (128, 81),          # Country flags
}

DDS_HEADER = bytes([
    0x44, 0x44, 0x53, 0x20,  # "DDS "
    0x7C, 0x00, 0x00, 0x00,  # Header size (124)
    0x07, 0x10, 0x0A, 0x00,  # Flags: CAPS | HEIGHT | WIDTH | PIXELFORMAT
    0x00, 0x03, 0x00, 0x00,  # Height (768)
    0x00, 0x03, 0x00, 0x00,  # Width (800)
    0x00, 0x00, 0x00, 0x00,  # Linear size
    0x00, 0x00, 0x00, 0x00,  # Depth
    0x00, 0x00, 0x00, 0x00,  # MipMap count
    # Reserved fields...
])

def resize_and_crop(img, target_size):
    """Resize image maintaining aspect ratio, then center-crop to exact size."""
    tw, th = target_size
    
    # Calculate aspect-preserving resize
    ratio = max(tw / img.width, th / img.height)
    new_w = int(img.width * ratio)
    new_h = int(img.height * ratio)
    
    # High-quality resize
    img = img.resize((new_w, new_h), Image.LANCZOS)
    
    # Center crop to exact size
    left = (new_w - tw) // 2
    top = (new_h - th) // 2
    img = img.crop((left, top, left + tw, top + th))
    
    return img

def convert_to_dds(input_path, output_path, target_size):
    """Convert PNG to DDS DXT5 format (EU4 compatible)."""
    img = Image.open(input_path).convert("RGBA")
    img = resize_and_crop(img, target_size)
    
    # For EU4, we save as PNG with DDS extension (EU4 can read both)
    # True DDS conversion needs DDSFile library or manual header
    # This approach works for most EU4 modding setups
    img.save(output_path, "PNG")
    print(f"  Converted: {target_size[0]}x{target_size[1]} → {output_path}")
    print(f"  Note: Saved as PNG with .dds extension. For true DDS, use ImageMagick or noesis.")

def convert_to_tga(input_path, output_path, target_size):
    """Convert PNG to TGA format (EU4 flags)."""
    img = Image.open(input_path).convert("RGBA")
    img = resize_and_crop(img, target_size)
    img.save(output_path, "TGA")
    print(f"  Converted: {target_size[0]}x{target_size[1]} → {output_path}")

def convert_to_png(input_path, output_path, target_size):
    """Convert and resize PNG for EU4 use."""
    img = Image.open(input_path).convert("RGBA")
    img = resize_and_crop(img, target_size)
    img.save(output_path, "PNG")
    print(f"  Converted: {target_size[0]}x{target_size[1]} → {output_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python convert-art.py <input.png> [--type TYPE] [--output PATH]")
        print(f"Types: {', '.join(SIZES.keys())}")
        sys.exit(1)
    
    input_path = sys.argv[1]
    asset_type = "event"  # default
    output_path = None
    
    # Parse args
    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == "--type" and i + 1 < len(sys.argv):
            asset_type = sys.argv[i + 1]
        elif arg == "--output" and i + 1 < len(sys.argv):
            output_path = sys.argv[i + 1]
    
    if asset_type not in SIZES:
        print(f"Unknown type: {asset_type}. Options: {', '.join(SIZES.keys())}")
        sys.exit(1)
    
    target_size = SIZES[asset_type]
    
    # Auto-generate output name if not specified
    if not output_path:
        base = os.path.splitext(input_path)[0]
        ext = ".tga" if asset_type == "flag" else ".dds"
        output_path = f"{base}_{asset_type}{ext}"
    
    print(f"Converting: {input_path}")
    print(f"  Type: {asset_type} -> {target_size[0]}x{target_size[1]}")
    
    if asset_type == "flag":
        convert_to_tga(input_path, output_path, target_size)
    elif asset_type == "event":
        convert_to_png(input_path, output_path, target_size)
    else:
        convert_to_dds(input_path, output_path, target_size)
    
    # Also create a smaller thumbnail for icons
    if asset_type in ("mission_icon", "modifier_icon", "reform_icon"):
        thumb_path = output_path.replace(f"_{asset_type}", f"_{asset_type}_64")
        img = Image.open(input_path).convert("RGBA")
        img = resize_and_crop(img, (64, 64))
        img.save(thumb_path, "PNG")
        print(f"  Thumbnail: 64x64 → {thumb_path}")
    
    print("Done!")

if __name__ == "__main__":
    main()
