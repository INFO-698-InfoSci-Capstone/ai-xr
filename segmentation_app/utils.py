import os
import cv2
import numpy as np
from PIL import Image
import io
from inference import get_model

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

def process_image(image_path):
    """Process an image with the segmentation model and return the path to the result and mask data."""
    if model is None:
        raise ValueError("Model failed to initialize")
    
    # Define output paths
    base_filename = os.path.basename(image_path).split('.')[0]
    result_filename = base_filename + '_result.jpg'
    result_path = os.path.join(os.path.dirname(image_path), result_filename)
    
    # Will store masks and metadata for each class
    masks_data = {}
    
    try:
        # Load image and run inference
        image_pil = Image.open(image_path).convert("RGB")
        image_cv2 = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
        results = model.infer(image_cv2)
        
        # Make a copy of the original image to draw on
        original_image_np = np.array(image_pil).copy()
        
        # Define colors for different classes - adjust based on your model's classes
        class_colors = {
            'metal': (255, 0, 0),      # Red
            'plastic': (0, 255, 0),    # Green
            'upholstery': (0, 0, 255), # Blue
            # Add more classes as needed
        }
        
        # Initialize class masks dictionary
        class_masks = {}
        
        # Process each prediction in the results
        for result in results:
            # Check if the result is a list (some models return lists)
            if isinstance(result, list):
                predictions = result
            else:
                # Access predictions from the response object
                predictions = result.predictions if hasattr(result, 'predictions') else [result]
            
            for pred in predictions:
                # Get class and color
                class_name = pred.class_name if hasattr(pred, 'class_name') else pred.class_id
                color = class_colors.get(class_name, (255, 255, 0))  # Default to yellow
                
                # Initialize class mask if not exists
                if class_name not in class_masks:
                    class_masks[class_name] = np.zeros(original_image_np.shape[:2], dtype=np.uint8)
                
                # Check if this is an instance segmentation prediction with points
                if hasattr(pred, 'points') and pred.points:
                    # Extract points from prediction
                    points = pred.points
                    points_array = np.array([(int(point.x), int(point.y)) for point in points], dtype=np.int32)
                    
                    # Create mask for this instance
                    instance_mask = np.zeros(original_image_np.shape[:2], dtype=np.uint8)
                    cv2.fillPoly(instance_mask, [points_array], 1)
                    
                    # Add to class mask
                    class_masks[class_name] = np.logical_or(class_masks[class_name], instance_mask).astype(np.uint8)
                    
                    # Apply the mask with transparency to the result image
                    colored_mask = np.zeros_like(original_image_np)
                    colored_mask[instance_mask == 1] = color
                    alpha = 0.5
                    cv2.addWeighted(original_image_np, 1, colored_mask, alpha, 0, original_image_np)
                
                # Get bounding box coordinates - models might provide them differently
                if hasattr(pred, 'x') and hasattr(pred, 'width'):
                    # Format: center x,y with width,height
                    x1 = int(pred.x - pred.width/2)
                    y1 = int(pred.y - pred.height/2)
                    x2 = int(pred.x + pred.width/2)
                    y2 = int(pred.y + pred.height/2)
                elif hasattr(pred, 'bbox'):
                    # Format: [x1, y1, x2, y2] or [x1, y1, w, h]
                    bbox = pred.bbox
                    if len(bbox) == 4:
                        if bbox[2] > bbox[0] and bbox[3] > bbox[1]:  # x2,y2 format
                            x1, y1, x2, y2 = map(int, bbox)
                        else:  # w,h format
                            x1, y1 = map(int, bbox[:2])
                            x2, y2 = int(x1 + bbox[2]), int(y1 + bbox[3])
                else:
                    # Skip if no bounding box info available
                    continue
                
                # Draw bounding box
                cv2.rectangle(original_image_np, (x1, y1), (x2, y2), color, 3)
                
                # Add label with confidence if available
                confidence = pred.confidence if hasattr(pred, 'confidence') else 1.0
                conf_text = f"{class_name}: {confidence:.2f}"
                
                # Improved label rendering
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 1.2
                font_thickness = 3
                text_size, _ = cv2.getTextSize(conf_text, font, font_scale, font_thickness)
                text_w, text_h = text_size
                
                # Draw background rectangle for text
                cv2.rectangle(original_image_np, (x1, y1-text_h-10), (x1+text_w, y1), color, -1)
                
                # Draw text with a black outline for better contrast
                cv2.putText(original_image_np, conf_text, (x1, y1-5), 
                            font, font_scale, (0, 0, 0), font_thickness+1)  # Black outline
                cv2.putText(original_image_np, conf_text, (x1, y1-5), 
                            font, font_scale, (255, 255, 255), font_thickness)  # White text
        
        # Save masks for each class
        for class_name, mask in class_masks.items():
            mask_filename = f"{base_filename}_{class_name}_mask.png"
            mask_path = os.path.join(os.path.dirname(image_path), mask_filename)
            cv2.imwrite(mask_path, mask * 255)  # Save as binary image (0 or 255)
            
            # Store mask data
            masks_data[class_name] = {
                'filename': 'uploads/' + mask_filename,
                'color': class_colors.get(class_name, (255, 255, 0))
            }
        
        # Convert back to RGB for saving
        result_image_rgb = cv2.cvtColor(original_image_np, cv2.COLOR_BGR2RGB)
        result_image_pil = Image.fromarray(result_image_rgb)
        
        # Save the result
        result_image_pil.save(result_path)
        print(f"Result saved to: {result_path}")
        
        return result_path, masks_data
        
    except Exception as e:
        print(f"Error during inference: {str(e)}")
        raise e