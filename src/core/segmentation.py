"""
segmentation.py
Implements segmentation algorithms like Otsu thresholding or k-means.
We can apply them to a specific slice or across entire channels.
"""

import numpy as np
from skimage.filters import threshold_otsu
from sklearn.cluster import KMeans

def otsu_threshold(image_2d):
    """
    Applies Otsu's thresholding to a 2D image (NumPy array).
    Returns a binary mask (0 or 1) of the same shape.
    """
    thresh_val = threshold_otsu(image_2d)
    binary_mask = (image_2d >= thresh_val).astype(np.uint8)
    return binary_mask

def kmeans_segmentation(image_2d, n_clusters=2):
    """
    Applies k-means to a 2D image by flattening it into a (H*W, 1) array,
    clustering into n_clusters, and returning a label image reshaped to (H, W).
    """
    H, W = image_2d.shape
    flattened = image_2d.reshape(-1, 1).astype(np.float32)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(flattened)
    labels = kmeans.labels_

    segmented = labels.reshape(H, W)
    return segmented

def segment_3d(image_3d, method='otsu', **kwargs):
    """
    Convenience function to apply segmentation slice-by-slice for a 3D volume 
    (e.g. Z, H, W) or (T, H, W).

    'method' can be 'otsu' or 'kmeans'. You can extend for more methods.

    Returns a segmented 3D array of the same shape.
    """
    D, H, W = image_3d.shape
    output = np.zeros((D, H, W), dtype=np.uint8)

    for i in range(D):
        slice_2d = image_3d[i, :, :]
        if method == 'otsu':
            mask = otsu_threshold(slice_2d)
        elif method == 'kmeans':
            n_clusters = kwargs.get('n_clusters', 2)
            mask = kmeans_segmentation(slice_2d, n_clusters=n_clusters)
        else:
            raise ValueError(f"Unknown segmentation method: {method}")
        output[i] = mask

    return output
