"""
test_slice.py
Tests for the GET /slice endpoint, which returns a PNG image slice.
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
    tiff_bytes = b"II*\x00FakeTIFFData"
    data = {
        'file': (BytesIO(tiff_bytes), 'test_image.tif')
    }
    resp = client.post('/upload', data=data, content_type='multipart/form-data')
    return resp.json.get('image_id')


def test_slice_no_image(client):
    """
    GET /slice with invalid image_id should return 404.
    """
    resp = client.get('/slice?image_id=non_existent')
    assert resp.status_code == 404
    assert "not found" in resp.json['error']


def test_slice_defaults(client, uploaded_image):
    """
    GET /slice without specifying z, time, channel uses defaults (0,0,0).
    Should return a PNG.
    """
    resp = client.get(f'/slice?image_id={uploaded_image}')
    # Even though the data is fake, we expect a 200 or an image
    assert resp.status_code == 200
    # The response content type should be image/png
    assert resp.content_type == 'image/png'
