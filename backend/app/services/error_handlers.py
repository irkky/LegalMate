from flask import jsonify, current_app
from werkzeug.exceptions import HTTPException
from pymongo.errors import PyMongoError
import logging

class DocumentProcessingError(Exception):
    """Original custom exception class without modifications"""
    def __init__(self, message, status_code=500, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def handle_http_exception(e):
    """Original HTTP exception handler"""
    current_app.logger.error(f"HTTP Error {e.code}: {e.description}")
    return jsonify({
        "error": e.name,
        "message": e.description
    }), e.code

def handle_mongo_error(e):
    """Original MongoDB error handler"""
    current_app.logger.error(f"MongoDB Error: {str(e)}")
    return jsonify({
        "error": "Database Error",
        "message": "Failed to process database operation"
    }), 500

def handle_document_processing_error(e):
    """Original custom error handler"""
    return jsonify(e.to_dict()), e.status_code

def handle_general_exception(e):
    """Original catch-all exception handler"""
    current_app.logger.exception("Unhandled Exception")
    return jsonify({
        "error": "Internal Server Error",
        "message": "An unexpected error occurred"
    }), 500