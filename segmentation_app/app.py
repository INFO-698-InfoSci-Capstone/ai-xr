import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import cv2
import numpy as np
from PIL import Image
import io
import time
from utils import process_image

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Required for flash messages

# Configure upload folder
UPLOAD_FOLDER = os.path.join('static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set maximum upload size to 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    # If user does not select file, browser also
    # submits an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # Create a unique filename
        unique_filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        try:
            # Process the image with our segmentation model - note we now get masks_data too
            start_time = time.time()
            result_filepath, masks_data = process_image(filepath)
            processing_time = time.time() - start_time
            
            # Get relative paths for the template (from static folder)
            # Extract just the 'uploads/filename.jpg' part
            original_image = 'uploads/' + os.path.basename(filepath)
            result_image = 'uploads/' + os.path.basename(result_filepath)
            
            print(f"Original image URL: {original_image}")
            print(f"Result image URL: {result_image}")
            print(f"Masks found for classes: {list(masks_data.keys())}")
            
            # Return the result page with the processed image and masks data
            return render_template('result.html', 
                                  original_image=original_image,
                                  result_image=result_image,
                                  masks_data=masks_data,
                                  processing_time=f"{processing_time:.2f}")
            
        except Exception as e:
            print(f"Error in upload_file: {str(e)}")
            flash(f"Error processing image: {str(e)}")
            return redirect(url_for('index'))
    else:
        flash('Allowed file types are png, jpg, jpeg')
        return redirect(url_for('index'))

@app.route('/api/process', methods=['POST'])
def api_process():
    """API endpoint for processing images"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Create a unique filename
        unique_filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        try:
            # Process the image
            start_time = time.time()
            result_filepath, masks_data = process_image(filepath)
            processing_time = time.time() - start_time
            
            # For API response
            original_image = 'uploads/' + os.path.basename(filepath)
            result_image = 'uploads/' + os.path.basename(result_filepath)
            
            # Return JSON response with results
            return jsonify({
                'status': 'success',
                'original_image': original_image,
                'result_image': result_image,
                'masks': {k: v['filename'] for k, v in masks_data.items()},
                'processing_time': f"{processing_time:.2f}"
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Allowed file types are png, jpg, jpeg'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)