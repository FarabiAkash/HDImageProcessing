"""
slice.py
Handles GET /slice for extracting a specific Z, Time, and Channel slice from a 5D image.
"""

from flask import request, jsonify, send_file
from io import BytesIO
from PIL import Image
from . import api_bp, IMAGE_STORE, IMAGE_PROCESSOR_STORE
from src.core.image_processor import ImageProcessor

@api_bp.route('/slice', methods=['GET'])
def get_slice():
    """
    GET /slice?image_id=<id>&z=<z>&time=<t>&channel=<c>
    Returns a 2D slice extracted from the 5D image.
    For 4D images, the z parameter is ignored.
    """
    image_id = request.args.get('image_id', 'image_1')
    z = int(request.args.get('z', 0))
    t = int(request.args.get('time', 0))
    c = int(request.args.get('channel', 0))

    if image_id not in IMAGE_STORE:
        return jsonify({"error": f"Image '{image_id}' not found"}), 404

    try:
        if image_id not in IMAGE_PROCESSOR_STORE:
            image_processor = ImageProcessor(IMAGE_STORE[image_id])
            IMAGE_PROCESSOR_STORE[image_id] = image_processor
        else:
            image_processor = IMAGE_PROCESSOR_STORE[image_id]

        # Get slice data, z parameter will be ignored for 4D images
        slice_data = image_processor.get_slice(z, t, c)

        # Convert the slice (NumPy array) to a PNG in memory
        pil_image = Image.fromarray(slice_data.astype('uint8'))
        img_io = BytesIO()
        pil_image.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        return jsonify({"error": str(e)}), 400
