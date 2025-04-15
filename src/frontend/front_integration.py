import os
import sys
import json
import argparse
from flask import Flask, request, jsonify, render_template, send_from_directory
import yaml
import glob
from typing import Dict, List, Optional

# Add parent directory to path for imports to work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our custom modules
from texture_generation.dynamic_description_generator import DynamicDescriptionGenerator
from texture_generation.texture_generator import TextureGenerator
from texture_generation.annotation_integration import AnnotationInterface

# Create Flask app
app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

# Global variables
UPLOAD_FOLDER = './uploads'
OUTPUT_FOLDER = './output'
TEXTURE_FOLDER = './textures'

# Ensure directories exist
for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER, TEXTURE_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# Initialize our classes
description_generator = DynamicDescriptionGenerator(use_ai_model=False)
texture_generator = TextureGenerator()
annotation_interface = AnnotationInterface(output_dir=OUTPUT_FOLDER)

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Save the uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # Process the uploaded file
    if file.filename.endswith('.yaml'):
        return process_yaml_file(file_path)
    elif file.filename.endswith('.txt'):
        return process_label_file(file_path)
    elif file.filename.endswith(('.jpg', '.jpeg', '.png')):
        return process_image_file(file_path)
    else:
        return jsonify({'error': 'Unsupported file type'}), 400

def process_yaml_file(yaml_path):
    """Process a YOLO data.yaml file"""
    try:
        # Parse the YAML file
        with open(yaml_path, 'r') as f:
            data_yaml = yaml.safe_load(f)
        
        # Extract class names
        class_names = data_yaml.get('names', [])
        if not class_names:
            return jsonify({'error': 'No class names found in YAML file'}), 400
        
        # Set the class names in the annotation interface
        annotation_interface.class_names = class_names
        
        # Generate descriptions and texture suggestions
        materials_data = generate_materials_data(class_names)
        
        return jsonify({
            'success': True,
            'message': f"Processed {len(class_names)} classes",
            'materials': materials_data
        })
    
    except Exception as e:
        return jsonify({'error': f"Error processing YAML file: {str(e)}"}), 500

def process_label_file(label_path):
    """Process a YOLO label file"""
    try:
        # Extract class IDs from the label file
        with open(label_path, 'r') as f:
            lines = f.readlines()
        
        # Extract class IDs
        class_ids = set()
        for line in lines:
            parts = line.strip().split()
            if len(parts) > 0:
                class_id = int(parts[0])
                class_ids.add(class_id)
        
        if not class_ids:
            return jsonify({'error': 'No class IDs found in label file'}), 400
        
        # Get material information for each class
        materials = []
        for class_id in sorted(class_ids):
            materials.append(annotation_interface.get_material_info(class_id))
        
        # Create materials data
        materials_data = {
            'materials': materials,
            'timestamp': annotation_interface._get_timestamp(),
            'version': '1.0'
        }
        
        # Save to file
        output_path = os.path.join(OUTPUT_FOLDER, 'material_descriptions.json')
        with open(output_path, 'w') as f:
            json.dump(materials_data, f, indent=2)
        
        return jsonify({
            'success': True,
            'message': f"Processed {len(class_ids)} classes from label file",
            'materials': materials_data
        })
    
    except Exception as e:
        return jsonify({'error': f"Error processing label file: {str(e)}"}), 500

def process_image_file(image_path):
    """Process an image file with YOLO annotations"""
    try:
        # Process the image using the annotation interface
        result = annotation_interface.process_image(image_path)
        
        # Get all materials
        materials_data = annotation_interface.get_all_materials()
        
        return jsonify({
            'success': True,
            'message': f"Processed image with {len(result['masks'])} segmentation masks",
            'image_path': image_path,
            'visualization_path': result['visualization_path'],
            'materials': materials_data
        })
    
    except Exception as e:
        return jsonify({'error': f"Error processing image file: {str(e)}"}), 500

def generate_materials_data(class_names):
    """Generate materials data from class names"""
    # Generate descriptions and texture suggestions
    results = {}
    for idx, class_name in enumerate(class_names):
        description = description_generator.get_material_description(class_name)
        texture_suggestions = description_generator.get_texture_suggestions(class_name)
        
        results[class_name] = {
            'id': idx,
            'name': class_name,
            'description': description,
            'texture_suggestions': texture_suggestions
        }
    
    # Save the results to a JSON file
    output_path = os.path.join(OUTPUT_FOLDER, 'material_descriptions.json')
    frontend_data = {
        'materials': list(results.values()),
        'timestamp': description_generator._get_timestamp(),
        'version': '1.0'
    }
    
    with open(output_path, 'w') as f:
        json.dump(frontend_data, f, indent=2)
    
    return frontend_data

@app.route('/api/download_dataset', methods=['POST'])
def download_dataset():
    """Download dataset from Roboflow"""
    try:
        # Download the dataset
        dataset_path = annotation_interface.download_dataset()
        
        # Get all materials
        materials_data = annotation_interface.get_all_materials()
        
        return jsonify({
            'success': True,
            'message': f"Downloaded dataset to {dataset_path}",
            'dataset_path': dataset_path,
            'materials': materials_data
        })
    
    except Exception as e:
        return jsonify({'error': f"Error downloading dataset: {str(e)}"}), 500

@app.route('/api/process_sample_images', methods=['POST'])
def process_sample_images():
    """Process sample images from the dataset"""
    try:
        if not annotation_interface.dataset_path:
            # Try to download the dataset first
            dataset_path = annotation_interface.download_dataset()
        else:
            dataset_path = annotation_interface.dataset_path
        
        # Get images from the dataset
        test_dir = os.path.join(dataset_path, "test")
        images_dir = os.path.join(test_dir, "images")
        
        if not os.path.exists(images_dir):
            return jsonify({'error': f"Images directory not found: {images_dir}"}), 404
        
        # Find image files
        image_files = sorted([
            os.path.join(images_dir, f) for f in os.listdir(images_dir)
            if f.endswith(('.jpg', '.jpeg', '.png'))
        ])
        
        if not image_files:
            return jsonify({'error': "No image files found"}), 404
        
        # Process up to 3 images
        results = []
        for img_file in image_files[:3]:
            try:
                result = annotation_interface.process_image(img_file)
                results.append({
                    'image_path': img_file,
                    'visualization_path': result['visualization_path'],
                    'masks_count': len(result['masks'])
                })
            except Exception as e:
                print(f"Error processing {img_file}: {e}")
        
        # Get all materials
        materials_data = annotation_interface.get_all_materials()
        
        return jsonify({
            'success': True,
            'message': f"Processed {len(results)} sample images",
            'results': results,
            'materials': materials_data
        })
    
    except Exception as e:
        return jsonify({'error': f"Error processing sample images: {str(e)}"}), 500

@app.route('/api/generate_textures', methods=['POST'])
def generate_textures():
    """Generate textures for materials"""
    try:
        # Get request data
        data = request.json
        materials_json_path = data.get('materials_json_path')
        
        if not materials_json_path:
            # Use default path if not provided
            materials_json_path = os.path.join(OUTPUT_FOLDER, 'material_descriptions.json')
        
        # Check if the file exists
        if not os.path.exists(materials_json_path):
            # Try to generate materials data from the annotation interface
            materials_data = annotation_interface.get_all_materials()
            
            if not materials_data['materials']:
                return jsonify({'error': 'No materials data available. Please upload a file or download a dataset first.'}), 404
        else:
            # Load the materials data
            with open(materials_json_path, 'r') as f:
                materials_data = json.load(f)
        
        # Generate textures
        texture_paths = texture_generator.process_materials_json(
            json_path=materials_json_path,
            output_dir=TEXTURE_FOLDER
        )
        
        # Create previews for each material
        previews = {}
        for material_name, paths in texture_paths.items():
            preview_path = texture_generator.create_texture_preview(material_name, paths)
            if preview_path:
                previews[material_name] = preview_path
        
        return jsonify({
            'success': True,
            'message': f"Generated textures for {len(texture_paths)} materials",
            'texture_paths': texture_paths,
            'previews': previews
        })
    
    except Exception as e:
        return jsonify({'error': f"Error generating textures: {str(e)}"}), 500

@app.route('/api/materials', methods=['GET'])
def get_materials():
    """Get available materials"""
    try:
        materials_json_path = os.path.join(OUTPUT_FOLDER, 'material_descriptions.json')
        
        if not os.path.exists(materials_json_path):
            # Try to generate materials data from the annotation interface
            materials_data = annotation_interface.get_all_materials()
            
            if not materials_data['materials']:
                return jsonify({'error': 'No materials data available. Please upload a file or download a dataset first.'}), 404
        else:
            # Load the materials data
            with open(materials_json_path, 'r') as f:
                materials_data = json.load(f)
        
        return jsonify(materials_data)
    
    except Exception as e:
        return jsonify({'error': f"Error retrieving materials: {str(e)}"}), 500

@app.route('/api/textures/<material_name>', methods=['GET'])
def get_textures(material_name):
    """Get available textures for a material"""
    try:
        material_dir = os.path.join(TEXTURE_FOLDER, material_name)
        
        if not os.path.exists(material_dir):
            return jsonify({'error': f"No textures available for {material_name}"}), 404
        
        # Get texture files
        texture_files = glob.glob(os.path.join(material_dir, f"{material_name}_*.png"))
        
        # Get preview if available
        preview_path = os.path.join(material_dir, f"{material_name}_preview.png")
        has_preview = os.path.exists(preview_path)
        
        return jsonify({
            'success': True,
            'material': material_name,
            'textures': [os.path.basename(path) for path in texture_files],
            'has_preview': has_preview,
            'preview': os.path.basename(preview_path) if has_preview else None
        })
    
    except Exception as e:
        return jsonify({'error': f"Error retrieving textures: {str(e)}"}), 500

@app.route('/api/segmentation/<image_name>', methods=['GET'])
def get_segmentation(image_name):
    """Get segmentation results for an image"""
    try:
        base_name = os.path.splitext(image_name)[0]
        
        if base_name not in annotation_interface.annotation_results:
            return jsonify({'error': f"No segmentation results for {image_name}"}), 404
        
        return jsonify({
            'success': True,
            'result': annotation_interface.annotation_results[base_name]
        })
    
    except Exception as e:
        return jsonify({'error': f"Error retrieving segmentation results: {str(e)}"}), 500

@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    """Serve uploaded files"""
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/output/<path:filename>')
def serve_output(filename):
    """Serve output files"""
    return send_from_directory(OUTPUT_FOLDER, filename)

@app.route('/textures/<path:filename>')
def serve_texture(filename):
    """Serve texture files"""
    return send_from_directory(TEXTURE_FOLDER, filename)

def main():
    """Main entry point for the frontend application"""
    parser = argparse.ArgumentParser(description="Furniture Texture Frontend")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to run the server on")
    parser.add_argument("--port", type=int, default=5000, help="Port to run the server on")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    parser.add_argument("--download-dataset", action="store_true", help="Download dataset from Roboflow")
    
    args = parser.parse_args()
    
    # Download dataset if requested
    if args.download_dataset:
        try:
            dataset_path = annotation_interface.download_dataset()
            print(f"Downloaded dataset to {dataset_path}")
            
            # Process sample images
            process_sample_images()
        except Exception as e:
            print(f"Error downloading dataset: {e}")
    
    # Run the Flask app
    print(f"Starting frontend server at http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()