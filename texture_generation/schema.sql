-- Drop existing tables if they exist (in correct order due to foreign key dependencies)
DROP TABLE IF EXISTS part_texture_categories CASCADE;
DROP TABLE IF EXISTS furniture_type_parts CASCADE;
DROP TABLE IF EXISTS textures CASCADE;
DROP TABLE IF EXISTS texture_categories CASCADE;
DROP TABLE IF EXISTS furniture_parts CASCADE;
DROP TABLE IF EXISTS furniture_types CASCADE;

-- Create tables with SERIAL IDs and proper foreign key relationships
CREATE TABLE furniture_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL
);

CREATE TABLE furniture_parts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE texture_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(200)
);

CREATE TABLE textures (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(200),
    category_id INTEGER NOT NULL REFERENCES texture_categories(id),
    preview_image_path VARCHAR(200) NOT NULL,
    thumbnail_path VARCHAR(200) NOT NULL
);

CREATE TABLE furniture_type_parts (
    furniture_type_id INTEGER REFERENCES furniture_types(id),
    furniture_part_id INTEGER REFERENCES furniture_parts(id),
    PRIMARY KEY (furniture_type_id, furniture_part_id)
);

CREATE TABLE part_texture_categories (
    part_id INTEGER REFERENCES furniture_parts(id),
    texture_category_id INTEGER REFERENCES texture_categories(id),
    PRIMARY KEY (part_id, texture_category_id)
);

-- Create indexes for better query performance
CREATE INDEX idx_furniture_type_category ON furniture_types(category);
CREATE INDEX idx_texture_category ON textures(category_id);
CREATE INDEX idx_furniture_type_parts_type ON furniture_type_parts(furniture_type_id);
CREATE INDEX idx_furniture_type_parts_part ON furniture_type_parts(furniture_part_id);
CREATE INDEX idx_part_texture_categories_part ON part_texture_categories(part_id);
CREATE INDEX idx_part_texture_categories_category ON part_texture_categories(texture_category_id); 