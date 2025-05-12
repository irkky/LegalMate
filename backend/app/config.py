import os
from pathlib import Path
from pymongo import MongoClient
import vertexai
from vertexai.preview.language_models import TextGenerationModel
from google.cloud import language_v1
import logging

# Configure logging for better debugging and monitoring
logging.basicConfig(level=logging.INFO)

# --------------------------------------------------
# GCP Credentials and Environment
# --------------------------------------------------
# Path to service-account.json (ensure it's in .gitignore to avoid exposing credentials)
GCP_CREDENTIALS = Path(__file__).resolve().parent.parent / 'gcp' / 'service-account.json'

# Set the environment variable for GCP credentials if the file exists
if GCP_CREDENTIALS.exists():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(GCP_CREDENTIALS)
else:
    logging.error(f"GCP credentials file not found at {GCP_CREDENTIALS}. Please ensure it exists.")
    raise FileNotFoundError("GCP credentials file is missing.")

# Load environment variables for GCP settings with validation
PROJECT_ID = os.getenv('GCP_PROJECT_ID', 'practical-now-456807-u9')
LOCATION = os.getenv('GCP_LOCATION', 'us-central1')

# Ensure PROJECT_ID is set (critical for GCP services)
if not PROJECT_ID:
    logging.error("GCP_PROJECT_ID environment variable is not set. Please provide a valid project ID.")
    raise EnvironmentError("GCP_PROJECT_ID is required for GCP services.")

# --------------------------------------------------
# Initialize GCP Clients with Error Handling
# --------------------------------------------------
try:
    # Vertex AI for text generation (summarization)
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    VERTEX_SUMMARY_MODEL = TextGenerationModel.from_pretrained('text-bison@001')
except Exception as e:
    logging.error(f"Failed to initialize Vertex AI: {e}")
    raise

try:
    # Natural Language API for entity extraction
    NLP_CLIENT = language_v1.LanguageServiceClient()
except Exception as e:
    logging.error(f"Failed to initialize Natural Language API client: {e}")
    raise

# --------------------------------------------------
# MongoDB Configuration
# --------------------------------------------------
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
MONGODB_DB = os.getenv('MONGODB_DB', 'legalmate_db')

try:
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DB]
    documents_collection = db['documents']
except Exception as e:
    logging.error(f"Failed to connect to MongoDB: {e}")
    raise

class Config:
    # File upload settings
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads/')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit for uploads
    JSON_SORT_KEYS = False

    # Expose GCP clients as class attributes
    NLP_CLIENT = NLP_CLIENT
    VERTEX_MODEL = VERTEX_SUMMARY_MODEL

    @classmethod
    def init_app(cls, app):
        # Ensure upload folder exists
        upload_folder = app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
            app.logger.info(f'Created upload directory: {upload_folder}')

        # Create MongoDB indexes for efficient querying
        try:
            documents_collection.create_index('filename')
            documents_collection.create_index('upload_time')
            app.logger.info('Created database indexes for filename and upload_time')
        except Exception as e:
            app.logger.error(f'Index creation failed: {e}')