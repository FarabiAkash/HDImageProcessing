"""
file_validation.py
Utility functions for validating file inputs (extensions, size limits, etc.).
"""

import os

def validate_tiff_file(filename, file_bytes):
    """
    Checks that the file extension is .tif or .tiff and that file_bytes isn't empty.
    Raises ValueError if invalid.
    """
    valid_extensions = ('.tif', '.tiff')
    ext = os.path.splitext(filename)[1].lower()

    if ext not in valid_extensions:
        raise ValueError(f"Invalid file extension '{ext}'. Must be .tif or .tiff.")
    
    if not file_bytes:
        raise ValueError("File is empty.")

    # Optionally, check magic numbers or other deeper checks
    # E.g., checking the first few bytes for the TIFF header (49 49 2A 00 or 4D 4D 00 2A in hex)

    return True
