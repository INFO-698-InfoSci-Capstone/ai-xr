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
from texture_generation.dynamic_description_generator import DynamicDescriptionGenerator
from texture_generation.texture_generator import TextureGenerator
from texture_generation.annotation_integration import AnnotationInterface
from texture_generation.roboflow_loader import download_roboflow_dataset
from texture_generation.segmentation import load_classlabels
import frontend_integration

def setup_directories(base_dir: str) -> Dict[str, str]:
    """Set up the necessary directories for the project"""
    dirs = {
        'base': base_dir,
        'output': os.path.join(base_dir, 'output'),
        'textures': os.path.join(base_dir, 'textures'),
        'uploads': os.path.join(base_dir, 'uploads'),
        'frontend': os.path.join(base_dir, 'frontend')
    }
    
    # Create directories
    for path in dirs.values():
        os.makedirs(path, exist_ok=True)
    
    return dirs

def copy_frontend_files(frontend_dir: str) -> None:
    """Copy frontend files to the frontend directory"""
    # Create templates and static directories
    templates_dir = os.path.join(frontend_dir, 'templates')
    static_dir = os.path.join(frontend_dir, 'static')
    
    os.makedirs(templates_dir, exist_ok=True)
    os.makedirs(static_dir, exist_ok=True)
    
    # Copy index.html template
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_template = os.path.join(script_dir, 'templates', 'index.html')
    target_template = os.path.join(templates_dir, 'index.html')
    
    if os.path.exists(source_template):
        shutil.copy2(source_template, target_template)
        print(f"Copied index.html template to {target_template}")
    else:
        print(f"Warning: Template file not found at {source_template}")

def run_frontend(host: str = "127.0.0.1", port: int = 5000, debug: bool = False, 
                download_dataset: bool = False) -> None:
    """Run the frontend application"""
    args = argparse.Namespace(
        host=host,
        port=port,
        debug=debug,
        download_dataset=download_dataset
    )
    
    frontend_integration.main(args)

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
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    
    args = parser.parse_args()
    
    try:
        # Setup directories
        dirs = setup_directories(args.output_dir)
        
        # Copy frontend files
        copy_frontend_files(dirs['frontend'])
        
        # Run frontend if requested
        if args.run_frontend:
            run_frontend(
                host=args.host, 
                port=args.port, 
                debug=args.debug, 
                download_dataset=args.download
            )
        else:
            # Initialize the annotation interface
            annotation_interface = AnnotationInterface(output_dir=dirs['output'])
            
            # Get dataset path
            dataset_path = None
            if args.dataset:
                dataset_path = args.dataset
                annotation_interface.set_dataset_path(dataset_path)
                print(f"Using existing dataset at {dataset_path}")
            elif args.download:
                print("Downloading dataset from Roboflow...")
                dataset_path = annotation_interface.download_dataset()
            
            # Process sample images if dataset is available
            if dataset_path:
                # Get images from the dataset
                test_dir = os.path.join(dataset_path, "test")
                images_dir = os.path.join(test_dir, "images")
                
                if os.path.exists(images_dir):
                    image_files = sorted([
                        os.path.join(images_dir, f) for f in os.listdir(images_dir)
                        if f.endswith(('.jpg', '.jpeg', '.png'))
                    ])
                    
                    if image_files:
                        for img_file in image_files[:3]:  # Process up to 3 images
                            print(f"Processing {img_file}...")
                            try:
                                result = annotation_interface.process_image(img_file)
                                print(f"  Found {len(result['masks'])} masks")
                            except Exception as e:
                                print(f"  Error: {e}")
                
                # Get all materials
                materials_data = annotation_interface.get_all_materials()
                print(f"Generated information for {len(materials_data['materials'])} materials")
                
                # Generate textures if requested
                if not args.no_textures:
                    # Initialize the texture generator
                    texture_generator = TextureGenerator()
                    
                    # Process the materials data
                    materials_json_path = os.path.join(dirs['output'], 'material_descriptions.json')
                    texture_paths = texture_generator.process_materials_json(
                        json_path=materials_json_path,
                        output_dir=dirs['textures']
                    )
                    
                    # Create previews for each material
                    previews = {}
                    for material_name, paths in texture_paths.items():
                        preview_path = texture_generator.create_texture_preview(material_name, paths)
                        if preview_path:
                            previews[material_name] = preview_path
                    
                    print(f"Generated textures for {len(texture_paths)} materials")
        
        print("Processing complete!")
        return 0
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())