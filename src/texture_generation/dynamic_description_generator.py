import yaml
import json
import os
from typing import Dict, List, Tuple, Optional
import numpy as np
from PIL import Image
import torch

# Check if transformers is available
TRANSFORMERS_AVAILABLE = False
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    print("Transformers library not available. Using fallback descriptions.")

class DynamicDescriptionGenerator:
    """
    Generates dynamic descriptions for furniture part materials and suggests appropriate textures.
    Compatible with YOLO annotations and Stable Diffusion texture generation.
    """
    
    def __init__(self, use_ai_model: bool = True, cache_file: str = "material_descriptions.json"):
        """
        Initialize the description generator.
        
        Args:
            use_ai_model: Whether to use an AI model for enhanced descriptions
            cache_file: Path to cache file for storing generated descriptions
        """
        self.cache_file = cache_file
        self.descriptions = {}
        self.texture_suggestions = {}
        self.ai_model = None
        
        # Load cached descriptions if available
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                    self.descriptions = cache_data.get('descriptions', {})
                    self.texture_suggestions = cache_data.get('texture_suggestions', {})
                print(f"Loaded {len(self.descriptions)} cached descriptions and {len(self.texture_suggestions)} texture suggestions")
            except Exception as e:
                print(f"Error loading cached data: {e}")
        
        # Initialize AI model if requested and available
        self.use_ai_model = use_ai_model and TRANSFORMERS_AVAILABLE
        if self.use_ai_model:
            try:
                # Using a smaller model for efficiency
                self.ai_model = pipeline("text-generation", model="distilgpt2", max_length=100)
                print("AI model loaded successfully for enhanced descriptions")
            except Exception as e:
                print(f"Error loading AI model: {e}")
                self.use_ai_model = False
        
        # Base material descriptions
        self.base_descriptions = {
            # Materials
            "metal": "Rigid structural material with high strength and durability, commonly used for frames and supports.",
            "plastic": "Lightweight synthetic material that can be molded into various shapes, often used for chair components.",
            "wood": "Natural material with warm aesthetic, used for frames, legs, and surfaces of furniture.",
            "glass": "Transparent rigid material used for tabletops and decorative elements.",
            "leather": "Durable animal hide material with premium feel, used for upholstery.",
            "fabric": "Woven textile material used for upholstery and covering cushioned components.",
            "upholstery": "Soft, padded covering material that provides comfort and aesthetics to seating surfaces.",
            "mesh": "Breathable net-like material used for ergonomic support in chair backs and seats.",
            "rubber": "Flexible, elastic material used for cushioning and grips.",
            "ceramic": "Hard, heat-resistant material used for decorative elements or tabletops.",
            "marble": "Natural stone with distinctive patterns used for high-end tabletops and surfaces.",
            "velvet": "Soft, plush fabric with a dense pile used for premium upholstery.",
            "wicker": "Woven plant material used for decorative furniture with natural aesthetics.",
            "rattan": "Natural reed-like material woven to create furniture frames and surfaces.",
            "chrome": "Polished metal finish with high reflectivity used for decorative elements.",
            "composite": "Engineered material combining multiple substances for specific properties.",
            
            # Furniture parts
            "leg": "Supporting structural element that elevates furniture from the floor.",
            "arm": "Side support that provides resting place for a person's arms.",
            "seat": "Horizontal surface designed for sitting.",
            "back": "Vertical or angled support that provides back support.",
            "cushion": "Soft padded component that adds comfort.",
            "frame": "Main structural component that holds the furniture together.",
            "base": "Bottom structural component that provides stability.",
            "wheel": "Rotating component that allows furniture to move.",
            "table": "Flat-surfaced piece of furniture with legs, used for various purposes.",
            "drawer": "Storage compartment that can be pulled out horizontally.",
            "handle": "Component used to open doors or drawers.",
            "surface": "Top horizontal plane of a table or desk."
        }
        
        # Texture suggestion mappings
        self.default_texture_suggestions = {
            "metal": ["brushed metal", "polished chrome", "dark steel", "bronze finish", "copper patina"],
            "plastic": ["matte plastic", "glossy finish", "textured plastic", "faux wood grain", "transparent"],
            "wood": ["natural oak", "dark walnut", "cherry wood", "maple finish", "reclaimed wood"],
            "glass": ["clear glass", "frosted glass", "tinted glass", "tempered glass", "etched pattern"],
            "leather": ["black leather", "brown leather", "white leather", "distressed leather", "faux leather"],
            "fabric": ["woven textile", "cotton blend", "microfiber", "canvas", "patterned fabric"],
            "upholstery": ["plush velvet", "linen fabric", "textured weave", "suede finish", "patterned upholstery"],
            "mesh": ["breathable mesh", "ergonomic weave", "nylon mesh", "structured support mesh", "patterned mesh"],
            "rubber": ["textured rubber", "smooth silicone", "non-slip finish", "matte black", "colored rubber"],
            "marble": ["white carrara", "black marble", "veined pattern", "polished finish", "matte texture"],
            "velvet": ["crushed velvet", "smooth velvet", "plush texture", "iridescent sheen", "patterned velvet"]
        }
    
    def get_material_description(self, material_class: str) -> str:
        """
        Get a description for a material class.
        
        Args:
            material_class: The material class name (e.g., "metal", "plastic")
            
        Returns:
            A description of the material
        """
        # Check if we already have a cached description
        if material_class in self.descriptions:
            return self.descriptions[material_class]
        
        # Check if we have a base description
        material_lower = material_class.lower()
        if material_lower in self.base_descriptions:
            description = self.base_descriptions[material_lower]
        else:
            # Generate a description using AI if available
            if self.use_ai_model:
                try:
                    prompt = f"A brief description of {material_class} as used in furniture:"
                    result = self.ai_model(prompt, do_sample=True, top_k=50, temperature=0.7)
                    ai_text = result[0]['generated_text'].replace(prompt, "").strip()
                    # Use just the first sentence from AI generation
                    description = ai_text.split('.')[0] + '.'
                except Exception as e:
                    print(f"Error generating AI description for {material_class}: {e}")
                    description = f"A type of material used in furniture identified as {material_class}."
            else:
                # Fallback for when AI is not available
                description = f"A type of material used in furniture identified as {material_class}."
        
        # Cache the description
        self.descriptions[material_class] = description
        self._save_cache()
        
        return description
    
    def get_texture_suggestions(self, material_class: str, count: int = 5) -> List[str]:
        """
        Get texture suggestions for a material class.
        
        Args:
            material_class: The material class name
            count: Number of suggestions to return
            
        Returns:
            A list of texture suggestions
        """
        # Check if we already have cached suggestions
        if material_class in self.texture_suggestions:
            suggestions = self.texture_suggestions[material_class]
            return suggestions[:count]
        
        # Check if we have default suggestions
        material_lower = material_class.lower()
        if material_lower in self.default_texture_suggestions:
            suggestions = self.default_texture_suggestions[material_lower]
        else:
            # Find the closest material class
            closest_match = self._find_closest_material(material_lower)
            if closest_match:
                suggestions = self.default_texture_suggestions[closest_match]
            else:
                # Generic suggestions if no match found
                suggestions = [
                    f"{material_class} natural finish",
                    f"{material_class} dark finish",
                    f"{material_class} light color",
                    f"textured {material_class}",
                    f"polished {material_class}"
                ]
        
        # Cache the suggestions
        self.texture_suggestions[material_class] = suggestions
        self._save_cache()
        
        return suggestions[:count]
    
    def _find_closest_material(self, material: str) -> Optional[str]:
        """Find the closest matching material from our defaults"""
        for key in self.default_texture_suggestions.keys():
            if key in material or material in key:
                return key
        return None
    
    def _save_cache(self) -> None:
        """Save descriptions and suggestions to cache file"""
        try:
            cache_data = {
                'descriptions': self.descriptions,
                'texture_suggestions': self.texture_suggestions
            }
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def process_yolo_annotations(self, data_yaml_path: str, labels_dir: str, sample_image_path: str = None) -> Dict:
        """
        Process YOLO annotations to extract materials and generate descriptions.
        
        Args:
            data_yaml_path: Path to the YOLO data.yaml file
            labels_dir: Directory containing YOLO label files
            sample_image_path: Optional path to a sample image for visualization
            
        Returns:
            Dictionary of materials with descriptions and texture suggestions
        """
        # Load class names from YOLO data.yaml
        class_names = []
        if os.path.exists(data_yaml_path):
            with open(data_yaml_path, 'r') as file:
                data_yaml = yaml.safe_load(file)
                class_names = data_yaml.get('names', [])
        
        if not class_names:
            print("Warning: No class names found in data.yaml")
            return {}
        
        # Process each class and generate descriptions and texture suggestions
        results = {}
        for idx, class_name in enumerate(class_names):
            description = self.get_material_description(class_name)
            texture_suggestions = self.get_texture_suggestions(class_name)
            
            results[class_name] = {
                'id': idx,
                'name': class_name,
                'description': description,
                'texture_suggestions': texture_suggestions
            }
        
        return results
    
    def generate_frontend_json(self, class_data: Dict) -> str:
        """
        Generate a JSON string suitable for frontend consumption.
        
        Args:
            class_data: Dictionary of class data from process_yolo_annotations
            
        Returns:
            JSON string for frontend
        """
        frontend_data = {
            'materials': list(class_data.values()),
            'timestamp': self._get_timestamp(),
            'version': '1.0'
        }
        
        return json.dumps(frontend_data, indent=2)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp string"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    """Example usage of the DynamicDescriptionGenerator"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate dynamic descriptions for furniture materials")
    parser.add_argument("--data-yaml", type=str, required=True, help="Path to YOLO data.yaml file")
    parser.add_argument("--labels-dir", type=str, required=True, help="Directory containing YOLO label files")
    parser.add_argument("--output", type=str, default="material_descriptions.json", help="Output JSON file path")
    parser.add_argument("--no-ai", action="store_true", help="Disable AI-enhanced descriptions")
    
    args = parser.parse_args()
    
    # Initialize the generator
    generator = DynamicDescriptionGenerator(use_ai_model=not args.no_ai)
    
    # Process YOLO annotations
    class_data = generator.process_yolo_annotations(args.data_yaml, args.labels_dir)
    
    # Print results
    print("\nGenerated Material Descriptions:")
    for class_name, data in class_data.items():
        print(f"\n{class_name} (ID: {data['id']}):")
        print(f"  Description: {data['description']}")
        print(f"  Texture Suggestions: {', '.join(data['texture_suggestions'])}")
    
    # Generate frontend JSON
    frontend_json = generator.generate_frontend_json(class_data)
    
    # Save to file
    with open(args.output, 'w') as f:
        f.write(frontend_json)
    
    print(f"\nSaved frontend JSON to {args.output}")


if __name__ == "__main__":
    main()