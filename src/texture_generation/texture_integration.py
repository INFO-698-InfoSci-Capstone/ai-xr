#!/usr/bin/env python3
"""
Integration script that ties together the YOLO detection,
Stable Diffusion texture generation, and frontend display.
"""

import os
import sys
import argparse
import glob
import shutil
from typing import Dict, List, Optional, Tuple
import json

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules
from dynamic_description_generator import DynamicDescriptionGenerator
from texture_generator import TextureGenerator
from roboflow_loader import download_roboflow_dataset
from segmentation import load_classlabels

def setup_directories(base_dir: str) -> Dict[str, str]:
    """Set up the necessary directories for the project"""
    dirs = {
        'base': base_dir,
        'output': os.path.join(base_dir, 'output'),
        'textures': os.path.join(base_dir, 'textures'),
        'frontend': os.path.join(base_dir, 'frontend')
    }
    
    # Create directories
    for path in dirs.values():
        os.makedirs(path, exist_ok=True)
    
    return dirs

def process_dataset(dataset_path: str, output_dir: str) -> Dict:
    """Process a YOLO dataset and generate descriptions for materials"""
    print(f"Processing dataset at {dataset_path}")
    
    # Check if data.yaml exists
    data_yaml_path = os.path.join(dataset_path, "data.yaml")
    if not os.path.exists(data_yaml_path):
        raise FileNotFoundError(f"data.yaml not found in {dataset_path}")
    
    # Initialize the description generator
    description_generator = DynamicDescriptionGenerator()
    
    # Process the dataset
    class_data = description_generator.process_yolo_annotations(
        data_yaml_path=data_yaml_path,
        labels_dir=os.path.join(dataset_path, "train", "labels")
    )
    
    # Generate frontend JSON
    frontend_json = description_generator.generate_frontend_json(class_data)
    
    # Save the JSON file
    json_path = os.path.join(output_dir, "material_descriptions.json")
    with open(json_path, 'w') as f:
        f.write(frontend_json)
    
    print(f"Saved material descriptions to {json_path}")
    
    return json.loads(frontend_json)

def generate_textures(materials_json: Dict, output_dir: str) -> Dict[str, List[str]]:
    """Generate textures for materials using Stable Diffusion"""
    print("Generating textures for materials")
    
    # Initialize the texture generator
    texture_generator = TextureGenerator()
    
    # Create a temporary JSON file
    temp_json_path = os.path.join(output_dir, "temp_materials.json")
    with open(temp_json_path, 'w') as f:
        json.dump(materials_json, f, indent=2)
    
    # Process the materials JSON
    texture_paths = texture_generator.process_materials_json(
        json_path=temp_json_path,
        output_dir=output_dir
    )
    
    # Create previews for each material
    previews = {}
    for material_name, paths in texture_paths.items():
        preview_path = texture_generator.create_texture_preview(material_name, paths)
        if preview_path:
            previews[material_name] = preview_path
    
    # Remove the temporary file
    if os.path.exists(temp_json_path):
        os.remove(temp_json_path)
    
    print(f"Generated textures for {len(texture_paths)} materials")
    
    return texture_paths

def setup_frontend(frontend_dir: str, output_dir: str) -> None:
    """Set up the frontend files"""
    print(f"Setting up frontend in {frontend_dir}")
    
    # Copy the frontend template files
    static_dir = os.path.join(frontend_dir, "static")
    os.makedirs(static_dir, exist_ok=True)
    
    # Create a simple CSS file
    css_file = os.path.join(static_dir, "style.css")
    with open(css_file, 'w') as f:
        f.write("""
/* Custom styles for the Furniture Texture Generator */
.material-card {
    transition: transform 0.3s ease;
    cursor: pointer;
    margin-bottom: 20px;
}
.material-card:hover {
    transform: translateY(-5px);
}
.texture-option {
    cursor: pointer;
    border: 3px solid transparent;
    transition: all 0.2s ease;
}
.texture-option:hover {
    border-color: #0d6efd;
}
.texture-option.selected {
    border-color: #0d6efd;
}
.loading-spinner {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 1000;
    display: flex;
    justify-content: center;
    align-items: center;
}
.spinner-content {
    background-color: white;
    padding: 20px;
    border-radius: 5px;
    text-align: center;
}
""")
    
    print(f"Created frontend CSS file at {css_file}")
    
    # Create a simple README file
    readme_file = os.path.join(frontend_dir, "README.md")
    with open(readme_file, 'w') as f:
        f.write("""# Furniture Texture Generator Frontend

This directory contains the frontend files for the Furniture Texture Generator.

## Getting Started

1. Run the Flask application from the parent directory:
   ```bash
   python frontend_integration.py
   ```

2. Open your browser and navigate to http://localhost:5000

## Features

- Upload YOLO data.yaml files to process material class labels
- Generate textures for each material class
- View and select textures for each material
- Apply selected textures to furniture parts
""")
    
    print(f"Created frontend README file at {readme_file}")

def run_frontend(frontend_dir: str, host: str = "127.0.0.1", port: int = 5000) -> None:
    """Run the Flask frontend application"""
    from frontend_integration import app
    
    print(f"Starting frontend server at http://{host}:{port}")
    app.run(host=host, port=port)

def main():
    """Main entry point for the integration script"""
    parser = argparse.ArgumentParser(description="Furniture Texture Generator Integration")
    parser.add_argument("--download", action="store_true", help="Download the dataset from Roboflow")
    parser.add_argument("--dataset", type=str, help="Path to existing dataset (skip download if provided)")
    parser.add_argument("--output-dir", type=str, default="./output", help="Output directory")
    parser.add_argument("--no-textures", action="store_true", help="Skip texture generation")
    parser.add_argument("--run-frontend", action="store_true", help="Run the Flask frontend")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to run the frontend on")
    parser.add_argument("--port", type=int, default=5000, help="Port to run the frontend on")
    
    args = parser.parse_args()
    
    try:
        # Setup directories
        dirs = setup_directories(args.output_dir)
        
        # Get dataset path
        dataset_path = None
        if args.dataset:
            dataset_path = args.dataset
            print(f"Using existing dataset at {dataset_path}")
        elif args.download:
            print("Downloading dataset from Roboflow...")
            dataset_path = download_roboflow_dataset()
        
        # Process dataset if available
        if dataset_path:
            materials_data = process_dataset(dataset_path, dirs['output'])
            
            # Generate textures if requested
            if not args.no_textures:
                texture_paths = generate_textures(materials_data, dirs['textures'])
        
        # Setup frontend
        setup_frontend(dirs['frontend'], dirs['output'])
        
        # Run frontend if requested
        if args.run_frontend:
            run_frontend(dirs['frontend'], args.host, args.port)
        
        print("Processing complete!")
        return 0
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())