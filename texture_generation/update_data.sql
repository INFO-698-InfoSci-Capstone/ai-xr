-- Truncate all tables in the correct order (reverse of creation order)
TRUNCATE TABLE part_texture_categories CASCADE;
TRUNCATE TABLE furniture_type_parts CASCADE;
TRUNCATE TABLE textures CASCADE;
TRUNCATE TABLE texture_categories CASCADE;
TRUNCATE TABLE furniture_parts CASCADE;
TRUNCATE TABLE furniture_types CASCADE;

-- Insert furniture types with their categories and descriptions
INSERT INTO furniture_types (name, category, description) VALUES
('Modern Sofa', 'sofa', 'Contemporary sofa with clean lines and minimalist design'),
('Classic Sofa', 'sofa', 'Traditional sofa with elegant details and timeless appeal'),
('Accent Chair', 'chair', 'Stylish chair perfect for adding a decorative touch'),
('Dining Chair', 'chair', 'Comfortable chair designed for dining room use'),
('Office Desk', 'desk', 'Professional desk with ample workspace'),
('Dining Table', 'table', 'Elegant table for dining room settings'),
('Coffee Table', 'table', 'Low table perfect for living room settings'),
('Side Table', 'table', 'Small table ideal for placing next to seating'),
('Platform Bed', 'bed', 'Modern bed with clean lines and low profile');

-- Insert furniture parts with descriptions
INSERT INTO furniture_parts (name, description) VALUES
('Seat Cushion', 'Main seating surface for comfort'),
('Backrest', 'Support for back while seated'),
('Armrest', 'Support for arms while seated'),
('Frame', 'Main structural component'),
('Legs', 'Support structure for elevation'),
('Top Surface', 'Main usable surface area'),
('Headboard', 'Decorative and functional bed head'),
('Footboard', 'Decorative and functional bed foot'),
('Platform', 'Main support surface for mattress');

-- Insert texture categories with descriptions
INSERT INTO texture_categories (name, description) VALUES
('Fabric', 'Soft and comfortable fabric materials'),
('Leather', 'Premium leather materials'),
('Wood', 'Natural and processed wood materials'),
('Metal', 'Various metal finishes'),
('Glass', 'Clear and frosted glass options'),
('Stone', 'Natural and engineered stone materials');

-- Link furniture types to their parts (using subqueries to get IDs)
INSERT INTO furniture_type_parts (furniture_type_id, furniture_part_id)
SELECT ft.id, fp.id
FROM furniture_types ft, furniture_parts fp
WHERE ft.name = 'Modern Sofa' AND fp.name IN ('Seat Cushion', 'Backrest', 'Armrest', 'Frame', 'Legs');

INSERT INTO furniture_type_parts (furniture_type_id, furniture_part_id)
SELECT ft.id, fp.id
FROM furniture_types ft, furniture_parts fp
WHERE ft.name = 'Classic Sofa' AND fp.name IN ('Seat Cushion', 'Backrest', 'Armrest', 'Frame', 'Legs');

INSERT INTO furniture_type_parts (furniture_type_id, furniture_part_id)
SELECT ft.id, fp.id
FROM furniture_types ft, furniture_parts fp
WHERE ft.name = 'Accent Chair' AND fp.name IN ('Seat Cushion', 'Backrest', 'Armrest', 'Frame', 'Legs');

INSERT INTO furniture_type_parts (furniture_type_id, furniture_part_id)
SELECT ft.id, fp.id
FROM furniture_types ft, furniture_parts fp
WHERE ft.name = 'Dining Chair' AND fp.name IN ('Seat Cushion', 'Backrest', 'Frame', 'Legs');

INSERT INTO furniture_type_parts (furniture_type_id, furniture_part_id)
SELECT ft.id, fp.id
FROM furniture_types ft, furniture_parts fp
WHERE ft.name IN ('Office Desk', 'Dining Table', 'Coffee Table', 'Side Table') 
AND fp.name IN ('Top Surface', 'Frame', 'Legs');

INSERT INTO furniture_type_parts (furniture_type_id, furniture_part_id)
SELECT ft.id, fp.id
FROM furniture_types ft, furniture_parts fp
WHERE ft.name = 'Platform Bed' AND fp.name IN ('Headboard', 'Footboard', 'Platform', 'Frame', 'Legs');

-- Link parts to compatible texture categories
INSERT INTO part_texture_categories (furniture_part_id, texture_category_id)
SELECT fp.id, tc.id
FROM furniture_parts fp, texture_categories tc
WHERE fp.name = 'Seat Cushion' AND tc.name IN ('Fabric', 'Leather');

INSERT INTO part_texture_categories (furniture_part_id, texture_category_id)
SELECT fp.id, tc.id
FROM furniture_parts fp, texture_categories tc
WHERE fp.name = 'Backrest' AND tc.name IN ('Fabric', 'Leather');

INSERT INTO part_texture_categories (furniture_part_id, texture_category_id)
SELECT fp.id, tc.id
FROM furniture_parts fp, texture_categories tc
WHERE fp.name = 'Armrest' AND tc.name IN ('Fabric', 'Leather');

INSERT INTO part_texture_categories (furniture_part_id, texture_category_id)
SELECT fp.id, tc.id
FROM furniture_parts fp, texture_categories tc
WHERE fp.name = 'Frame' AND tc.name IN ('Wood', 'Metal');

INSERT INTO part_texture_categories (furniture_part_id, texture_category_id)
SELECT fp.id, tc.id
FROM furniture_parts fp, texture_categories tc
WHERE fp.name = 'Legs' AND tc.name IN ('Wood', 'Metal');

INSERT INTO part_texture_categories (furniture_part_id, texture_category_id)
SELECT fp.id, tc.id
FROM furniture_parts fp, texture_categories tc
WHERE fp.name = 'Top Surface' AND tc.name IN ('Wood', 'Metal', 'Glass', 'Stone');

INSERT INTO part_texture_categories (furniture_part_id, texture_category_id)
SELECT fp.id, tc.id
FROM furniture_parts fp, texture_categories tc
WHERE fp.name = 'Headboard' AND tc.name IN ('Fabric', 'Leather', 'Wood');

INSERT INTO part_texture_categories (furniture_part_id, texture_category_id)
SELECT fp.id, tc.id
FROM furniture_parts fp, texture_categories tc
WHERE fp.name = 'Footboard' AND tc.name IN ('Wood', 'Metal');

INSERT INTO part_texture_categories (furniture_part_id, texture_category_id)
SELECT fp.id, tc.id
FROM furniture_parts fp, texture_categories tc
WHERE fp.name = 'Platform' AND tc.name IN ('Wood', 'Metal');

-- Insert textures
INSERT INTO textures (name, category_id, description, preview_image_path, thumbnail_path)
SELECT 'Blue Velvet', tc.id,
       'Deep plush velvet texture with visible pile and light-catching surface',
       '/textures/fabric/full/velvet_blue.jpg',
       '/textures/fabric/thumbnails/velvet_blue.jpg'
FROM texture_categories tc WHERE tc.name = 'Fabric';

INSERT INTO textures (name, category_id, description, preview_image_path, thumbnail_path)
SELECT 'Gray Linen', tc.id,
       'Natural linen fabric with visible woven texture',
       '/textures/fabric/full/linen_gray.jpg',
       '/textures/fabric/thumbnails/linen_gray.jpg'
FROM texture_categories tc WHERE tc.name = 'Fabric';

INSERT INTO textures (name, category_id, description, preview_image_path, thumbnail_path)
SELECT 'Beige Cotton', tc.id,
       'Soft cotton weave in warm beige',
       '/textures/fabric/full/cotton_beige.jpg',
       '/textures/fabric/thumbnails/cotton_beige.jpg'
FROM texture_categories tc WHERE tc.name = 'Fabric';

INSERT INTO textures (name, category_id, description, preview_image_path, thumbnail_path)
SELECT 'Brown Leather', tc.id,
       'Premium full-grain leather with natural pores',
       '/textures/leather/full/leather_brown.jpg',
       '/textures/leather/thumbnails/leather_brown.jpg'
FROM texture_categories tc WHERE tc.name = 'Leather';

INSERT INTO textures (name, category_id, description, preview_image_path, thumbnail_path)
SELECT 'Black Leather', tc.id,
       'Smooth black leather with subtle grain pattern',
       '/textures/leather/full/leather_black.jpg',
       '/textures/leather/thumbnails/leather_black.jpg'
FROM texture_categories tc WHERE tc.name = 'Leather';

INSERT INTO textures (name, category_id, description, preview_image_path, thumbnail_path)
SELECT 'Oak Wood', tc.id,
       'Natural oak wood grain with warm honey tones',
       '/textures/wood/full/wood_oak.jpg',
       '/textures/wood/thumbnails/wood_oak.jpg'
FROM texture_categories tc WHERE tc.name = 'Wood';

INSERT INTO textures (name, category_id, description, preview_image_path, thumbnail_path)
SELECT 'Walnut Wood', tc.id,
       'Rich dark walnut wood with distinctive grain pattern',
       '/textures/wood/full/wood_walnut.jpg',
       '/textures/wood/thumbnails/wood_walnut.jpg'
FROM texture_categories tc WHERE tc.name = 'Wood';

INSERT INTO textures (name, category_id, description, preview_image_path, thumbnail_path)
SELECT 'Brushed Steel', tc.id,
       'Brushed stainless steel with linear grain pattern',
       '/textures/metal/full/metal_steel.jpg',
       '/textures/metal/thumbnails/metal_steel.jpg'
FROM texture_categories tc WHERE tc.name = 'Metal';

INSERT INTO textures (name, category_id, description, preview_image_path, thumbnail_path)
SELECT 'Brass', tc.id,
       'Polished brass with warm golden tone',
       '/textures/metal/full/metal_brass.jpg',
       '/textures/metal/thumbnails/metal_brass.jpg'
FROM texture_categories tc WHERE tc.name = 'Metal';

INSERT INTO textures (name, category_id, description, preview_image_path, thumbnail_path)
SELECT 'Clear Glass', tc.id,
       'Transparent glass with subtle surface reflection',
       '/textures/glass/full/glass_clear.jpg',
       '/textures/glass/thumbnails/glass_clear.jpg'
FROM texture_categories tc WHERE tc.name = 'Glass';

INSERT INTO textures (name, category_id, description, preview_image_path, thumbnail_path)
SELECT 'Frosted Glass', tc.id,
       'Frosted glass with diffused light effect',
       '/textures/glass/full/glass_frosted.jpg',
       '/textures/glass/thumbnails/glass_frosted.jpg'
FROM texture_categories tc WHERE tc.name = 'Glass';

INSERT INTO textures (name, category_id, description, preview_image_path, thumbnail_path)
SELECT 'Marble', tc.id,
       'White marble with gray veining',
       '/textures/stone/full/stone_marble.jpg',
       '/textures/stone/thumbnails/stone_marble.jpg'
FROM texture_categories tc WHERE tc.name = 'Stone';

INSERT INTO textures (name, category_id, description, preview_image_path, thumbnail_path)
SELECT 'Granite', tc.id,
       'Speckled granite in gray and black tones',
       '/textures/stone/full/stone_granite.jpg',
       '/textures/stone/thumbnails/stone_granite.jpg'
FROM texture_categories tc WHERE tc.name = 'Stone'; 