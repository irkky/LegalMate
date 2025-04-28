from werkzeug.utils import secure_filename
import os
import time

def save_uploaded_file(file):
    """Original file saving logic from create_document endpoint"""
    original_filename = secure_filename(file.filename)
    unique_filename = f"{time.time()}_{original_filename}"
    file_path = os.path.join(os.getcwd(), 'uploads', unique_filename)  # Maintains original path logic
    file.save(file_path)
    return unique_filename, file_path