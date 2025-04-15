import os
import sys
import glob
from texture_generation import roboflow_loader, segmentation, stablediffusion_loader

def main() -> int:
    """
    Main entry point of the application.
    
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        dataset_path = roboflow_loader.download_roboflow_dataset()
        # Define output path
        output_path = "./texture_output"
        os.makedirs(output_path, exist_ok=True)

        # Explore the dataset structure
        print("\nExploring YOLO dataset structure:")
        print("Root directory contents:")
        for item in glob.glob(f"{dataset_path}/*"):
            print(f"- {os.path.basename(item)}")

        # YOLO datasets use .txt annotations instead of .json
        print("\nLooking for YOLO annotation files:")
        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                if file.endswith(".txt"):
                    print(f"Found YOLO annotation file: {os.path.join(root, file)}")

        # Check dataset.yaml file
        print("\nLooking for dataset YAML file:")
        if os.path.exists(os.path.join(dataset_path, "data.yaml")):
            print("Found data.yaml - this is crucial for YOLO training")

        segmentation.load_classlabels(dataset_path)

        stablediffusion_loader.texture_load()
       
        return 0
    except Exception as e:
        return 1

if __name__ == "__main__":
    sys.exit(main())