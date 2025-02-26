"""
test_statistics.py
Tests for the GET /statistics endpoint.
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


def test_statistics_no_image(client):
    """
    GET /statistics with invalid image_id should return 404.
    """
    resp = client.get('/statistics?image_id=non_existent')
    assert resp.status_code == 404
    assert "not found" in resp.json['error']


def test_statistics_success(client, uploaded_image):
    """
    GET /statistics with a valid image_id should return mean, std, min, max arrays.
    """
    resp = client.get(f'/statistics?image_id={uploaded_image}')
    assert resp.status_code == 200
    assert 'mean' in resp.json
    assert 'std' in resp.json
    assert 'min' in resp.json
    assert 'max' in resp.json
    # Usually these are lists of floats per channel, so let's check that they're lists
    assert isinstance(resp.json['mean'], list)
    assert isinstance(resp.json['std'], list)
