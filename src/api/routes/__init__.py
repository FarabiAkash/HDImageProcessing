"""
__init__.py under routes
Sets up the Blueprint for all API routes and holds in-memory stores for simplicity.
"""

from flask import Blueprint

# Create a single Blueprint for all our routes
api_bp = Blueprint('api', __name__)

# In-memory store for uploaded images (raw bytes). 
# In production, store images on disk or in an object store (S3, etc.).
IMAGE_STORE = {}

# In-memory store for image processor instances keyed by image_id.
# Typically, you'd reconstruct an ImageProcessor from disk or DB each time instead.
IMAGE_PROCESSOR_STORE = {}

# Import the individual route modules to register their endpoints on the blueprint
from src.api.routes.upload import *
from src.api.routes.metadata import *
from src.api.routes.slice import *
from src.api.routes.analyze import *
from src.api.routes.statistics import *
