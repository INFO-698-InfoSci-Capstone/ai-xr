from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv
import uuid
from utils import process_image
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import torch
import diffusers
from diffusers import StableDiffusionPipeline
import base64
from io import BytesIO
from PIL import Image

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='../project/public')
if torch.cuda.is_available():
    print("CUDA is available")
    print(torch.version.cuda)
    print(torch.__version__)
    print(diffusers.__version__)
else:
    print("CUDA is not available")
# Configure CORS for all routes
CORS(app, 
     resources={
         r"/*": {
             "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Origin"],
             "expose_headers": ["Content-Range", "X-Content-Range"],
             "supports_credentials": True,
             "send_wildcard": False
         }
     },
     supports_credentials=True
)

# Add CORS headers to all responses
@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    if origin in ["http://localhost:5173", "http://127.0.0.1:5173"]:
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Max-Age', '3600')
    return response

# Handle OPTIONS requests explicitly
@app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
@app.route('/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    return '', 204

# Initialize Stable Diffusion pipeline
model_id = "stabilityai/stable-diffusion-2-1"
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
).to("cuda")

# Move pipeline to GPU if available
if torch.cuda.is_available():
    print("Moving pipeline to GPU")
    pipe = pipe.to("cuda")
else:
    print("CUDA is not available, using CPU")

# Configure rate limiting with more lenient limits for development
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per minute"],  # Increased from 60 to 200
    storage_uri="memory://"
)

# Configure upload folder for segmentation
UPLOAD_FOLDER = os.path.join('static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set maximum upload size to 10MB
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:root@localhost:5432/texturedb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Association table for furniture type parts
furniture_type_parts = db.Table('furniture_type_parts',
    db.Column('furniture_type_id', db.Integer, db.ForeignKey('furniture_types.id'), primary_key=True),
    db.Column('furniture_part_id', db.Integer, db.ForeignKey('furniture_parts.id'), primary_key=True)
)

# Association table for part texture categories
part_texture_categories = db.Table('part_texture_categories',
    db.Column('part_id', db.Integer, db.ForeignKey('furniture_parts.id'), primary_key=True),
    db.Column('texture_category_id', db.Integer, db.ForeignKey('texture_categories.id'), primary_key=True)
)

class TextureCategory(db.Model):
    __tablename__ = 'texture_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    textures = db.relationship('Texture', backref='category', lazy=True, cascade="all, delete")

class FurniturePart(db.Model):
    __tablename__ = 'furniture_parts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    furniture_types = db.relationship('FurnitureType', secondary=furniture_type_parts, backref=db.backref('parts', lazy=True))
    texture_categories = db.relationship('TextureCategory', secondary=part_texture_categories, backref=db.backref('compatible_parts', lazy=True))

class FurnitureType(db.Model):
    __tablename__ = 'furniture_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)

class Texture(db.Model):
    __tablename__ = 'textures'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('texture_categories.id', ondelete='CASCADE'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    negative_prompt = db.Column(db.Text, nullable=True)
    preview_image_path = db.Column(db.String(255), nullable=False)
    thumbnail_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

# Routes
@app.route('/api/texture-options')
def get_texture_options():
    furniture_type_id = request.args.get('furniture_type_id', type=int)
    part_id = request.args.get('part_id', type=int)
    material_type = request.args.get('material_type', type=str)
    
    try:
        query = Texture.query.join(TextureCategory)
        part = None

        if part_id:
            # Get the furniture part
            part = FurniturePart.query.get(part_id)
            if part:
                # Get compatible texture categories for this part
                category_ids = [category.id for category in part.texture_categories]
                query = query.filter(Texture.category_id.in_(category_ids))

        if material_type:
            # Filter by texture category name matching the material type
            query = query.filter(TextureCategory.name.ilike(material_type))
        
        textures = query.all()
        
        # Format the response
        result = []
        for texture in textures:
            result.append({
                'id': texture.id,
                'name': texture.name,
                'category': texture.category.name,
                'preview_image_path': texture.preview_image_path,
                'thumbnail_path': texture.thumbnail_path,
                'description': texture.description,
                'prompt': texture.prompt,
                'partName': part.name if part else None
            })
        
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/furniture-types')
def get_furniture_types():
    try:
        types = FurnitureType.query.all()
        result = []
        for type_obj in types:
            result.append({
                'id': type_obj.id,
                'name': type_obj.name,
                'category': type_obj.category
            })
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/furniture-parts')
def get_furniture_parts():
    furniture_type_id = request.args.get('furniture_type_id', type=int)
    if not furniture_type_id:
        return jsonify({
            'success': False,
            'error': 'Missing furniture_type_id parameter'
        }), 400
    
    try:
        # Get parts for the specified furniture type
        furniture_type = FurnitureType.query.get(furniture_type_id)
        if not furniture_type:
            return jsonify({
                'success': False,
                'error': 'Furniture type not found'
            }), 404
        
        parts = furniture_type.parts
        result = []
        for part in parts:
            result.append({
                'id': part.id,
                'name': part.name,
                'furniture_type_id': furniture_type_id
            })
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/texture-categories')
def get_texture_categories():
    categories = TextureCategory.query.all()
    result = []
    for category in categories:
        result.append({
            'id': category.id,
            'name': category.name,
            'description': category.description
        })
    return jsonify(result)

@app.route('/api/segment', methods=['POST'])
@limiter.limit("100 per minute")  # More lenient limit for segmentation
def segment_image():
    """Process an image with instance segmentation"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Allowed file types are png, jpg, jpeg'}), 400
    
    try:
        # Create a unique filename
        unique_filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Process the image
        result = process_image(filepath, save_debug_images=True)
        result['success'] = True
        result['image_path'] = os.path.join('uploads', unique_filename)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate-texture', methods=['POST'])
def generate_texture():
    try:
        data = request.json
        print("Received request data:", data)
        
        if not data or 'segmentationData' not in data or 'maskClass' not in data:
            print("Missing required data:", {
                'has_data': bool(data),
                'has_segmentationData': 'segmentationData' in data if data else False,
                'has_maskClass': 'maskClass' in data if data else False
            })
            return jsonify({
                'success': False,
                'error': 'Missing required data'
            }), 400

        # Get the mask data for the specific class
        mask_data = None
        for mask in data['segmentationData']['masks']:
            if mask['class'] == data['maskClass']:
                mask_data = mask
                break

        if not mask_data:
            print("Mask not found for class:", data['maskClass'])
            return jsonify({
                'success': False,
                'error': 'Mask not found'
            }), 404

        # Get prompt from either texture object or direct prompt
        prompt = data.get('prompt')
        if not prompt and 'textureDescription' in data:
            prompt = f"Generate a seamless texture for {data['maskClass']} with the following characteristics: {data['textureDescription']}"

        if not prompt:
            print("No prompt available")
            return jsonify({
                'success': False,
                'error': 'No prompt available for texture generation'
            }), 400

        print("Using prompt:", prompt)

        pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16
    ).to("cuda")
        
        # Generate texture using Stable Diffusion with GPU
        with torch.no_grad():
            if torch.cuda.is_available():
                print("Generating texture on GPU")
                # Move input tensors to GPU
                pipe = pipe.to("cuda")
            else:
                print("Warning: Generating texture on CPU - this will be slow")
            
            image = pipe(
                prompt=prompt,
                negative_prompt="blurry, low quality, distorted, unrealistic",
                num_inference_steps=30,
                guidance_scale=7.5
            ).images[0]

            # Move pipeline back to CPU to free GPU memory
            if torch.cuda.is_available():
                pipe = pipe.to("cpu")
                torch.cuda.empty_cache()

        print("Generated image:", image)

        # Convert the generated image to base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # Save the generated texture
        unique_id = str(uuid.uuid4())
        texture_path = os.path.join('static', 'generated_textures', f'{unique_id}.png')
        os.makedirs(os.path.dirname(texture_path), exist_ok=True)
        image.save(texture_path)

        response = {
            'success': True,
            'generatedTexture': f"data:image/png;base64,{img_str}",
            'texturePath': texture_path
        }
        print("Sending response:", response)
        return jsonify(response)

    except Exception as e:
        print("Error in generate_texture:", str(e))
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Serve uploaded files
@app.route('/static/uploads/<path:filename>')
def serve_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Serve static files from the public directory
@app.route('/textures/<path:filename>')
def serve_texture(filename):
    return send_from_directory(app.static_folder + '/textures', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000) 