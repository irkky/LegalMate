from flask import current_app
import PyPDF2
import docx
import spacy
from transformers import pipeline
from collections import defaultdict
import logging

# Initialize NLP components (same as original)
nlp = spacy.load("en_core_web_sm")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Original risk keywords and settings
RISK_KEYWORDS = {
    "indemnification": ["indemnify", "hold harmless"],
    "termination": ["terminate", "expiry"],
    "liability": ["liability", "damages"],
    "confidentiality": ["confidential", "non-disclosure"]
}

AMBIGUOUS_TERMS = ["reasonable", "material adverse effect", "sole discretion"]

def extract_text_from_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            return ''.join([page.extract_text() for page in reader.pages if page.extract_text()])
    except Exception as e:
        current_app.logger.error(f"PDF extraction error: {e}")
        return None

def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])
    except Exception as e:
        current_app.logger.error(f"DOCX extraction error: {e}")
        return None

def preprocess_text(text):
    text = ' '.join(text.split())
    return ''.join(char for char in text if char.isalnum() or char in [' ', '.', ',', '\n'])

def extract_legal_entities(text):
    doc = nlp(text)
    entities = defaultdict(list)
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PERSON", "DATE", "LAW"]:
            entities[ent.label_].append(ent.text)
    for sent in doc.sents:
        if "governing law" in sent.text.lower():
            entities["CLAUSES"].append("Governing Law")
        if "force majeure" in sent.text.lower():
            entities["CLAUSES"].append("Force Majeure")
    return dict(entities)

def generate_summary(text):
    try:
        return summarizer(text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
    except Exception as e:
        current_app.logger.error(f"Summarization failed: {e}")
        return None

def identify_legal_risks(text):
    risks = []
    doc = nlp(text.lower())
    
    # Original clause checks
    if not any("governing law" in sent.text for sent in doc.sents):
        risks.append("Missing Governing Law clause")
    
    # Original ambiguous terms check
    risks += [f"Ambiguous term: {term}" for term in AMBIGUOUS_TERMS if term in text]
    
    # Original risk keyword checks
    for category, keywords in RISK_KEYWORDS.items():
        if any(keyword in text.lower() for keyword in keywords):
            risks.append(f"Potential risk in {category} clause")
    
    return risks