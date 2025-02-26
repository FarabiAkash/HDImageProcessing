"""
pca_utils.py
Helper functions for performing PCA or related dimensionality reduction tasks
outside of the main ImageProcessor class. 
"""

import numpy as np
from sklearn.decomposition import PCA

def run_pca_on_array(array, n_components=3):
    """
    A generic utility to run PCA on a 2D array [samples, features].
    Returns the transformed array (samples, n_components).
    """
    pca = PCA(n_components=n_components)
    transformed = pca.fit_transform(array)
    return transformed, pca.explained_variance_ratio_

def flatten_5d_for_pca(data_5d, flatten_dims=(0,1,3,4)):
    """
    Flattens the specified dimensions of a 5D array to create a 2D array
    that can be fed to PCA. For example, flatten Z, T, H, W to get rows, 
    with channels as columns. 
    Returns a tuple of:
      - 2D array
      - shape information needed to reshape back
    """
    # data_5d has shape (Z, T, C, H, W). 
    # flatten_dims is a tuple of dimension indices to flatten into a single axis. 
    # By default, flatten Z, T, H, W => keep C separate.

    # We'll treat dimension 2 (C) as the "features" axis.
    # So we reorder data_5d to place C last, then flatten everything else first.
    
    Z, T, C, H, W = data_5d.shape
    # reorder to (Z, T, H, W, C)
    data_reordered = np.moveaxis(data_5d, 2, -1)  # now shape => (Z, T, H, W, C)

    # flatten (Z, T, H, W) => single dimension
    flattened = data_reordered.reshape(-1, C)  # shape => (Z*T*H*W, C)

    return flattened, (Z, T, H, W, C)
