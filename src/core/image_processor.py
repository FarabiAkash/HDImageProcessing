"""
image_processor.py
Core class for loading, storing, and performing operations on 5D image data.
"""

import numpy as np
import io
from tifffile import TiffFile
from sklearn.decomposition import PCA

class ImageProcessor:
    """
    ImageProcessor is responsible for:
    1. Loading a 5D TIFF from bytes or file.
    2. Providing metadata (shape, dtype, etc.).
    3. Extracting slices at (Z, T, Channel).
    4. Running PCA for dimensionality reduction.
    5. Computing basic statistics (mean, std, min, max).
    """

    def __init__(self, image_bytes):
        """
        Constructor that receives the raw TIFF data (bytes).
        Internally, loads the image as a 5D NumPy array: (Z, T, C, H, W).
        """
        self.image_data = self._load_tiff_from_bytes(image_bytes)  # shape = (Z, T, C, H, W)
        self.metadata = self._extract_metadata()

    def _load_tiff_from_bytes(self, image_bytes):
        """
        Loads multi-dimensional TIFF data from an in-memory bytes object
        using the tifffile library.

        Returns:
            A NumPy array shaped like (Z, T, C, H, W).
            Adjust the ordering logic according to your data.
        """
        with io.BytesIO(image_bytes) as buf:
            with TiffFile(buf) as tif:
                # Many scientific 5D TIFFs store data in a single "page series"
                series = tif.series[0]
                data = series.asarray()  # This might return a multi-dimensional array
                # The shape might come in various forms, e.g. (T, Z, C, H, W), or (Z, T, C, H, W)
                # We need to confirm the shape from 'data.shape' and reorder if needed.

                # Example: if the shape is (T, Z, C, H, W), reorder to (Z, T, C, H, W):
                # This reordering depends on your data specifics. 
                # We will assume the data is (Z, T, C, H, W) directly for simplicity.
                
                if data.ndim < 5:
                    # If the file is not actually 5D, you may need to expand dims
                    # e.g. (H, W) => (1,1,1,H,W), (Z, H, W) => (Z,1,1,H,W), etc.
                    data = np.expand_dims(data, axis=0)  # minimal approach
                    # Expand more as needed to ensure 5D shape

                # Ensure data is float or uint (depending on your use-case)
                # data = data.astype(np.float32)  # or keep original dtype

                return data

    def _extract_metadata(self):
        """
        Extracts basic metadata from self.image_data, e.g. shape, dtype.
        Returns a dict.
        """
        shape = self.image_data.shape  # (Z, T, C, H, W)
        metadata = {
            "dtype": str(self.image_data.dtype),
            "shape": shape,
            "Z": shape[0],
            "T": shape[1] if len(shape) > 1 else 1,
            "Channels": shape[2] if len(shape) > 2 else 1,
            "Height": shape[3] if len(shape) > 3 else 1,
            "Width": shape[4] if len(shape) > 4 else 1
        }
        return metadata

    def get_metadata(self):
        """Returns the metadata dictionary created on init."""
        return self.metadata

    def get_slice(self, z, t, c):
        """
        Extracts a 2D slice at the specified Z, Time, and Channel.
        Returns a NumPy 2D array (Height x Width).
        """
        # Validate indices
        Z, T, C, H, W = self.image_data.shape
        if not (0 <= z < Z and 0 <= t < T and 0 <= c < C):
            raise ValueError(f"Invalid slice indices z={z}, t={t}, c={c}")

        slice_2d = self.image_data[z, t, c, :, :]  # shape = (H, W)
        return slice_2d

    def run_pca(self, n_components=3):
        """
        Runs PCA on the entire image data to reduce the channel dimension 
        or flatten some of the dimensions, depending on the use-case.

        Strategy:
        1) Flatten the (Z, T) dimensions + (H, W) dimensions and only keep the channel dimension, or 
        2) Flatten everything except channels, depending on how you want to apply PCA.

        For demonstration, we flatten everything except the channel dimension 
        and then do PCA across channels. This is somewhat naive but shows the concept.
        """
        Z, T, C, H, W = self.image_data.shape
        # Reshape to (Z*T*H*W, C)
        reshaped = self.image_data.reshape(-1, C).astype(np.float32)

        # Fit PCA on the flattened data
        pca = PCA(n_components=n_components)
        pca_result = pca.fit_transform(reshaped)  # shape => (Z*T*H*W, n_components)

        # Reshape back to (Z, T, H, W, 
