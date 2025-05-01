import os
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flasgger import Swagger
import cv2
import numpy as np
from PIL import Image
import io
import time
from utils import process_image

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Configure CORS
CORS(app)

# Configure rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["60 per minute"]
)

# Configure Swagger
swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "Image Segmentation API",
        "description": "API for processing images with instance segmentation",
        "version": "1.0.0"
    }
})

# Configure upload folder
UPLOAD_FOLDER = os.path.join('static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set maximum upload size to 10MB
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/segment', methods=['POST'])
@limiter.limit("60 per minute")
def segment_image():
    """
    Process an image with instance segmentation
    ---
    tags:
      - segmentation
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The image file to process
    responses:
      200:
        description: Successful processing
        schema:
          type: object
          properties:
            width:
              type: integer
              description: Image width
            height:
              type: integer
              description: Image height
            masks:
              type: array
              items:
                type: object
                properties:
                  class:
                    type: string
                    description: Class name of the detected object
                  confidence:
                    type: number
                    description: Confidence score of the detection
                  points:
                    type: array
                    items:
                      type: array
                      items:
                        type: integer
                    description: Polygon coordinates of the mask
                  rgb_color:
                    type: array
                    items:
                      type: integer
                    description: RGB color for visualization
      400:
        description: Invalid input
      413:
        description: File too large
      500:
        description: Server error
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Allowed file types are png, jpg, jpeg'}), 400
    
    try:
        # Create a unique filename
        unique_filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Process the image
        start_time = time.time()
        result = process_image(filepath, save_debug_images=True)
        processing_time = time.time() - start_time
        
        # Add processing time to response
        result['processing_time'] = f"{processing_time:.2f}"
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)