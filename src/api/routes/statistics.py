"""
statistics.py
Handles GET /statistics to retrieve basic image statistics (mean, std, min, max) for each band/channel.
"""

from flask import request, jsonify
from . import api_bp, IMAGE_STORE, IMAGE_PROCESSOR_STORE
from src.core.image_processor import ImageProcessor

@api_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """
    GET /statistics?image_id=<id>
    Returns basic image statistics, e.g., mean, std, min, max for each band or channel.
    """
    image_id = request.args.get('image_id', 'image_1')

    if image_id not in IMAGE_STORE:
        return jsonify({"error": f"Image '{image_id}' not found"}), 404

    if image_id not in IMAGE_PROCESSOR_STORE:
        image_processor = ImageProcessor(IMAGE_STORE[image_id])
        IMAGE_PROCESSOR_STORE[image_id] = image_processor
    else:
        image_processor = IMAGE_PROCESSOR_STORE[image_id]

    # Placeholder method for statistics
    stats = image_processor.get_statistics()

    return jsonify(stats), 200
