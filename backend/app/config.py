import os
from pymongo import MongoClient

# Initialize MongoDB connection (maintains original top-level initialization)
client = MongoClient("mongodb://localhost:27017/")
db = client["legalmate_db"]
documents_collection = db["documents"]

class Config:
    # Maintain original configuration values
    UPLOAD_FOLDER = 'uploads/'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    JSON_SORT_KEYS = False

    @classmethod
    def init_app(cls, app):
        # Original startup configuration from if __name__ == '__main__'
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
            app.logger.info("Created upload directory")
        
        # Original index creation logic
        try:
            documents_collection.create_index("filename")
            documents_collection.create_index("upload_time")
            app.logger.info("Created database indexes")
        except Exception as e:
            app.logger.error(f"Index creation failed: {str(e)}")