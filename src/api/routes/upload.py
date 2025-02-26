from flask import Blueprint, request, jsonify
from ...utils.file_validation import validate_file
from ...tasks.async_tasks import process_upload

bp = Blueprint('upload', __name__)

@bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
        
    file = request.files['file']
    if not validate_file(file):
        return jsonify({'error': 'Invalid file format'}), 400
        
    task = process_upload.delay(file)
    return jsonify({'task_id': str(task.id)}), 202
