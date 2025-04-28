from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from bson import ObjectId
from datetime import datetime
from app.services import (
    DocumentProcessingError,
    extract_text_from_pdf,
    extract_text_from_docx,
    preprocess_text,
    extract_legal_entities,
    generate_summary,
    identify_legal_risks
)
from app.config import documents_collection
import os
import time

bp = Blueprint('documents', __name__)

@bp.route('/', methods=['POST'])
def create_document():
    try:
        if 'file' not in request.files:
            raise DocumentProcessingError("No file provided", 400)
        
        file = request.files['file']
        if not file or file.filename == '':
            raise DocumentProcessingError("Empty file submission", 400)

        filename = secure_filename(file.filename)
        if not filename.lower().endswith(('.pdf', '.docx')):
            raise DocumentProcessingError("Unsupported file type", 400)

        unique_filename = f"{time.time()}_{filename}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)

        # Text extraction
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        else:
            text = extract_text_from_docx(file_path)
        
        if not text:
            raise DocumentProcessingError("Text extraction failed", 500)

        text = preprocess_text(text)

        # NLP processing
        entities = extract_legal_entities(text)
        summary = generate_summary(text)
        risks = identify_legal_risks(text)

        # Database operations
        document_data = {
            "filename": unique_filename,
            "file_path": file_path,
            "text": text,
            "entities": entities,
            "summary": summary,
            "risks": risks,
            "upload_time": datetime.utcnow(),
            "status": "processed"
        }
        
        result = documents_collection.insert_one(document_data)
        doc_id = str(result.inserted_id)

        return jsonify({
            "id": doc_id,
            "filename": unique_filename,
            "status": "processed",
            "links": {
                "self": f"/documents/{doc_id}",
                "analysis": f"/analysis/{doc_id}"
            }
        }), 201

    except DocumentProcessingError:
        raise
    except Exception as e:
        current_app.logger.error(f"Unexpected error: {str(e)}")
        raise DocumentProcessingError("Internal server error", 500)

@bp.route('/', methods=['GET'])
def list_documents():
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        skip = (page - 1) * limit

        total = documents_collection.count_documents({})
        cursor = documents_collection.find().skip(skip).limit(limit)
        
        documents = []
        for doc in cursor:
            documents.append({
                "id": str(doc['_id']),
                "filename": doc.get('filename', ''),
                "upload_date": doc.get('upload_time', '').isoformat(),
                "status": doc.get('status', 'unknown')
            })

        return jsonify({
            "data": documents,
            "pagination": {
                "total": total,
                "page": page,
                "limit": limit,
                "next": f"/documents?page={page+1}&limit={limit}" if (page * limit) < total else None
            }
        }), 200

    except Exception as e:
        current_app.logger.error(f"Document listing error: {str(e)}")
        raise DocumentProcessingError("Failed to retrieve documents", 500)

@bp.route('/<string:doc_id>', methods=['GET'])
def get_document(doc_id):
    try:
        document = documents_collection.find_one({"_id": ObjectId(doc_id)})
        if not document:
            raise DocumentProcessingError("Document not found", 404)

        return jsonify({
            "id": str(document['_id']),
            "filename": document.get('filename', ''),
            "upload_date": document.get('upload_time', '').isoformat(),
            "analysis": {
                "entities": document.get('entities', {}),
                "risks": document.get('risks', []),
                "summary": document.get('summary', '')
            },
            "text": document.get('text', ''),
            "links": {
                "download": f"/documents/{doc_id}/file",
                "delete": f"/documents/{doc_id}"
            }
        }), 200

    except Exception as e:
        current_app.logger.error(f"Document retrieval error: {str(e)}")
        raise DocumentProcessingError("Invalid document ID", 400)

@bp.route('/<string:doc_id>', methods=['DELETE'])
def delete_document(doc_id):
    try:
        result = documents_collection.delete_one({"_id": ObjectId(doc_id)})
        if result.deleted_count == 0:
            raise DocumentProcessingError("Document not found", 404)
        return jsonify({"message": "Document deleted successfully"}), 204
    except Exception as e:
        current_app.logger.error(f"Document deletion error: {str(e)}")
        raise DocumentProcessingError("Invalid document ID", 400)