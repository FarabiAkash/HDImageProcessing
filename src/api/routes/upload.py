"""
upload.py
Handles file upload (POST /upload) and stores raw image bytes in IMAGE_STORE.
"""

from flask import request, jsonify
from . import api_bp, IMAGE_STORE

@api_bp.route('/upload', methods=['POST'])
def upload_image():
    """
    POST /upload
    Accepts a multi-dimensional TIFF file and stores it in memory.
    
    Form-Data: file => multi-dimensional TIFF
    Returns a JSON response with an 'image_id'.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Generate a simple ID or use a UUID in practice
    image_id = f"image_{len(IMAGE_STORE) + 1}"  # Generate unique ID based on store size

    # Read file bytes directly
    file_bytes = file.read()
    
    # Store the raw data in our in-memory store
    IMAGE_STORE[image_id] = file_bytes

    return jsonify({"message": "File uploaded successfully", "image_id": image_id}), 200
