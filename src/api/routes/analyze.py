"""
analyze.py
Handles POST /analyze for running PCA or other analyses on the image data.
"""

from flask import request, jsonify
from . import api_bp, IMAGE_STORE, IMAGE_PROCESSOR_STORE
from src.core.image_processor import ImageProcessor

@api_bp.route('/analyze', methods=['POST'])
def analyze_image():
    """
    POST /analyze
    Request JSON body can include:
    {
        "image_id": "image_1",
        "components": 3
    }
    Runs PCA on the image data with the specified number of components.
    Returns the PCA-reduced data as JSON (2D or 3D array).
    """
    content = request.json or {}
    image_id = content.get('image_id', 'image_1')
    n_components = content.get('components', 3)

    if image_id not in IMAGE_STORE:
        return jsonify({"error": f"Image '{image_id}' not found"}), 404

    if image_id not in IMAGE_PROCESSOR_STORE:
        image_processor = ImageProcessor(IMAGE_STORE[image_id])
        IMAGE_PROCESSOR_STORE[image_id] = image_processor
    else:
        image_processor = IMAGE_PROCESSOR_STORE[image_id]

    # Placeholder method in ImageProcessor to run PCA
    pca_result = image_processor.run_pca(n_components)  # returns a NumPy array

    return jsonify({
        "image_id": image_id,
        "n_components": n_components,
        "pca_result": pca_result.tolist()  # Convert NumPy array to list for JSON serialization
    }), 200
