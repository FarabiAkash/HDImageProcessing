"""
test_image_processor.py
Tests the ImageProcessor class in src/core/image_processor.py
"""

import pytest
import numpy as np
from src.core.image_processor import ImageProcessor


@pytest.fixture
def fake_5d_data():
    """
    Creates a small 5D NumPy array shaped (Z, T, C, H, W).
    For instance: (2, 1, 2, 4, 4) for quick testing.
    """
    # Shape: (2, 1, 2, 4, 4)
    data = np.random.randint(0, 255, size=(2, 1, 2, 4, 4), dtype=np.uint8)
    return data


@pytest.fixture
def fake_tiff_bytes(fake_5d_data):
    """
    Mocks the in-memory bytes of a TIFF file by saving the fake_5d_data 
    with tifffile to an in-memory buffer.
    """
    import io
    from tifffile import imwrite

    buf = io.BytesIO()
    imwrite(buf, fake_5d_data, imagej=True)  # imagej=True handles some multi-dim metadata
    buf.seek(0)
    return buf.read()


def test_init_loads_data(fake_tiff_bytes):
    """
    Tests if ImageProcessor loads TIFF bytes without error 
    and sets image_data appropriately.
    """
    processor = ImageProcessor(fake_tiff_bytes)
    assert processor.image_data is not None
    assert processor.image_data.ndim == 5  # Expect 5D shape


def test_get_metadata(fake_tiff_bytes):
    """
    Verifies that get_metadata returns expected keys 
    and shape matches the loaded data.
    """
    processor = ImageProcessor(fake_tiff_bytes)
    metadata = processor.get_metadata()

    assert "dtype" in metadata
    assert "shape" in metadata
    assert "Z" in metadata
    assert "T" in metadata
    assert "Channels" in metadata
    assert "Height" in metadata
    assert "Width" in metadata
    # Check shape consistency
    shape = metadata["shape"]
    assert len(shape) == 5


def test_get_slice(fake_tiff_bytes):
    """
    Checks if get_slice returns a 2D array (H, W).
    """
    processor = ImageProcessor(fake_tiff_bytes)
    slice_2d = processor.get_slice(z=0, t=0, c=0)
    assert slice_2d.ndim == 2  # Expect 2D
    # shape should be (Height, Width)
    Z, T, C, H, W = processor.image_data.shape
    assert slice_2d.shape == (H, W)


def test_get_slice_invalid_indices(fake_tiff_bytes):
    """
    Expects ValueError when requesting a slice out of range.
    """
    processor = ImageProcessor(fake_tiff_bytes)
    Z, T, C, H, W = processor.image_data.shape

    with pytest.raises(ValueError):
        # Use an out-of-bounds index
        processor.get_slice(z=Z+1, t=0, c=0)


def test_run_pca(fake_tiff_bytes):
    """
    Ensures run_pca returns a 5D array with last dimension = n_components (if flattening channels).
    """
    processor = ImageProcessor(fake_tiff_bytes)
    n_components = 2
    pca_result = processor.run_pca(n_components=n_components)
    assert pca_result.ndim == 5
    # Should be (Z, T, H, W, n_components)
    assert pca_result.shape[-1] == n_components


def test_get_statistics(fake_tiff_bytes):
    """
    Checks if get_statistics returns mean, std, min, max lists with length = # of channels.
    """
    processor = ImageProcessor(fake_tiff_bytes)
    stats = processor.get_statistics()

    assert "mean" in stats
    assert "std" in stats
    assert "min" in stats
    assert "max" in stats

    # Should have as many entries as the number of channels
    num_channels = processor.image_data.shape[2]
    for key in ["mean", "std", "min", "max"]:
        assert len(stats[key]) == num_channels
