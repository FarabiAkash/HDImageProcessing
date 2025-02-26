"""
test_metadata.py
Tests for the GET /metadata endpoint.
"""

import pytest
from io import BytesIO
from src.api.app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def uploaded_image(client):
    """
    Helper fixture that uploads a sample TIFF file 
    and returns the image_id from the response.
    """
    tiff_bytes = b"II*\x00FakeTIFFData"
    data = {
        'file': (BytesIO(tiff_bytes), 'test_image.tif')
    }
    resp = client.post('/upload', data=data, content_type='multipart/form-data')
    return resp.json.get('image_id')


def test_metadata_no_image_id(client):
    """
    GET /metadata with no image_id (defaults to 'image_1' in code).
    If 'image_1' is not uploaded, we get 404.
    """
    resp = client.get('/metadata')
    assert resp.status_code == 404
    assert "not found" in resp.json['error']


def test_metadata_success(client, uploaded_image):
    """
    GET /metadata with a valid image_id should return metadata dict.
    """
    resp = client.get(f'/metadata?image_id={uploaded_image}')
    assert resp.status_code == 200
    assert 'shape' in resp.json
    assert 'dtype' in resp.json
    assert 'Z' in resp.json
