class Texture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    preview_image_path = db.Column(db.String(200), nullable=False)
    thumbnail_path = db.Column(db.String(200), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('texture_category.id'), nullable=False)
    
    # Relationships
    category = db.relationship('TextureCategory', backref='textures') 