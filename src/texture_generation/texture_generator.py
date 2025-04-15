import torch
import argparse
import os
import json
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Tuple, Union

# Try importing diffusers and related libraries
DIFFUSERS_AVAILABLE = False
try:
    from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler
    DIFFUSERS_AVAILABLE = True
except ImportError:
    print("Diffusers library not available. Texture generation will be limited.")

class TextureGenerator:
    """
    Generates textures for furniture parts using Stable Diffusion.
    Works with YOLO annotations and the DynamicDescriptionGenerator.
    """
    
    def __init__(self, model_path: str = "runwayml/stable-diffusion-v1-5"):
        """
        Initialize the texture generator.
        
        Args:
            model_path: Path to the Stable Diffusion model
        """
        self.model_path = model_path
        self.pipeline = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Check if diffusers is available
        if not DIFFUSERS_AVAILABLE:
            print("WARNING: Diffusers library not available. Using placeholder textures.")
            return
        
        # Try to load the model
        try:
            print(f"Loading Stable Diffusion model from {model_path}...")
            
            # For simplicity, we'll use the basic SD pipeline without ControlNet
            from diffusers import StableDiffusionPipeline
            
            self.pipeline = StableDiffusionPipeline.from_pretrained(
                model_path, 
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None
            )
            
            if self.device == "cuda":
                self.pipeline = self.pipeline.to(self.device)
                # Enable memory optimizations
                self.pipeline.enable_vae_slicing()
                self.pipeline.enable_attention_slicing()
            
            print("Stable Diffusion model loaded successfully!")
        except Exception as e:
            print(f"Error loading Stable Diffusion model: {e}")
            print("Falling back to placeholder textures.")
    
    def generate_texture(self, 
                        prompt: str, 
                        width: int = 512, 
                        height: int = 512, 
                        num_inference_steps: int = 30, 
                        guidance_scale: float = 7.5,
                        seed: Optional[int] = None) -> Optional[Image.Image]:
        """
        Generate a texture based on a prompt.
        
        Args:
            prompt: Text prompt describing the desired texture
            width: Width of the generated image
            height: Height of the generated image
            num_inference_steps: Number of denoising steps
            guidance_scale: How closely to follow the prompt
            seed: Random seed for reproducibility
            
        Returns:
            PIL Image of the generated texture or None if generation failed
        """
        if self.pipeline is None:
            return self._generate_placeholder_texture(prompt, width, height, seed)
        
        try:
            # Set the random seed if provided
            if seed is not None:
                generator = torch.Generator(device=self.device).manual_seed(seed)
            else:
                generator = None
            
            # Generate the image
            output = self.pipeline(
                prompt=prompt,
                width=width,
                height=height,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                generator=generator
            )
            
            # Get the image from the output
            image = output.images[0]
            
            return image
        except Exception as e:
            print(f"Error generating texture with prompt '{prompt}': {e}")
            return self._generate_placeholder_texture(prompt, width, height, seed)
    
    def _generate_placeholder_texture(self, 
                                     prompt: str, 
                                     width: int = 512, 
                                     height: int = 512,
                                     seed: Optional[int] = None) -> Image.Image:
        """
        Generate a placeholder texture when Stable Diffusion is not available.
        
        Args:
            prompt: Text prompt describing the desired texture
            width: Width of the image
            height: Height of the image
            seed: Random seed for reproducibility
            
        Returns:
            PIL Image of a placeholder texture
        """
        # Set random seed for reproducibility
        if seed is not None:
            np.random.seed(seed)
        
        # Extract color keywords from the prompt
        color_mapping = {
            "red": [255, 0, 0],
            "green": [0, 255, 0],
            "blue": [0, 0, 255],
            "yellow": [255, 255, 0],
            "cyan": [0, 255, 255],
            "magenta": [255, 0, 255],
            "white": [255, 255, 255],
            "black": [0, 0, 0],
            "gray": [128, 128, 128],
            "brown": [165, 42, 42],
            "orange": [255, 165, 0],
            "purple": [128, 0, 128],
            "pink": [255, 192, 203],
            "gold": [255, 215, 0],
            "silver": [192, 192, 192]
        }
        
        # Default color and texture pattern
        base_color = np.array([200, 200, 200])  # Light gray default
        pattern_type = "noise"  # Default pattern
        
        # Extract color from prompt
        for color_name, color_value in color_mapping.items():
            if color_name in prompt.lower():
                base_color = np.array(color_value)
                break
        
        # Extract pattern type from prompt
        pattern_mapping = {
            "noise": lambda x, y: np.random.rand(),
            "gradient": lambda x, y: x / width,
            "stripes": lambda x, y: 0.5 + 0.5 * np.sin(x * 20 / width),
            "checkered": lambda x, y: (x // 64 + y // 64) % 2,
            "dots": lambda x, y: 1 if ((x % 64 - 32)**2 + (y % 64 - 32)**2) < 400 else 0
        }
        
        for pattern_name in pattern_mapping.keys():
            if pattern_name in prompt.lower():
                pattern_type = pattern_name
                break
        
        # Create the base image
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Apply the pattern
        pattern_func = pattern_mapping.get(pattern_type, pattern_mapping["noise"])
        
        for y in range(height):
            for x in range(width):
                # Get pattern value at this position
                pattern_value = pattern_func(x, y)
                
                # Mix base color with pattern
                pixel_color = base_color * (0.5 + 0.5 * pattern_value)
                image[y, x] = np.clip(pixel_color, 0, 255).astype(np.uint8)
        
        # Convert to PIL Image
        pil_image = Image.fromarray(image)
        
        return pil_image
    
    def generate_textures_for_material(self, 
                                      material: str, 
                                      texture_suggestions: List[str],
                                      output_dir: str = "./textures",
                                      size: Tuple[int, int] = (512, 512)) -> List[str]:
        """
        Generate textures for a material based on suggestions.
        
        Args:
            material: Material name
            texture_suggestions: List of texture suggestions
            output_dir: Directory to save generated textures
            size: Size of generated textures (width, height)
            
        Returns:
            List of paths to generated texture images
        """
        # Create output directory if it doesn't exist
        material_dir = os.path.join(output_dir, material)
        os.makedirs(material_dir, exist_ok=True)
        
        generated_paths = []
        
        # Generate textures for each suggestion
        for idx, suggestion in enumerate(texture_suggestions):
            # Create a descriptive prompt
            prompt = f"Seamless texture of {suggestion}, for furniture, highly detailed, material sample"
            
            # Generate the texture
            texture_image = self.generate_texture(
                prompt=prompt,
                width=size[0],
                height=size[1],
                seed=idx  # Use index as seed for reproducibility
            )
            
            if texture_image:
                # Save the texture
                texture_path = os.path.join(material_dir, f"{material}_{idx+1}.png")
                texture_image.save(texture_path)
                generated_paths.append(texture_path)
                print(f"Generated texture {idx+1}/{len(texture_suggestions)} for {material}")
            else:
                print(f"Failed to generate texture {idx+1}/{len(texture_suggestions)} for {material}")
        
        return generated_paths
    
    def process_materials_json(self, json_path: str, output_dir: str = "./textures") -> Dict:
        """
        Process a materials JSON file and generate textures for each material.
        
        Args:
            json_path: Path to JSON file with material descriptions
            output_dir: Directory to save generated textures
            
        Returns:
            Dictionary mapping materials to lists of texture paths
        """
        # Load the JSON file
        with open(json_path, 'r') as f:
            materials_data = json.load(f)
        
        texture_paths = {}
        
        # Process each material
        for material_data in materials_data.get('materials', []):
            material_name = material_data.get('name')
            texture_suggestions = material_data.get('texture_suggestions', [])
            
            if not material_name or not texture_suggestions:
                continue
            
            print(f"\nGenerating textures for {material_name}...")
            paths = self.generate_textures_for_material(
                material=material_name,
                texture_suggestions=texture_suggestions,
                output_dir=output_dir
            )
            
            texture_paths[material_name] = paths
        
        # Save the texture paths to a JSON file
        textures_json = {
            'texture_paths': texture_paths,
            'version': '1.0'
        }
        
        textures_json_path = os.path.join(output_dir, 'texture_paths.json')
        with open(textures_json_path, 'w') as f:
            json.dump(textures_json, f, indent=2)
        
        print(f"\nSaved texture paths to {textures_json_path}")
        
        return texture_paths
    
    def create_texture_preview(self, 
                              material_name: str, 
                              texture_paths: List[str],
                              output_path: Optional[str] = None) -> Optional[str]:
        """
        Create a preview image showing all textures for a material.
        
        Args:
            material_name: Name of the material
            texture_paths: List of paths to texture images
            output_path: Path to save the preview image
            
        Returns:
            Path to the preview image, or None if creation failed
        """
        if not texture_paths:
            print(f"No textures available for {material_name}")
            return None
        
        try:
            # Determine grid size
            num_textures = len(texture_paths)
            cols = min(num_textures, 3)
            rows = (num_textures + cols - 1) // cols
            
            # Create the figure
            fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 4))
            fig.suptitle(f"Texture Options for {material_name}", fontsize=16)
            
            # Make axes a 2D array for consistency
            if rows == 1 and cols == 1:
                axes = np.array([[axes]])
            elif rows == 1:
                axes = np.array([axes])
            elif cols == 1:
                axes = np.array([[ax] for ax in axes])
            
            # Add textures to the grid
            for i, texture_path in enumerate(texture_paths):
                row = i // cols
                col = i % cols
                
                # Load the texture
                texture = Image.open(texture_path)
                
                # Display the texture
                axes[row, col].imshow(texture)
                axes[row, col].set_title(f"Option {i+1}")
                axes[row, col].axis('off')
            
            # Hide empty subplots
            for i in range(num_textures, rows * cols):
                row = i // cols
                col = i % cols
                axes[row, col].axis('off')
            
            # Set tight layout
            plt.tight_layout(rect=[0, 0, 1, 0.96])  # Leave room for the title
            
            # Save the preview
            if output_path is None:
                output_dir = os.path.dirname(texture_paths[0])
                output_path = os.path.join(output_dir, f"{material_name}_preview.png")
            
            plt.savefig(output_path, dpi=100, bbox_inches='tight')
            plt.close()
            
            print(f"Created texture preview for {material_name} at {output_path}")
            return output_path
        except Exception as e:
            print(f"Error creating texture preview for {material_name}: {e}")
            return None


def main():
    """Example usage of the TextureGenerator"""
    parser = argparse.ArgumentParser(description="Generate textures for furniture materials")
    parser.add_argument("--materials-json", type=str, required=True, help="Path to materials JSON file")
    parser.add_argument("--output-dir", type=str, default="./textures", help="Output directory for textures")
    parser.add_argument("--model-path", type=str, default="runwayml/stable-diffusion-v1-5", help="Stable Diffusion model path")
    
    args = parser.parse_args()
    
    # Initialize the generator
    generator = TextureGenerator(model_path=args.model_path)
    
    # Process the materials JSON
    texture_paths = generator.process_materials_json(
        json_path=args.materials_json,
        output_dir=args.output_dir
    )
    
    # Create previews for each material
    for material_name, paths in texture_paths.items():
        generator.create_texture_preview(material_name, paths)
    
    print("\nAll textures generated successfully!")


if __name__ == "__main__":
    main()