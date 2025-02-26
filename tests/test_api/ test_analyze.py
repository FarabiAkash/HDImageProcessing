"""
test_analyze.py
Tests for the POST /analyze endpoint (PCA).
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


def test_analyze_no_image(client):
    """
    POST /analyze with a missing image_id should 404 if not found.
    """
    payload = {"image_id": "non_existent", "components": 2}
    resp = client.post('/analyze', json=payload)
    assert resp.status_code == 404
    assert "not found" in resp.json['error']


def test_analyze_pca(client, uploaded_image):
    """
    POST /analyze with a valid image_id and components.
    Expects a JSON response containing pca_result as a list.
    """
    payload = {"image_id": uploaded_image, "components": 2}
    resp = client.post('/analyze', json=payload)
    assert resp.status_code == 200
    assert resp.json['image_id'] == uploaded_image
    assert resp.json['n_components'] == 2
    # pca_result should be a nested list
    assert isinstance(resp.json['pca_result'], list)
