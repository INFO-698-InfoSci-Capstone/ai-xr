from roboflow import Roboflow
import os
import glob
import yaml
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image

def download_roboflow_dataset():
    """Download a dataset from Roboflow in YOLOv11 format"""
    rf = Roboflow(api_key="SN5wJh6Iq1qReYz1KzDq")
    project = rf.workspace("interiorfurniture").project("chair-eecyt")

    # Modified line to download YOLOv11 format instead of COCO
    dataset = project.version(1).download("yolov11")  # Roboflow typically uses "yolov5" label format for YOLOv5/v7/v8/v11

    print(f"Dataset downloaded to: {dataset.location}")
    return dataset.location