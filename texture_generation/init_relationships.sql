-- First, let's insert some basic parts for furniture
INSERT INTO furniture_parts (id, name) VALUES
(1, 'Seat Cushion'),
(2, 'Backrest'),
(3, 'Armrest'),
(4, 'Frame'),
(5, 'Legs'),
(6, 'Top Surface'),
(7, 'Headboard'),
(8, 'Footboard'),
(9, 'Platform');

-- Now link furniture types to their parts
INSERT INTO furniture_type_parts (furniture_type_id, furniture_part_id) VALUES
-- Sofa (id: 1)
(1, 1),  -- Seat Cushion
(1, 2),  -- Backrest
(1, 3),  -- Armrest
(1, 4),  -- Frame
(1, 5),  -- Legs

-- Accent Chair (id: 2)
(2, 1),  -- Seat Cushion
(2, 2),  -- Backrest
(2, 3),  -- Armrest
(2, 4),  -- Frame
(2, 5),  -- Legs

-- Dining Chair (id: 3)
(3, 1),  -- Seat Cushion
(3, 2),  -- Backrest
(3, 4),  -- Frame
(3, 5),  -- Legs

-- Bench (id: 4)
(4, 1),  -- Seat Cushion
(4, 4),  -- Frame
(4, 5),  -- Legs

-- Desk (id: 5)
(5, 6),  -- Top Surface
(5, 4),  -- Frame
(5, 5),  -- Legs

-- Dining Table (id: 6)
(6, 6),  -- Top Surface
(6, 4),  -- Frame
(6, 5),  -- Legs

-- Coffee Table (id: 7)
(7, 6),  -- Top Surface
(7, 4),  -- Frame
(7, 5),  -- Legs

-- Side Table (id: 8)
(8, 6),  -- Top Surface
(8, 4),  -- Frame
(8, 5),  -- Legs

-- Bed (id: 9)
(9, 7),  -- Headboard
(9, 8),  -- Footboard
(9, 9),  -- Platform
(9, 4),  -- Frame
(9, 5);  -- Legs

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