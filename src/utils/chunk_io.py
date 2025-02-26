"""
chunk_io.py
Utilities for chunked reading/writing of large images 
to reduce memory usage.
"""

import os

def read_in_chunks(file_obj, chunk_size=1024*1024):
    """
    Generator that reads a file in chunks of specified size.
    Useful for large file uploads or downloads.
    """
    while True:
        data = file_obj.read(chunk_size)
        if not data:
            break
        yield data

def write_in_chunks(filename, file_bytes, chunk_size=1024*1024):
    """
    Writes bytes to a file in chunks.
    """
    with open(filename, 'wb') as f:
        size = len(file_bytes)
        offset = 0
        while offset < size:
            end = min(offset + chunk_size, size)
            f.write(file_bytes[offset:end])
            offset += chunk_size
    return os.path.getsize(filename)
