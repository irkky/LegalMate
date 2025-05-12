import os
from google.cloud import documentai_v1 as documentai
from google.cloud import language_v1
from google.cloud import aiplatform

# GCP settings
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "practical-now-456807-u9")
LOCATION = os.getenv("GCP_LOCATION", "us-central1")

# Document AI setup
PROCESSOR_ID = os.getenv("DOC_AI_PROCESSOR_ID", "77c5199ac4ed9e8a")
PROCESSOR_NAME = f"projects/{PROJECT_ID}/locations/{LOCATION}/processors/{PROCESSOR_ID}"

def extract_clauses(file_path: str) -> list:
    """
    Extracts clauses using Google Cloud Document AI.
    Returns a list of extracted clause texts.
    """
    client = documentai.DocumentProcessorServiceClient()
    with open(file_path, "rb") as f:
        content = f.read()
    request = documentai.ProcessRequest(
        name=PROCESSOR_NAME,
        raw_document=documentai.RawDocument(
            content=content,
            mime_type="application/pdf" if file_path.lower().endswith(".pdf") else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ),
    )
    result = client.process_document(request=request)
    clauses = []
    # Traverse document entities or form fields
    for entity in result.document.entities:
        if entity.type_.lower() == "clause":
            clauses.append(entity.mention_text)
    return clauses


def analyze_entities(text: str) -> dict:
    """
    Uses Google Cloud Natural Language API to extract named entities.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_entities(document=document)
    entities = {}
    for ent in response.entities:
        ent_type = language_v1.Entity.Type(ent.type_).name
        entities.setdefault(ent_type, []).append(ent.name)
    return entities


def vertex_summarize(text: str, max_output_tokens: int = 150) -> str:
    """
    Summarize text using Vertex AI text generation model (e.g., `text-bison@001`).
    """
    aiplatform.init(
        project=PROJECT_ID,
        location=LOCATION
    )
    model = aiplatform.TextGenerationModel.from_pretrained("text-bison@001")
    response = model.predict(
        text,
        max_output_tokens=max_output_tokens,
        temperature=0.2
    )
    return response.text
