import numpy as np
from skimage import io
from ..utils.chunk_io import chunked_read

class ImageProcessor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.image = None
        
    def load_image(self):
        """Load multi-dimensional TIFF image"""
        self.image = chunked_read(self.filepath)
        
    def get_slice(self, dimensions):
        """Extract a specific slice from the image"""
        if self.image is None:
            self.load_image()
        return np.take(self.image, dimensions, axis=tuple(range(len(dimensions))))
    
    def calculate_statistics(self):
        """Calculate basic statistics for the image"""
        if self.image is None:
            self.load_image()
        return {
            'mean': float(np.mean(self.image)),
            'std': float(np.std(self.image)),
            'min': float(np.min(self.image)),
            'max': float(np.max(self.image))
        }
