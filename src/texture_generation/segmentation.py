import os
import glob
import yaml
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image


filepath = ''

def load_classlabels(filepath):
    # Define the dataset path
    # dataset_path = "/content/chair-1"
    test_dir = os.path.join(filepath, "test")
    images_dir = os.path.join(test_dir, "images")
    labels_dir = os.path.join(test_dir, "labels")

    # Define output path
    output_path = "./texture_output"
    os.makedirs(output_path, exist_ok=True)

    # Print directory structure
    print(f"Dataset path: {filepath}")
    print(f"Test images path: {images_dir}")
    print(f"Test labels path: {labels_dir}")

    # List images and labels
    image_files = sorted(glob.glob(os.path.join(images_dir, "*.jpg")) +
                        glob.glob(os.path.join(images_dir, "*.jpeg")) +
                        glob.glob(os.path.join(images_dir, "*.png")))
    label_files = sorted(glob.glob(os.path.join(labels_dir, "*.txt")))

    print(f"\nFound {len(image_files)} image files")
    print(f"Found {len(label_files)} label files")

    # Load class names from data.yaml
    data_yaml_path = os.path.join(filepath, "data.yaml")
    class_names = []
    if os.path.exists(data_yaml_path):
        with open(data_yaml_path, 'r') as file:
            data_yaml = yaml.safe_load(file)
            class_names = data_yaml.get('names', [])
            print("\nClass names from data.yaml:")
            for idx, name in enumerate(class_names):
                print(f"{idx}: {name}")
    else:
        print("Warning: data.yaml not found. Class names will be numbered.")

    # If no class names were found, create a default list
    if not class_names:
        class_names = [f"class_{i}" for i in range(80)]  # Default to 80 classes (COCO standard)
    
    display_sample_with_masks(class_names,image_files,labels_dir)

def read_yolo_seg_file(file_path, img_width, img_height):
    """Read YOLO segmentation file and return list of masks and class ids"""
    masks = []
    class_ids = []

    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 5:  # Need at least class_id and 2 points (4 values)
                continue

            class_id = int(parts[0])
            class_ids.append(class_id)

            # Convert polygon points from normalized to absolute coordinates
            polygon = []
            for i in range(1, len(parts), 2):
                if i+1 < len(parts):
                    x = float(parts[i]) * img_width
                    y = float(parts[i+1]) * img_height
                    polygon.append((x, y))

            # Create mask from polygon
            mask = np.zeros((img_height, img_width), dtype=np.uint8)
            polygon_np = np.array(polygon, np.int32).reshape((-1, 1, 2))
            cv2.fillPoly(mask, [polygon_np], 1)
            masks.append(mask)

    return masks, class_ids

# Display a sample image with masks
def display_sample_with_masks(class_names,image_files,labels_dir,img_idx=0):
    if len(image_files) <= img_idx:
        print("No image found at the specified index")
        return None, None, None

    img_path = image_files[img_idx]
    img_name = os.path.basename(img_path)
    base_name = os.path.splitext(img_name)[0]
    label_path = os.path.join(labels_dir, base_name + '.txt')

    if not os.path.exists(label_path):
        print(f"Label file not found: {label_path}")
        return None, None, None

    # Load image
    image = cv2.imread(img_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_height, img_width = image.shape[:2]

    # Load masks
    masks, class_ids = read_yolo_seg_file(label_path, img_width, img_height)

    # Display image with masks
    plt.figure(figsize=(12, 8))
    plt.imshow(image)

    # Draw masks with different colors
    colors = plt.cm.tab20(np.linspace(0, 1, max(len(masks), 1)))
    for i, (mask, class_id) in enumerate(zip(masks, class_ids)):
        color_mask = np.zeros((img_height, img_width, 3))
        color_rgba = colors[i % len(colors)][:3]  # Get RGB part of RGBA
        for c in range(3):
            color_mask[:,:,c] = mask * color_rgba[c]

        plt.imshow(color_mask, alpha=0.5)

        # Get class name and add label
        class_name = class_names[class_id] if class_id < len(class_names) else f"Class {class_id}"

        # Find mask center for label placement
        y_indices, x_indices = np.where(mask > 0)
        if len(y_indices) > 0 and len(x_indices) > 0:
            center_y = int(np.mean(y_indices))
            center_x = int(np.mean(x_indices))
            plt.text(center_x, center_y, class_name, color='white',
                     fontsize=12, ha='center', va='center',
                     bbox=dict(facecolor='black', alpha=0.7))

    plt.title(f"Image: {img_name}")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    return image, masks, class_ids

# Display first sample image
image, masks, class_ids = display_sample_with_masks(0)