import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def create_wood_texture(size=(800, 800), color=(139, 69, 19)):
    img = Image.new('RGB', size)
    draw = ImageDraw.Draw(img)
    
    # Create wood grain effect
    for i in range(0, size[0], 4):
        color_var = np.random.randint(-20, 20)
        wood_color = tuple(max(0, min(255, c + color_var)) for c in color)
        draw.line([(i, 0), (i, size[1])], fill=wood_color, width=4)
    
    # Add noise and blur for more realism
    img = img.filter(ImageFilter.GaussianBlur(2))
    return img

def create_fabric_texture(size=(800, 800), color=(0, 0, 139)):
    img = Image.new('RGB', size)
    draw = ImageDraw.Draw(img)
    
    # Create fabric weave pattern
    for i in range(0, size[0], 8):
        for j in range(0, size[1], 8):
            color_var = np.random.randint(-15, 15)
            fabric_color = tuple(max(0, min(255, c + color_var)) for c in color)
            draw.rectangle([i, j, i+7, j+7], fill=fabric_color)
    
    # Add texture
    img = img.filter(ImageFilter.GaussianBlur(1))
    return img

def create_leather_texture(size=(800, 800), color=(101, 67, 33)):
    img = Image.new('RGB', size)
    draw = ImageDraw.Draw(img)
    
    # Create base leather color
    draw.rectangle([0, 0, size[0], size[1]], fill=color)
    
    # Add leather grain pattern
    for _ in range(5000):
        x = np.random.randint(0, size[0])
        y = np.random.randint(0, size[1])
        radius = np.random.randint(1, 4)
        color_var = np.random.randint(-30, 10)
        grain_color = tuple(max(0, min(255, c + color_var)) for c in color)
        draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=grain_color)
    
    img = img.filter(ImageFilter.GaussianBlur(1))
    return img

def create_metal_texture(size=(800, 800), color=(192, 192, 192)):
    img = Image.new('RGB', size)
    draw = ImageDraw.Draw(img)
    
    # Create brushed metal effect
    for i in range(0, size[0], 2):
        color_var = np.random.randint(-20, 20)
        metal_color = tuple(max(0, min(255, c + color_var)) for c in color)
        draw.line([(i, 0), (i, size[1])], fill=metal_color)
    
    img = img.filter(ImageFilter.GaussianBlur(1))
    return img

def create_glass_texture(size=(800, 800), is_frosted=False):
    img = Image.new('RGB', size, (240, 240, 255))
    
    if is_frosted:
        # Create frosted effect
        for _ in range(10000):
            x = np.random.randint(0, size[0])
            y = np.random.randint(0, size[1])
            radius = np.random.randint(1, 3)
            color_var = np.random.randint(-15, 15)
            color = (240 + color_var, 240 + color_var, 255)
            ImageDraw.Draw(img).ellipse([x-radius, y-radius, x+radius, y+radius], fill=color)
    
    img = img.filter(ImageFilter.GaussianBlur(2))
    return img

def create_stone_texture(size=(800, 800), is_marble=True):
    img = Image.new('RGB', size, (220, 220, 220))
    draw = ImageDraw.Draw(img)
    
    if is_marble:
        # Create marble veining
        for _ in range(20):
            points = []
            x = np.random.randint(0, size[0])
            y = 0
            points.append((x, y))
            
            for _ in range(np.random.randint(3, 8)):
                x += np.random.randint(-100, 100)
                y += np.random.randint(50, 150)
                points.append((x, y))
            
            # Draw veining
            for i in range(len(points)-1):
                draw.line([points[i], points[i+1]], fill=(180, 180, 180), width=np.random.randint(1, 4))
    else:
        # Create granite speckles
        for _ in range(5000):
            x = np.random.randint(0, size[0])
            y = np.random.randint(0, size[1])
            radius = np.random.randint(1, 4)
            color = (np.random.randint(150, 200),) * 3
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color)
    
    img = img.filter(ImageFilter.GaussianBlur(1))
    return img

def create_and_save_textures():
    base_dir = '../project-bolt-sb1-uelpyywt/project/public/textures'
    
    # Define texture generators for each category
    texture_generators = {
        'wood': {
            'oak': lambda: create_wood_texture(color=(169, 109, 49)),
            'walnut': lambda: create_wood_texture(color=(89, 49, 29))
        },
        'fabric': {
            'velvet_blue': lambda: create_fabric_texture(color=(0, 0, 139)),
            'linen_gray': lambda: create_fabric_texture(color=(169, 169, 169)),
            'cotton_beige': lambda: create_fabric_texture(color=(209, 179, 139))
        },
        'leather': {
            'leather_brown': lambda: create_leather_texture(color=(101, 67, 33)),
            'leather_black': lambda: create_leather_texture(color=(40, 40, 40))
        },
        'metal': {
            'metal_steel': lambda: create_metal_texture(color=(192, 192, 192)),
            'metal_brass': lambda: create_metal_texture(color=(181, 166, 66))
        },
        'glass': {
            'glass_clear': lambda: create_glass_texture(is_frosted=False),
            'glass_frosted': lambda: create_glass_texture(is_frosted=True)
        },
        'stone': {
            'stone_marble': lambda: create_stone_texture(is_marble=True),
            'stone_granite': lambda: create_stone_texture(is_marble=False)
        }
    }
    
    for category, textures in texture_generators.items():
        # Create category directories
        full_dir = os.path.join(base_dir, category, 'full')
        thumb_dir = os.path.join(base_dir, category, 'thumbnails')
        os.makedirs(full_dir, exist_ok=True)
        os.makedirs(thumb_dir, exist_ok=True)
        
        # Generate and save textures
        for texture_name, generator in textures.items():
            try:
                # Generate full-size texture
                img = generator()
                
                # Save full-size image
                full_path = os.path.join(full_dir, f'{texture_name}.jpg')
                img.save(full_path, 'JPEG', quality=95)
                
                # Create and save thumbnail
                thumbnail = img.copy()
                thumbnail.thumbnail((200, 200))
                thumb_path = os.path.join(thumb_dir, f'{texture_name}.jpg')
                thumbnail.save(thumb_path, 'JPEG', quality=90)
                
                print(f'Created texture: {category}/{texture_name}')
                
            except Exception as e:
                print(f'Error processing {texture_name}: {str(e)}')

if __name__ == '__main__':
    create_and_save_textures() 