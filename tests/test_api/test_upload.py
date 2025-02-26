"""
test_upload.py
Tests for the POST /upload endpoint.
"""

import pytest
from io import BytesIO
from src.api.app import create_app


@pytest.fixture
def client():
    """
    Fixture to create a Flask test client.
    """
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


def test_upload_no_file(client):
    """
    If no file is part of the form data, it should return 400.
    """
    response = client.post('/upload', data={})
    assert response.status_code == 400
    assert response.json.get('error') == "No file part in the request"


def test_upload_empty_filename(client):
    """
    If the file is empty or has no filename, it should return 400.
    """
    data = {
        'file': (BytesIO(b''), '')  # No filename
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert response.json.get('error') == "No selected file"


def test_upload_success(client):
    """
    Valid file upload should return 200 with an 'image_id'.
    """
    # Create a dummy TIFF file in memory (just bytes - for example)
    tiff_bytes = b"II*\x00FakeTIFFData"  # Minimal placeholder, not a real 5D TIFF

    data = {
        'file': (BytesIO(tiff_bytes), 'test_image.tif')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert 'image_id' in response.json
    assert response.json['message'] == "File uploaded successfully"
