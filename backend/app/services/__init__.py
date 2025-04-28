# app/services/__init__.py
# Expose core service components

# Error handling
from .error_handlers import (
    DocumentProcessingError,
    handle_http_exception,
    handle_mongo_error,
    handle_document_processing_error,
    handle_general_exception
)

# Document processing utilities
from .document_processing import (
    extract_text_from_pdf,
    extract_text_from_docx,
    preprocess_text,
    extract_legal_entities,
    generate_summary,
    identify_legal_risks
)

# Logging configuration
from .logging_config import configure_logging

__all__ = [
    'DocumentProcessingError',
    'handle_http_exception',
    'handle_mongo_error',
    'handle_document_processing_error',
    'handle_general_exception',
    'extract_text_from_pdf',
    'extract_text_from_docx',
    'preprocess_text',
    'extract_legal_entities',
    'generate_summary',
    'identify_legal_risks',
    'configure_logging'
]