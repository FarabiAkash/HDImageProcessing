"""
metadata.py
Handles GET /metadata for retrieving image metadata such as dimensions, bands, etc.
"""

from flask import request, jsonify
from . import api_bp, IMAGE_STORE, IMAGE_PROCESSOR_STORE
from src.core.image_processor import ImageProcessor

@api_bp.route('/metadata', methods=['GET'])
def get_metadata():
    """
    GET /metadata?image_id=<id>
    Retrieves metadata (dimensions, number of channels, etc.) for the specified image.
    """
    image_id = request.args.get('image_id', 'image_1')  # Default to 'image_1' if none provided
    if image_id not in IMAGE_STORE:
        return jsonify({"error": f"Image '{image_id}' not found"}), 404

    # Initialize ImageProcessor if not already created
    if image_id not in IMAGE_PROCESSOR_STORE:
        image_processor = ImageProcessor(IMAGE_STORE[image_id])
        IMAGE_PROCESSOR_STORE[image_id] = image_processor
    else:
        image_processor = IMAGE_PROCESSOR_STORE[image_id]

    metadata = image_processor.get_metadata()  # Placeholder method in ImageProcessor
    return jsonify(metadata), 200
