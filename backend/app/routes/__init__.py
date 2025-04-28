# app/routes/__init__.py
# Blueprint initialization without modifying original route behavior

from .document_routes import bp as documents_bp
from .health_routes import bp as health_bp

__all__ = [
    'documents_bp',
    'health_bp'
]