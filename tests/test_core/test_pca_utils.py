"""
test_pca_utils.py
Tests the helper functions in src/utils/pca_utils.py
"""

import pytest
import numpy as np
from src.utils.pca_utils import run_pca_on_array, flatten_5d_for_pca


def test_run_pca_on_array():
    """
    Creates a small 2D dataset (samples x features) and tests PCA run.
    """
    # 10 samples, 5 features
    data = np.random.rand(10, 5).astype(np.float32)
    transformed, var_ratio = run_pca_on_array(data, n_components=2)

    # transformed should be shape (10, 2)
    assert transformed.shape == (10, 2)
    # var_ratio should be length 2
    assert len(var_ratio) == 2


def test_flatten_5d_for_pca():
    """
    Creates a fake 5D array and flattens it to check shape correctness.
    """
    # shape (Z, T, C, H, W) => (2, 1, 3, 4, 4)
    data_5d = np.random.rand(2, 1, 3, 4, 4).astype(np.float32)
    flattened, orig_shape = flatten_5d_for_pca(data_5d)

    # Expect flattened shape = (Z*T*H*W, C) => (2*1*4*4, 3) = (32, 3)
    assert flattened.shape == (32, 3)
    # orig_shape should be (2, 1, 4, 4, 3)
    # but let's see exactly what the function returns
    Z, T, H, W, C = orig_shape
    assert (Z, T, H, W, C) == (2, 1, 4, 4, 3)
