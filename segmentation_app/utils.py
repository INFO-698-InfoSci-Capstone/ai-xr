import os
import cv2
import numpy as np
from PIL import Image
import io
from inference import get_model
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Replace with your Roboflow model_id and API key
MODEL_ID = "chair-eecyt/3"
API_KEY = "SN5wJh6Iq1qReYz1KzDq"

# Initialize the model - do this only once at module level
try:
    model = get_model(model_id=MODEL_ID, api_key=API_KEY)
    print(f"Model loaded successfully: {model}")
except Exception as e:
    print(f"Error loading model: {str(e)}")
    model = None

def extract_polygons_from_mask(mask):
    """Extract polygon coordinates from a binary mask using cv2.findContours."""
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    polygons = []
    for contour in contours:
        # Simplify the contour to reduce the number of points
        epsilon = 0.005 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        # Convert to list of [x,y] points
        points = [[int(point[0][0]), int(point[0][1])] for point in approx]
        if len(points) >= 3:  # Only include polygons with at least 3 points
            polygons.append(points)
    return polygons

def process_image(image_path, save_debug_images=True):
    """Process an image with the segmentation model and return mask metadata."""
    if model is None:
        raise ValueError("Model failed to initialize")
    
    try:
        # Load image and run inference
        image_pil = Image.open(image_path).convert("RGB")
        image_cv2 = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
        results = model.infer(image_cv2)
        
        # Get image dimensions
        height, width = image_cv2.shape[:2]
        
        # Define colors for different classes
        class_colors = {
            'metal': (255, 0, 0),      # Red
            'plastic': (0, 255, 0),    # Green
            'upholstery': (0, 0, 255), # Blue
        }
        
        # Initialize response data
        response_data = {
            "width": width,
            "height": height,
            "masks": []
        }
        
        # Process each prediction in the results
        for result in results:
            predictions = result.predictions if hasattr(result, 'predictions') else [result]
            
            for pred in predictions:
                class_name = pred.class_name if hasattr(pred, 'class_name') else pred.class_id
                confidence = pred.confidence if hasattr(pred, 'confidence') else 1.0
                color = class_colors.get(class_name, (255, 255, 0))
                
                if hasattr(pred, 'points') and pred.points:
                    # Extract points from prediction
                    points = pred.points
                    points_array = np.array([(int(point.x), int(point.y)) for point in points], dtype=np.int32)
                    
                    # Create mask for this instance
                    instance_mask = np.zeros((height, width), dtype=np.uint8)
                    cv2.fillPoly(instance_mask, [points_array], 1)
                    
                    # Extract polygon coordinates
                    polygons = extract_polygons_from_mask(instance_mask)
                    
                    # Add to response data
                    for polygon in polygons:
                        response_data["masks"].append({
                            "class": class_name,
                            "confidence": float(confidence),
                            "points": polygon,
                            "rgb_color": list(color)
                        })
                    
                    # Save debug images if requested
                    if save_debug_images:
                        base_filename = os.path.basename(image_path).split('.')[0]
                        mask_filename = f"{base_filename}_{class_name}_mask.png"
                        mask_path = os.path.join(os.path.dirname(image_path), mask_filename)
                        cv2.imwrite(mask_path, instance_mask * 255)
        
        return response_data
        
    except Exception as e:
        print(f"Error during inference: {str(e)}")
        raise e