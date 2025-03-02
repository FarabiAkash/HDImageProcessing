# Architecture Overview

This is a microservice designed to handle 5D scientific images (dimensions typically represent: Time, Z-stack, Channels, Height, Width). The system is built with:

1. Flask API (Frontend)
2. Core Processing Engine
3. PostgreSQL Database (via Vercel)
4. Optional Celery/Redis for async tasks

# API Flow and Usage

## 1. First Step: Upload an Image

The first API you must call is the upload endpoint:

```bash
POST /upload
Content-Type: multipart/form-data
Body: file=@your_5d_image.tif
```

This endpoint will:

- Validate the TIFF file
- Store it in the system
- Return an `image_id` that you'll use for all subsequent operations

Expected response:

```json
{
  "message": "File uploaded successfully",
  "image_id": "image_1"
}
```

## 2. Check Image Metadata

After upload, you can verify the image dimensions:

```bash
GET /metadata?image_id=image_1
```

You'll receive:

```json
{
  "dtype": "uint16",
  "shape": [10, 5, 3, 512, 512], // [Time, Z, Channels, Height, Width]
  "Z": 10,
  "T": 5,
  "Channels": 3,
  "Height": 512,
  "Width": 512
}
```

## 3. Working with the Image

### a. Get 2D Slices

To visualize specific planes:

```bash
GET /slice?image_id=image_1&z=0&time=0&channel=0
```

Returns: A PNG image of the specified slice

### b. Run Analysis

For dimensional reduction or feature extraction:

```bash
POST /analyze
Content-Type: application/json
{
    "image_id": "image_1",
    "components": 2
}
```

Returns PCA results:

```json
{
    "image_id": "image_1",
    "n_components": 2,
    "pca_result": [[...]]
}
```

### c. Get Statistics

For basic image statistics:

```bash
GET /statistics?image_id=image_1
```

Returns:

```json
{
  "mean": [45.3, 61.8, 120.2], // per channel
  "std": [14.2, 18.7, 35.1],
  "min": [0, 0, 0],
  "max": [255, 255, 255]
}
```

# Key Components

## 1. Core Processing Engine

- Located in `src/core/image_processor.py`
- Handles TIFF loading, slicing, and analysis
- Uses libraries like tifffile, numpy, scikit-image

## 2. Database Integration

- Uses SQLAlchemy with Vercel PostgreSQL
- Stores metadata and processing results
- Image data can be stored in filesystem or cloud storage

## 3. Asynchronous Processing (Optional)

For heavy operations:

```python
# In your code
from src.tasks.async_tasks import heavy_pca
result = heavy_pca.delay(image_id="image_1", n_components=3)
```

# Setup Requirements

1. Environment Variables:

```bash
export VERCEL_POSTGRES_URL=postgresql://:@:/
export CELERY_BROKER_URL=redis://localhost:6379/0  # if using Celery
export CELERY_RESULT_BACKEND=redis://localhost:6379/0  # if using Celery
```

2. Dependencies:

```bash
pip install -r requirements.txt
```

3. Database Setup:

```bash
python -c "from src.db.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

# Best Practices

1. **Error Handling**: All endpoints include proper error handling for:

   - Invalid image formats
   - Missing files
   - Out-of-range parameters
   - Database connection issues

2. **Memory Management**: For large images:

   - Use chunked I/O operations
   - Consider using async processing
   - Implement proper cleanup

3. **Testing**:
   ```bash
   pytest  # Run all tests
   pytest --cov=src --cov-report=term-missing  # With coverage
   ```

# Common Use Cases

1. **Scientific Image Analysis**:

   ```python
   # Upload image
   image_id = upload_image("microscopy_data.tif")

   # Get middle slice
   middle_slice = get_slice(image_id, z=5, t=0, channel=0)

   # Run PCA
   pca_results = analyze_image(image_id, components=3)
   ```

2. **Batch Processing**:
   ```python
   # Using async tasks
   for image in image_list:
       heavy_pca.delay(image_id=image, n_components=3)
   ```

This microservice is designed to be scalable and can be deployed either as a standalone service or as part of a larger system. The modular architecture allows for easy extensions and modifications based on specific needs.
