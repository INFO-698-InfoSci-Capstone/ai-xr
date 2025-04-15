import os
import sys
import json
import yaml
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional, Any

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import existing modules 
from texture_generation.roboflow_loader import download_roboflow_dataset
from texture_generation.segmentation import load_classlabels, read_yolo_seg_file, display_sample_with_masks

class AnnotationInterface:
    """
    Interface between the existing annotation code and the frontend.
    Provides methods to work with Roboflow datasets, YOLO annotations,
    and segmentation masks.
    """
    
    def __init__(self, output_dir: str = "./output"):
        """
        Initialize the annotation interface.
        
        Args:
            output_dir: Directory to store output files
        """
        self.output_dir = output_dir
        self.dataset_path = None
        self.class_names = []
        self.annotation_results = {}
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
    
    def download_dataset(self) -> str:
        """
        Download a dataset from Roboflow.
        
        Returns:
            Path to the downloaded dataset
        """
        print("Downloading dataset from Roboflow...")
        self.dataset_path = download_roboflow_dataset()
        print(f"Dataset downloaded to {self.dataset_path}")
        
        # Load class labels and store them
        self._load_class_names()
        
        return self.dataset_path
    
    def set_dataset_path(self, path: str) -> None:
        """
        Set the dataset path manually.
        
        Args:
            path: Path to the YOLO dataset
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Dataset path not found: {path}")
        
        self.dataset_path = path
        print(f"Dataset path set to {self.dataset_path}")
        
        # Load class labels and store them
        self._load_class_names()
    
    def _load_class_names(self) -> None:
        """Load class names from the dataset's data.yaml file"""
        if not self.dataset_path:
            print("No dataset path set. Cannot load class names.")
            return
        
        data_yaml_path = os.path.join(self.dataset_path, "data.yaml")
        
        if not os.path.exists(data_yaml_path):
            print(f"data.yaml not found at {data_yaml_path}")
            return
        
        try:
            with open(data_yaml_path, 'r') as f:
                data_yaml = yaml.safe_load(f)
                self.class_names = data_yaml.get('names', [])
                
                if self.class_names:
                    print(f"Loaded {len(self.class_names)} class names from data.yaml")
                    for idx, name in enumerate(self.class_names):
                        print(f"  {idx}: {name}")
                else:
                    print("No class names found in data.yaml")
        except Exception as e:
            print(f"Error loading class names: {e}")
    
    def process_image(self, image_path: str) -> Dict[str, Any]:
        """
        Process an image with YOLO annotations.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary containing image information, masks, and class IDs
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Load image
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_height, img_width = image.shape[:2]
        
        # Get the label file path
        img_name = os.path.basename(image_path)
        base_name = os.path.splitext(img_name)[0]
        
        # Try to find the label file in multiple possible locations
        label_paths = [
            os.path.join(os.path.dirname(image_path), base_name + '.txt'),  # Same directory
            os.path.join(os.path.dirname(image_path), '..', 'labels', base_name + '.txt'),  # labels dir parallel to images
            os.path.join(self.dataset_path, 'labels', base_name + '.txt') if self.dataset_path else None  # dataset labels dir
        ]
        
        label_path = None
        for path in label_paths:
            if path and os.path.exists(path):
                label_path = path
                break
        
        if not label_path:
            raise FileNotFoundError(f"Label file not found for image: {image_path}")
        
        # Read YOLO segmentation file
        masks, class_ids = read_yolo_seg_file(label_path, img_width, img_height)
        
        if not masks:
            raise ValueError(f"No masks found in label file: {label_path}")
        
        # Create visualization
        visualization = self._create_visualization(image, masks, class_ids)
        
        # Save visualization
        vis_path = os.path.join(self.output_dir, f"{base_name}_segmentation.png")
        plt.imsave(vis_path, visualization)
        
        # Convert masks to base64 or other format for frontend
        mask_data = []
        for i, (mask, class_id) in enumerate(zip(masks, class_ids)):
            # Get class name
            class_name = self.class_names[class_id] if class_id < len(self.class_names) else f"class_{class_id}"
            
            # Find mask center
            y_indices, x_indices = np.where(mask > 0)
            if len(y_indices) > 0 and len(x_indices) > 0:
                center_y = int(np.mean(y_indices))
                center_x = int(np.mean(x_indices))
            else:
                center_y, center_x = 0, 0
            
            # Create mask data
            mask_data.append({
                'id': i,
                'class_id': int(class_id),
                'class_name': class_name,
                'center': [center_x, center_y],
                'area': int(np.sum(mask)),
                'mask_file': f"{base_name}_mask_{i}.png"
            })
            
            # Save individual mask
            mask_path = os.path.join(self.output_dir, f"{base_name}_mask_{i}.png")
            plt.imsave(mask_path, mask, cmap='gray')
        
        # Store the results
        self.annotation_results[base_name] = {
            'image_path': image_path,
            'visualization_path': vis_path,
            'masks': mask_data
        }
        
        return self.annotation_results[base_name]
    
    def _create_visualization(self, image: np.ndarray, masks: List[np.ndarray], class_ids: List[int]) -> np.ndarray:
        """
        Create a visualization of the segmentation masks.
        
        Args:
            image: Original image
            masks: List of segmentation masks
            class_ids: List of class IDs
            
        Returns:
            Visualization image with masks overlaid
        """
        # Create figure
        plt.figure(figsize=(12, 8))
        plt.imshow(image)
        
        # Define colors for masks
        colors = plt.cm.tab20(np.linspace(0, 1, max(len(masks), 1)))
        
        # Draw masks with different colors
        for i, (mask, class_id) in enumerate(zip(masks, class_ids)):
            color_mask = np.zeros(image.shape[:2] + (4,))  # RGBA
            color_rgba = colors[i % len(colors)]
            
            # Set color and alpha for mask area
            for c in range(3):
                color_mask[:,:,c] = mask * color_rgba[c]
            color_mask[:,:,3] = mask * 0.5  # Set alpha
            
            plt.imshow(color_mask)
            
            # Get class name and add label
            class_name = self.class_names[class_id] if class_id < len(self.class_names) else f"class_{class_id}"
            
            # Find mask center for label placement
            y_indices, x_indices = np.where(mask > 0)
            if len(y_indices) > 0 and len(x_indices) > 0:
                center_y = int(np.mean(y_indices))
                center_x = int(np.mean(x_indices))
                
                # Add label
                plt.text(center_x, center_y, class_name, 
                         color='white', fontsize=12, ha='center', va='center',
                         bbox=dict(facecolor='black', alpha=0.7))
        
        plt.title(f"Segmentation")
        plt.axis('off')
        plt.tight_layout()
        
        # Convert the plot to a numpy array
        plt.savefig("temp_vis.png", bbox_inches='tight', pad_inches=0.1)
        plt.close()
        
        # Read the saved image
        visualization = cv2.imread("temp_vis.png")
        visualization = cv2.cvtColor(visualization, cv2.COLOR_BGR2RGB)
        
        # Clean up
        if os.path.exists("temp_vis.png"):
            os.remove("temp_vis.png")
        
        return visualization
    
    def get_material_info(self, class_id: int) -> Dict[str, Any]:
        """
        Get information about a material class.
        
        Args:
            class_id: The class ID
            
        Returns:
            Dictionary with material information
        """
        # Get class name
        if class_id < len(self.class_names):
            class_name = self.class_names[class_id]
        else:
            class_name = f"class_{class_id}"
        
        # Define material properties based on class name
        material_properties = {
            "metal": {
                "description": "Rigid structural material with high strength and durability, commonly used for frames and supports.",
                "texture_suggestions": ["brushed metal", "polished chrome", "dark steel", "bronze finish", "copper patina"]
            },
            "plastic": {
                "description": "Lightweight synthetic material that can be molded into various shapes, often used for chair components.",
                "texture_suggestions": ["matte plastic", "glossy finish", "textured plastic", "faux wood grain", "transparent"]
            },
            "upholstery": {
                "description": "Soft, padded covering material that provides comfort and aesthetics to seating surfaces.",
                "texture_suggestions": ["plush velvet", "linen fabric", "textured weave", "suede finish", "patterned upholstery"]
            },
            "wood": {
                "description": "Natural material with warm aesthetic, used for frames, legs, and surfaces of furniture.",
                "texture_suggestions": ["natural oak", "dark walnut", "cherry wood", "maple finish", "reclaimed wood"]
            },
            "glass": {
                "description": "Transparent rigid material used for tabletops and decorative elements.",
                "texture_suggestions": ["clear glass", "frosted glass", "tinted glass", "tempered glass", "etched pattern"]
            },
            "leather": {
                "description": "Durable animal hide material with premium feel, used for upholstery.",
                "texture_suggestions": ["black leather", "brown leather", "white leather", "distressed leather", "faux leather"]
            },
            "fabric": {
                "description": "Woven textile material used for upholstery and covering cushioned components.",
                "texture_suggestions": ["woven textile", "cotton blend", "microfiber", "canvas", "patterned fabric"]
            }
        }
        
        # Check if class name is in our predefined materials
        material_info = None
        for key, info in material_properties.items():
            if key in class_name.lower():
                material_info = info
                break
        
        # If not found, use a generic description
        if not material_info:
            material_info = {
                "description": f"A material used in furniture identified as {class_name}.",
                "texture_suggestions": [f"{class_name} texture", f"{class_name} pattern", f"{class_name} finish", 
                                       f"{class_name} surface", f"{class_name} material"]
            }
        
        # Add class information
        material_info["id"] = class_id
        material_info["name"] = class_name
        
        return material_info
    
    def get_all_materials(self) -> Dict[str, Any]:
        """
        Get information about all detected materials.
        
        Returns:
            Dictionary with all material information
        """
        # Get unique class IDs from all results
        class_ids = set()
        for result in self.annotation_results.values():
            for mask in result['masks']:
                class_ids.add(mask['class_id'])
        
        # Get material information for each class
        materials = []
        for class_id in sorted(class_ids):
            materials.append(self.get_material_info(class_id))
        
        # Create materials data
        materials_data = {
            'materials': materials,
            'timestamp': self._get_timestamp(),
            'version': '1.0'
        }
        
        # Save to file
        output_path = os.path.join(self.output_dir, 'material_descriptions.json')
        with open(output_path, 'w') as f:
            json.dump(materials_data, f, indent=2)
        
        return materials_data
    
    def _get_timestamp(self) -> str:
        """Get current timestamp string"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Example usage
if __name__ == "__main__":
    interface = AnnotationInterface(output_dir="./output")
    
    # Download or set dataset path
    if len(sys.argv) > 1:
        interface.set_dataset_path(sys.argv[1])
    else:
        interface.download_dataset()
    
    # Process sample images from the dataset
    if interface.dataset_path:
        # Get images from the dataset
        test_dir = os.path.join(interface.dataset_path, "test")
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
                        result = interface.process_image(img_file)
                        print(f"  Found {len(result['masks'])} masks")
                    except Exception as e:
                        print(f"  Error: {e}")
            else:
                print("No image files found")
        else:
            print(f"Images directory not found: {images_dir}")
    
    # Get all materials
    materials_data = interface.get_all_materials()
    print(f"Generated information for {len(materials_data['materials'])} materials")