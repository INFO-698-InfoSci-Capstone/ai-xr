-- Insert furniture types with their categories
INSERT INTO furniture_types (name, category) VALUES
('Modern Sofa', 'sofa'),
('Classic Sofa', 'sofa'),
('Accent Chair', 'chair'),
('Dining Chair', 'chair'),
('Office Desk', 'desk'),
('Dining Table', 'table'),
('Coffee Table', 'table'),
('Side Table', 'table'),
('Platform Bed', 'bed');

-- Insert furniture parts
INSERT INTO furniture_parts (name) VALUES
('Seat Cushion'),
('Backrest'),
('Armrest'),
('Frame'),
('Legs'),
('Top Surface'),
('Headboard'),
('Footboard'),
('Platform');

-- Link furniture types to their parts
INSERT INTO furniture_type_parts (furniture_type_id, furniture_part_id) VALUES
-- Sofa (id: 1, 2)
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),  -- Modern Sofa
(2, 1), (2, 2), (2, 3), (2, 4), (2, 5),  -- Classic Sofa

-- Chairs (id: 3, 4)
(3, 1), (3, 2), (3, 3), (3, 4), (3, 5),  -- Accent Chair
(4, 1), (4, 2), (4, 4), (4, 5),          -- Dining Chair

-- Desk (id: 5)
(5, 6), (5, 4), (5, 5),  -- Office Desk

-- Tables (id: 6, 7, 8)
(6, 6), (6, 4), (6, 5),  -- Dining Table
(7, 6), (7, 4), (7, 5),  -- Coffee Table
(8, 6), (8, 4), (8, 5),  -- Side Table

-- Bed (id: 9)
(9, 7), (9, 8), (9, 9), (9, 4), (9, 5);  -- Platform Bed

-- Insert texture categories with descriptions
INSERT INTO texture_categories (id, name, description) VALUES
(1, 'Fabric', 'Soft and comfortable fabric materials'),
(2, 'Leather', 'Premium leather materials'),
(3, 'Wood', 'Natural and processed wood materials'),
(4, 'Metal', 'Various metal finishes'),
(5, 'Glass', 'Clear and frosted glass options'),
(6, 'Stone', 'Natural and engineered stone materials');

-- Link parts to compatible texture categories
INSERT INTO part_texture_categories (part_id, texture_category_id) VALUES
-- Seat Cushion (id: 1)
(1, 1),  -- Fabric
(1, 2),  -- Leather

-- Backrest (id: 2)
(2, 1),  -- Fabric
(2, 2),  -- Leather

-- Armrest (id: 3)
(3, 1),  -- Fabric
(3, 2),  -- Leather

-- Frame (id: 4)
(4, 3),  -- Wood
(4, 4),  -- Metal

-- Legs (id: 5)
(5, 3),  -- Wood
(5, 4),  -- Metal

-- Top Surface (id: 6)
(6, 3),  -- Wood
(6, 4),  -- Metal
(6, 5),  -- Glass
(6, 6),  -- Stone

-- Headboard (id: 7)
(7, 1),  -- Fabric
(7, 2),  -- Leather
(7, 3),  -- Wood

-- Footboard (id: 8)
(8, 3),  -- Wood
(8, 4),  -- Metal

-- Platform (id: 9)
(9, 3),  -- Wood
(9, 4);  -- Metal

-- Insert textures with descriptions
INSERT INTO textures (id, name, category_id, description, preview_image_path, thumbnail_path) VALUES
-- Fabric textures
(1, 'Blue Velvet', 1, 'Deep plush velvet texture with visible pile and light-catching surface', '/textures/fabric/full/velvet_blue.jpg', '/textures/fabric/thumbnails/velvet_blue.jpg'),
(2, 'Gray Linen', 1, 'Natural linen fabric with visible woven texture', '/textures/fabric/full/linen_gray.jpg', '/textures/fabric/thumbnails/linen_gray.jpg'),
(3, 'Beige Cotton', 1, 'Soft cotton weave in warm beige', '/textures/fabric/full/cotton_beige.jpg', '/textures/fabric/thumbnails/cotton_beige.jpg'),

-- Leather textures
(4, 'Brown Leather', 2, 'Premium full-grain leather with natural pores', '/textures/leather/full/leather_brown.jpg', '/textures/leather/thumbnails/leather_brown.jpg'),
(5, 'Black Leather', 2, 'Smooth black leather with subtle grain pattern', '/textures/leather/full/leather_black.jpg', '/textures/leather/thumbnails/leather_black.jpg'),

-- Wood textures
(6, 'Oak Wood', 3, 'Natural oak wood grain with warm honey tones', '/textures/wood/full/wood_oak.jpg', '/textures/wood/thumbnails/wood_oak.jpg'),
(7, 'Walnut Wood', 3, 'Rich dark walnut wood with distinctive grain pattern', '/textures/wood/full/wood_walnut.jpg', '/textures/wood/thumbnails/wood_walnut.jpg'),

-- Metal textures
(8, 'Brushed Steel', 4, 'Brushed stainless steel with linear grain pattern', '/textures/metal/full/metal_steel.jpg', '/textures/metal/thumbnails/metal_steel.jpg'),
(9, 'Brass', 4, 'Polished brass with warm golden tone', '/textures/metal/full/metal_brass.jpg', '/textures/metal/thumbnails/metal_brass.jpg'),

-- Glass textures
(10, 'Clear Glass', 5, 'Transparent glass with subtle surface reflection', '/textures/glass/full/glass_clear.jpg', '/textures/glass/thumbnails/glass_clear.jpg'),
(11, 'Frosted Glass', 5, 'Frosted glass with diffused light effect', '/textures/glass/full/glass_frosted.jpg', '/textures/glass/thumbnails/glass_frosted.jpg'),

-- Stone textures
(12, 'Marble', 6, 'White marble with gray veining', '/textures/stone/full/stone_marble.jpg', '/textures/stone/thumbnails/stone_marble.jpg'),
(13, 'Granite', 6, 'Speckled granite in gray and black tones', '/textures/stone/full/stone_granite.jpg', '/textures/stone/thumbnails/stone_granite.jpg');

-- Update textures with proper image paths
UPDATE textures SET 
    preview_image_path = '/textures/fabric/full/velvet_blue.jpg',
    thumbnail_path = '/textures/fabric/thumbnails/velvet_blue.jpg'
WHERE id = 1;

UPDATE textures SET 
    preview_image_path = '/textures/fabric/full/linen_gray.jpg',
    thumbnail_path = '/textures/fabric/thumbnails/linen_gray.jpg'
WHERE id = 2;

UPDATE textures SET 
    preview_image_path = '/textures/fabric/full/cotton_beige.jpg',
    thumbnail_path = '/textures/fabric/thumbnails/cotton_beige.jpg'
WHERE id = 3;

UPDATE textures SET 
    preview_image_path = '/textures/leather/full/leather_brown.jpg',
    thumbnail_path = '/textures/leather/thumbnails/leather_brown.jpg'
WHERE id = 4;

UPDATE textures SET 
    preview_image_path = '/textures/leather/full/leather_black.jpg',
    thumbnail_path = '/textures/leather/thumbnails/leather_black.jpg'
WHERE id = 5;

UPDATE textures SET 
    preview_image_path = '/textures/wood/full/wood_oak.jpg',
    thumbnail_path = '/textures/wood/thumbnails/wood_oak.jpg'
WHERE id = 6;

UPDATE textures SET 
    preview_image_path = '/textures/wood/full/wood_walnut.jpg',
    thumbnail_path = '/textures/wood/thumbnails/wood_walnut.jpg'
WHERE id = 7;

UPDATE textures SET 
    preview_image_path = '/textures/metal/full/metal_steel.jpg',
    thumbnail_path = '/textures/metal/thumbnails/metal_steel.jpg'
WHERE id = 8;

UPDATE textures SET 
    preview_image_path = '/textures/metal/full/metal_brass.jpg',
    thumbnail_path = '/textures/metal/thumbnails/metal_brass.jpg'
WHERE id = 9;

UPDATE textures SET 
    preview_image_path = '/textures/glass/full/glass_clear.jpg',
    thumbnail_path = '/textures/glass/thumbnails/glass_clear.jpg'
WHERE id = 10;

UPDATE textures SET 
    preview_image_path = '/textures/glass/full/glass_frosted.jpg',
    thumbnail_path = '/textures/glass/thumbnails/glass_frosted.jpg'
WHERE id = 11;

UPDATE textures SET 
    preview_image_path = '/textures/stone/full/stone_marble.jpg',
    thumbnail_path = '/textures/stone/thumbnails/stone_marble.jpg'
WHERE id = 12;

UPDATE textures SET 
    preview_image_path = '/textures/stone/full/stone_granite.jpg',
    thumbnail_path = '/textures/stone/thumbnails/stone_granite.jpg'
WHERE id = 13; 