# High-Dimensional Image Processing Microservice

This repository contains a Python-based microservice for uploading, processing, and analyzing high-dimensional (5D) scientific images. It includes:

- **Image Processing Core** (Loading 5D TIFF, slicing, PCA, basic stats).
- **Flask API** (Upload, metadata, slicing, analysis, and stats endpoints).
- **Database Integration** (Vercel PostgreSQL via SQLAlchemy).
- **Optional Asynchronous Tasks** (Celery/Redis).
- **Unit Tests** (Pytest coverage for API, core, and DB).

## Table of Contents

- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation & Setup](#installation--setup)
  - [Environment Variables](#environment-variables)
  - [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
  - [Local Development](#local-development)
  - [Docker Container (Optional)](#docker-container-optional)
- [Using the API](#using-the-api)
  - [Endpoint Reference](#endpoint-reference)
  - [Example Requests](#example-requests)
- [Testing](#testing)
- [Asynchronous Tasks (Optional)](#asynchronous-tasks-optional)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Project Structure

```text
project_root/
├── README.md
├── requirements.txt
├── data/
│   └── sample_5d_image.tif  # Example data (optional)
├── notebooks/
│   └── demonstration.ipynb  # Jupyter Notebook demo
├── src/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── upload.py
│   │   │   ├── metadata.py
│   │   │   ├── slice.py
│   │   │   ├── analyze.py
│   │   │   └── statistics.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── image_processor.py
│   │   └── segmentation.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── models.py
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── celery_app.py
│   │   └── async_tasks.py
│   └── utils/
│       ├── __init__.py
│       ├── file_validation.py
│       ├── chunk_io.py
│       └── pca_utils.py
└── tests/
    ├── __init__.py
    ├── test_api/
    │   ├── test_upload.py
    │   ├── test_metadata.py
    │   ├── test_slice.py
    │   ├── test_analyze.py
    │   └── test_statistics.py
    ├── test_core/
    │   ├── test_image_processor.py
    │   ├── test_segmentation.py
    │   └── test_pca_utils.py
    └── test_db/
        └── test_database.py

```

## Requirements

- **Python 3.8+**
- The following Python libraries (see requirements.txt):

  - Flask
  - tifffile
  - numpy
  - Pillow
  - scikit-image
  - scikit-learn
  - SQLAlchemy
  - psycopg2-binary
  - celery
  - redis
  - pytest

- **PostgreSQL** (Vercel Postgres recommended).
- **Redis** (optional, if running Celery for asynchronous tasks).

## Installation & Setup

1.  bashCopyEditgit clone https://github.com/YourUser/highdim-image-processor.gitcd highdim-image-processor
2.  bashCopyEditpython -m venv venvsource venv/bin/activate # On macOS/Linux# orvenv\\Scripts\\activate.bat # On Windows
3.  bashCopyEditpip install -r requirements.txt

### Environment Variables

Set the following environment variables as needed:

- bashCopyEditexport VERCEL_POSTGRES_URL=postgresql://:@:/
- bashCopyEditexport CELERY_BROKER_URL=redis://localhost:6379/0
- bashCopyEditexport CELERY_RESULT_BACKEND=redis://localhost:6379/0

### Database Setup

1.  bashCopyEditpython -c "from src.db.database import Base, engine; Base.metadata.create_all(bind=engine)"This will create any tables defined in src/db/models.py.
2.  **(Optional)** Use migrations via Alembic if you want to manage schema changes over time.

## Running the Application

### Local Development

1.  bashCopyEditcd src/apipython app.pyBy default, this will run on http://127.0.0.1:5000.
2.  **Verify** that you can connect to the DB:

    - Check logs for any errors about database connections.
    - Ensure VERCEL_POSTGRES_URL is correct.

### Docker Container (Optional)

If you prefer a container-based deployment:

1.  dockerfileCopyEditFROM python:3.9-slimWORKDIR /appCOPY . /appRUN pip install --no-cache-dir -r requirements.txtENV VERCEL_POSTGRES_URL=EXPOSE 5000CMD \["python", "src/api/app.py"\]
2.  bashCopyEditdocker build -t highdim-processor .docker run -p 5000:5000 highdim-processor
3.  **Access** via http://localhost:5000.

## Using the API

### Endpoint Reference

1.  **POST /upload**

    - Uploads a multi-dimensional TIFF file.
    - **Form Data**: file => TIF/TIFF file.
    - **Response**: {"message": "...", "image_id": "..."}

2.  **GET /metadata**

    - Retrieves metadata for the uploaded image.
    - **Query Params**: image_id=...
    - **Response**: {"dtype": "...", "shape": \[...\], "Z": ..., "T": ..., "Channels": ..., "Height": ..., "Width": ...}

3.  **GET /slice**

    - Returns a 2D slice (PNG image).
    - **Query Params**: image_id=..., z=..., time=..., channel=...
    - **Response**: Binary PNG file

4.  **POST /analyze**

    - Runs PCA (or other analysis) on the image.
    - **JSON Body**: {"image_id": "...", "components": ...}
    - **Response**: {"image_id": "...", "n_components": ..., "pca_result": \[...\]}

5.  **GET /statistics**

    - Returns basic stats (mean, std, min, max) by channel.
    - **Query Params**: image_id=...
    - **Response**: {"mean": \[...\], "std": \[...\], "min": \[...\], "max": \[...\]}

### Example Requests

Assuming your service is at http://localhost:5000, here are some curl commands:

1.  bashCopyEditcurl -X POST -F file=@path/to/5d_image.tif http://localhost:5000/upload**Sample Response**:jsonCopyEdit{ "message": "File uploaded successfully", "image_id": "image_1"}
2.  bashCopyEditcurl "http://localhost:5000/metadata?image_id=image_1"**Sample Response**:jsonCopyEdit{ "dtype": "uint16", "shape": \[10, 5, 3, 512, 512\], "Z": 10, "T": 5, "Channels": 3, "Height": 512, "Width": 512}
3.  bashCopyEditcurl "http://localhost:5000/slice?image_id=image_1&z=0&time=0&channel=0" --output slice.png

    - Downloads a 2D slice as slice.png.

4.  bashCopyEditcurl -X POST -H "Content-Type: application/json" \\ -d '{"image_id": "image_1", "components": 2}' \\ http://localhost:5000/analyze**Sample Response**:jsonCopyEdit{ "image_id": "image_1", "n_components": 2, "pca_result": \[ \[ \[ ... \] \] \]}
5.  bashCopyEditcurl "http://localhost:5000/statistics?image_id=image_1"**Sample Response**:jsonCopyEdit{ "mean": \[ 45.3, 61.8, 120.2 \], "std": \[ 14.2, 18.7, 35.1 \], "min": \[ 0, 0, 0 \], "max": \[ 255, 255, 255 \]}

## Testing

This project uses **Pytest** for all tests (API, core, and DB). To run the test suite:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`  bashCopyEditpytest  `

- bashCopyEditpip install pytest-covpytest --cov=src --cov-report=term-missing
- Tests are organized by functionality in tests/test_api/, tests/test_core/, tests/test_db/.

## Asynchronous Tasks (Optional)

If you choose to run heavy operations asynchronously:

1.  bashCopyEditredis-server
2.  bashCopyEditcelery -A src.tasks.celery_app.celery worker --loglevel=info
3.  pythonCopyEditfrom src.tasks.async_tasks import heavy_pcaheavy_pca.delay(image_id="image_1", n_components=3)

## Troubleshooting

- **Database Connection Errors**: Ensure VERCEL_POSTGRES_URL is set correctly. Double-check your credentials and network access.
- **TIFF Loading Errors**: Verify that the TIFF files are truly multi-dimensional. The tifffile library might throw warnings if the file format is unusual.
- **Out-of-Memory**: For very large images, consider chunked I/O (see src/utils/chunk_io.py), or a cluster-based approach to distribute tasks.

## License

This project is provided under the MIT License. You are free to modify and distribute it as long as you include the license notice.

**Thank you for using the High-Dimensional Image Processing Microservice!** If you have any questions or suggestions, feel free to open an issue or contribute directly to the repository.
