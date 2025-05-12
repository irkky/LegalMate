import os
from .gcp_client import (
    extract_clauses,
    analyze_entities,
    vertex_summarize
)

# Point Google SDK at your service account
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(
    os.path.dirname(__file__),
    "service-account.json"
)