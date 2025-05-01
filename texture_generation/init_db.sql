-- Insert texture categories
INSERT INTO texture_categories (id, name, description) VALUES
(1, 'Fabric', 'Soft and comfortable fabric materials'),
(2, 'Leather', 'Premium leather materials'),
(3, 'Wood', 'Natural and processed wood materials'),
(4, 'Metal', 'Various metal finishes'),
(5, 'Glass', 'Clear and frosted glass options'),
(6, 'Stone', 'Natural and engineered stone materials');

-- Insert textures
INSERT INTO textures (id, name, category_id, description, prompt, preview_image_path, thumbnail_path) VALUES
-- Fabric textures
(1, 'Blue Velvet', 1, 'Deep plush velvet texture with visible pile and light-catching surface, rich jewel-toned blue color', 'Deep blue velvet texture, high resolution', '/textures/fabric/velvet_blue.jpg', '/textures/thumbnails/fabric/velvet_blue.jpg'),
(2, 'Gray Linen', 1, 'Natural linen fabric with visible woven texture, modern gray tone', 'Gray linen fabric texture, high resolution', '/textures/fabric/linen_gray.jpg', '/textures/thumbnails/fabric/linen_gray.jpg'),
(3, 'Beige Cotton', 1, 'Soft cotton weave in warm beige, casual and comfortable', 'Beige cotton fabric texture, high resolution', '/textures/fabric/cotton_beige.jpg', '/textures/thumbnails/fabric/cotton_beige.jpg'),

-- Leather textures
(4, 'Brown Leather', 2, 'Premium full-grain leather with natural pores, rich brown color', 'Brown leather texture, high resolution', '/textures/leather/leather_brown.jpg', '/textures/thumbnails/leather/leather_brown.jpg'),
(5, 'Black Leather', 2, 'Smooth black leather with subtle grain pattern', 'Black leather texture, high resolution', '/textures/leather/leather_black.jpg', '/textures/thumbnails/leather/leather_black.jpg'),

-- Wood textures
(6, 'Oak Wood', 3, 'Natural oak wood grain with warm honey tones', 'Oak wood texture, high resolution', '/textures/wood/wood_oak.jpg', '/textures/thumbnails/wood/wood_oak.jpg'),
(7, 'Walnut Wood', 3, 'Rich dark walnut wood with distinctive grain pattern', 'Walnut wood texture, high resolution', '/textures/wood/wood_walnut.jpg', '/textures/thumbnails/wood/wood_walnut.jpg'),

-- Metal textures
(8, 'Brushed Steel', 4, 'Brushed stainless steel with linear grain pattern', 'Brushed steel texture, high resolution', '/textures/metal/metal_steel.jpg', '/textures/thumbnails/metal/metal_steel.jpg'),
(9, 'Brass', 4, 'Polished brass with warm golden tone', 'Brass metal texture, high resolution', '/textures/metal/metal_brass.jpg', '/textures/thumbnails/metal/metal_brass.jpg'),

-- Glass textures
(10, 'Clear Glass', 5, 'Transparent glass with subtle surface reflection', 'Clear glass texture, high resolution', '/textures/glass/glass_clear.jpg', '/textures/thumbnails/glass/glass_clear.jpg'),
(11, 'Frosted Glass', 5, 'Frosted glass with diffused light effect', 'Frosted glass texture, high resolution', '/textures/glass/glass_frosted.jpg', '/textures/thumbnails/glass/glass_frosted.jpg'),

-- Stone textures
(12, 'Marble', 6, 'White marble with gray veining', 'White marble texture, high resolution', '/textures/stone/stone_marble.jpg', '/textures/thumbnails/stone/stone_marble.jpg'),
(13, 'Granite', 6, 'Speckled granite in gray and black tones', 'Granite texture, high resolution', '/textures/stone/stone_granite.jpg', '/textures/thumbnails/stone/stone_granite.jpg'); 