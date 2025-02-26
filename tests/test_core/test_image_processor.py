import pytest
import numpy as np
from src.core.image_processor import ImageProcessor

def test_image_loading():
    processor = ImageProcessor('data/sample_5d_image.tif')
    processor.load_image()
    assert processor.image is not None
    
def test_slice_extraction():
    processor = ImageProcessor('data/sample_5d_image.tif')
    slice_dims = [0, 0, 0]
    result = processor.get_slice(slice_dims)
    assert isinstance(result, np.ndarray)
    
def test_statistics_calculation():
    processor = ImageProcessor('data/sample_5d_image.tif')
    stats = processor.calculate_statistics()
    assert all(key in stats for key in ['mean', 'std', 'min', 'max'])
