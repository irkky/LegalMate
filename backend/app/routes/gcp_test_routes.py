from flask import Blueprint, request, jsonify, current_app
from app.services.document_processing import (
    extract_text_from_pdf,
    extract_text_from_docx,
    preprocess_text,
    extract_clauses_from_document,
    extract_legal_entities,
    generate_summary,
    identify_legal_risks
)

bp = Blueprint('gcp_test', __name__, url_prefix='/gcp-test')

@bp.route('/document', methods=['POST'])
def run_gcp_pipeline():
    """
    Upload a PDF or DOCX and see:
      - raw text,
      - GCP-extracted clauses,
      - GCP NLP entities,
      - Vertex summary,
      - risk list
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    filename = file.filename.lower()
    if not filename.endswith(('.pdf', '.docx')):
        return jsonify({"error": "Unsupported file type"}), 400

    # 1) Save to temp and extract text
    tmp_path = f"/tmp/{filename}"
    file.save(tmp_path)

    text = (extract_text_from_pdf if filename.endswith('.pdf') else extract_text_from_docx)(tmp_path)
    if not text:
        return jsonify({"error": "Text extraction failed"}), 500

    text = preprocess_text(text)

    # 2) Run GCP clause extractor
    clauses = extract_clauses_from_document(tmp_path)

    # 3) Run GCP NLP entity extractor
    entities = extract_legal_entities(text)

    # 4) Run Vertex AI summarizer
    summary = generate_summary(text)

    # 5) Run local risk identifier
    risks = identify_legal_risks(text)

    return jsonify({
        "text_snippet": text[:300] + ("…" if len(text) > 300 else ""),
        "clauses": clauses,
        "entities": entities,
        "summary": summary,
        "risks": risks
    }), 200
