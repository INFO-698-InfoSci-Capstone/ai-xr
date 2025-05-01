import os
import requests
from PIL import Image
from io import BytesIO

# Base URLs for different texture types
TEXTURE_URLS = {
    'wood': [
        ('oak', 'https://raw.githubusercontent.com/textures/wood-textures/main/oak.jpg'),
        ('walnut', 'https://raw.githubusercontent.com/textures/wood-textures/main/walnut.jpg'),
    ],
    'fabric': [
        ('velvet_blue', 'https://raw.githubusercontent.com/textures/fabric-textures/main/velvet_blue.jpg'),
        ('linen_gray', 'https://raw.githubusercontent.com/textures/fabric-textures/main/linen_gray.jpg'),
        ('cotton_beige', 'https://raw.githubusercontent.com/textures/fabric-textures/main/cotton_beige.jpg'),
    ],
    'leather': [
        ('leather_brown', 'https://raw.githubusercontent.com/textures/leather-textures/main/brown.jpg'),
        ('leather_black', 'https://raw.githubusercontent.com/textures/leather-textures/main/black.jpg'),
    ],
    'metal': [
        ('metal_steel', 'https://raw.githubusercontent.com/textures/metal-textures/main/steel.jpg'),
        ('metal_brass', 'https://raw.githubusercontent.com/textures/metal-textures/main/brass.jpg'),
    ],
    'glass': [
        ('glass_clear', 'https://raw.githubusercontent.com/textures/glass-textures/main/clear.jpg'),
        ('glass_frosted', 'https://raw.githubusercontent.com/textures/glass-textures/main/frosted.jpg'),
    ],
    'stone': [
        ('stone_marble', 'https://raw.githubusercontent.com/textures/stone-textures/main/marble.jpg'),
        ('stone_granite', 'https://raw.githubusercontent.com/textures/stone-textures/main/granite.jpg'),
    ],
}

def create_thumbnail(image, size=(200, 200)):
    """Create a thumbnail from an image while maintaining aspect ratio"""
    thumbnail = image.copy()
    thumbnail.thumbnail(size)
    return thumbnail

def download_and_save_textures():
    base_dir = '../project-bolt-sb1-uelpyywt/project/public/textures'
    
    for category, textures in TEXTURE_URLS.items():
        # Create category directories if they don't exist
        full_dir = os.path.join(base_dir, category, 'full')
        thumb_dir = os.path.join(base_dir, category, 'thumbnails')
        os.makedirs(full_dir, exist_ok=True)
        os.makedirs(thumb_dir, exist_ok=True)
        
        for texture_name, url in textures:
            try:
                # For demonstration, we'll create a colored gradient instead of downloading
                img = Image.new('RGB', (800, 800))
                
                # Create a simple gradient based on the texture type
                if category == 'wood':
                    color = (139, 69, 19)  # Brown
                elif category == 'fabric':
                    color = (0, 0, 139)  # Blue for velvet
                elif category == 'leather':
                    color = (101, 67, 33)  # Brown
                elif category == 'metal':
                    color = (192, 192, 192)  # Silver
                elif category == 'glass':
                    color = (200, 200, 255)  # Light blue
                else:  # stone
                    color = (169, 169, 169)  # Gray
                
                # Fill with solid color for now
                img.paste(color, [0, 0, 800, 800])
                
                # Save full-size image
                full_path = os.path.join(full_dir, f'{texture_name}.jpg')
                img.save(full_path, 'JPEG', quality=95)
                
                # Create and save thumbnail
                thumbnail = create_thumbnail(img)
                thumb_path = os.path.join(thumb_dir, f'{texture_name}.jpg')
                thumbnail.save(thumb_path, 'JPEG', quality=90)
                
                print(f'Created texture: {category}/{texture_name}')
                
            except Exception as e:
                print(f'Error processing {texture_name}: {str(e)}')

if __name__ == '__main__':
    download_and_save_textures() 