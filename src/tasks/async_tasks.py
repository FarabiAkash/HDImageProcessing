"""
async_tasks.py
Defines Celery tasks for long-running or large image operations (e.g., PCA, segmentation).
"""

import os
import numpy as np
from .celery_app import celery
from src.core.image_processor import ImageProcessor
from src.api.routes import IMAGE_STORE, IMAGE_PROCESSOR_STORE  # If you want to re-use in-memory data
# Or import a DB function if you store images in a database
# from src.db.database import SessionLocal
# from src.db.models import ImageMetadata

@celery.task(name='heavy_pca')
def heavy_pca(image_id, n_components=3):
    """
    A Celery task that runs PCA on an image in the background.
    :param image_id: The identifier of the image to process
    :param n_components: Number of PCA components
    :return: The shape of the PCA result or partial data
    """
    # In a real-world scenario, you'd load the image from DB or storage.
    # For demonstration, we'll pull from the in-memory store.
    if image_id not in IMAGE_STORE:
        return {"error": f"Image '{image_id}' not found"}

    # Use or recreate the ImageProcessor
    if image_id not in IMAGE_PROCESSOR_STORE:
        ip = ImageProcessor(IMAGE_STORE[image_id])
        IMAGE_PROCESSOR_STORE[image_id] = ip
    else:
        ip = IMAGE_PROCESSOR_STORE[image_id]

    pca_result = ip.run_pca(n_components)
    result_shape = pca_result.shape

    # Optionally, store or log the result somewhere persistent
    # e.g., store partial stats or the entire result in a DB
    # For brevity, we just return the shape
    return {
        "image_id": image_id,
        "n_components": n_components,
        "pca_shape": result_shape
    }

@celery.task(name='heavy_segmentation')
def heavy_segmentation(image_id, z=0, t=0, c=0, method='otsu', **kwargs):
    """
    Example segmentation task.
    :param image_id: The identifier of the image to process
    :param z, t, c: Indices to segment a single 2D slice or you could do 3D volumes
    :param method: 'otsu' or 'kmeans'
    :param kwargs: Additional parameters for the method
    :return: The counts of segmented labels (or some summary)
    """
    from src.core.segmentation import otsu_threshold, kmeans_segmentation

    if image_id not in IMAGE_STORE:
        return {"error": f"Image '{image_id}' not found"}

    # Use or recreate the ImageProcessor
    if image_id not in IMAGE_PROCESSOR_STORE:
        ip = ImageProcessor(IMAGE_STORE[image_id])
        IMAGE_PROCESSOR_STORE[image_id] = ip
    else:
        ip = IMAGE_PROCESSOR_STORE[image_id]

    slice_2d = ip.get_slice(z, t, c)

    if method == 'otsu':
        seg_mask = otsu_threshold(slice_2d)
        # Return the fraction of foreground pixels
        foreground_fraction = seg_mask.sum() / seg_mask.size
        return {
            "image_id": image_id,
            "method": "otsu",
            "foreground_fraction": foreground_fraction
        }
    elif method == 'kmeans':
        n_clusters = kwargs.get('n_clusters', 2)
        labels_2d = kmeans_segmentation(slice_2d, n_clusters)
        # Count label frequency
        unique, counts = np.unique(labels_2d, return_counts=True)
        label_counts = dict(zip(unique.tolist(), counts.tolist()))
        return {
            "image_id": image_id,
            "method": "kmeans",
            "n_clusters": n_clusters,
            "label_counts": label_counts
        }
    else:
        return {"error": f"Unknown segmentation method '{method}'"}
