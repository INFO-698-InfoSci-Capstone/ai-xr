-- Update fabric textures
UPDATE textures 
SET preview_image_path = '/textures/fabric/full/velvet_blue.jpg',
    thumbnail_path = '/textures/fabric/thumbnails/velvet_blue.jpg'
WHERE id = 1 AND name = 'Blue Velvet';

UPDATE textures 
SET preview_image_path = '/textures/fabric/full/linen_gray.jpg',
    thumbnail_path = '/textures/fabric/thumbnails/linen_gray.jpg'
WHERE id = 2 AND name = 'Gray Linen';

UPDATE textures 
SET preview_image_path = '/textures/fabric/full/cotton_beige.jpg',
    thumbnail_path = '/textures/fabric/thumbnails/cotton_beige.jpg'
WHERE id = 3 AND name = 'Beige Cotton';

-- Update leather textures
UPDATE textures 
SET preview_image_path = '/textures/leather/full/leather_brown.jpg',
    thumbnail_path = '/textures/leather/thumbnails/leather_brown.jpg'
WHERE id = 4 AND name = 'Brown Leather';

UPDATE textures 
SET preview_image_path = '/textures/leather/full/leather_black.jpg',
    thumbnail_path = '/textures/leather/thumbnails/leather_black.jpg'
WHERE id = 5 AND name = 'Black Leather';

-- Update wood textures
UPDATE textures 
SET preview_image_path = '/textures/wood/full/wood_oak.jpg',
    thumbnail_path = '/textures/wood/thumbnails/wood_oak.jpg'
WHERE id = 6 AND name = 'Oak Wood';

UPDATE textures 
SET preview_image_path = '/textures/wood/full/wood_walnut.jpg',
    thumbnail_path = '/textures/wood/thumbnails/wood_walnut.jpg'
WHERE id = 7 AND name = 'Walnut Wood';

-- Update metal textures
UPDATE textures 
SET preview_image_path = '/textures/metal/full/metal_steel.jpg',
    thumbnail_path = '/textures/metal/thumbnails/metal_steel.jpg'
WHERE id = 8 AND name = 'Brushed Steel';

UPDATE textures 
SET preview_image_path = '/textures/metal/full/metal_brass.jpg',
    thumbnail_path = '/textures/metal/thumbnails/metal_brass.jpg'
WHERE id = 9 AND name = 'Brass';

-- Update glass textures
UPDATE textures 
SET preview_image_path = '/textures/glass/full/glass_clear.jpg',
    thumbnail_path = '/textures/glass/thumbnails/glass_clear.jpg'
WHERE id = 10 AND name = 'Clear Glass';

UPDATE textures 
SET preview_image_path = '/textures/glass/full/glass_frosted.jpg',
    thumbnail_path = '/textures/glass/thumbnails/glass_frosted.jpg'
WHERE id = 11 AND name = 'Frosted Glass';

-- Update stone textures
UPDATE textures 
SET preview_image_path = '/textures/stone/full/stone_marble.jpg',
    thumbnail_path = '/textures/stone/thumbnails/stone_marble.jpg'
WHERE id = 12 AND name = 'Marble';

UPDATE textures 
SET preview_image_path = '/textures/stone/full/stone_granite.jpg',
    thumbnail_path = '/textures/stone/thumbnails/stone_granite.jpg'
WHERE id = 13 AND name = 'Granite';

-- Verify the updates
SELECT id, name, category_id, preview_image_path, thumbnail_path 
FROM textures 
ORDER BY id; 