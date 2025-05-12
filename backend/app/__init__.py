from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.services.logging_config import configure_logging
from werkzeug.exceptions import HTTPException
from pymongo.errors import PyMongoError
from app.services.error_handlers import DocumentProcessingError
from app.routes.gcp_test_routes import bp as gcp_test_bp

def create_app():
    # Initialize Flask application
    app = Flask(__name__)
    
    # Load configuration settings
    app.config.from_object(Config)
    
    # Enhanced CORS configuration
    CORS(
        app,
        resources={
            r"/documents*": {
                "origins": "http://localhost:3000",
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "expose_headers": ["Content-Disposition"],
                "supports_credentials": True,
                "max_age": 86400
            }
        }
    )
    
    configure_logging(app)
    
    # Initialize application components
    Config.init_app(app)
    
    # Import and register blueprints
    from app.routes.document_routes import bp as documents_bp
    from app.routes.health_routes import bp as health_bp
    
    app.register_blueprint(documents_bp, url_prefix='/documents')
    app.register_blueprint(health_bp)
    app.register_blueprint(gcp_test_bp)
    
    # Register error handlers
    from app.services.error_handlers import (
        handle_http_exception,
        handle_mongo_error,
        handle_document_processing_error,
        handle_general_exception
    )
    
    app.register_error_handler(HTTPException, handle_http_exception)
    app.register_error_handler(PyMongoError, handle_mongo_error)
    app.register_error_handler(DocumentProcessingError, handle_document_processing_error)
    app.register_error_handler(Exception, handle_general_exception)
    
    return app