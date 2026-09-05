"""
Loads all 15 ComplianceRule objects, embeds them, and stores them
in a persistent ChromaDB collection for retrieval.
Run this once (and again any time rules_data.py changes).
"""

import chromadb
from chromadb.utils import embedding_functions
from rules_data import RULES

client = chromadb.PersistentClient(path="./chroma_db")

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

try:
    client.delete_collection("compliance_rules")
except Exception:
    pass

collection = client.create_collection(
    name="compliance_rules",
    embedding_function=embedding_fn,
)

documents = []
metadatas = []
ids = []

for rule in RULES:
    embed_text = (
        f"{rule.title}. {rule.condition} "
        f"Relevant fields: {', '.join(rule.field_dependencies)}. "
        f"Scenario: {rule.scenario}."
    )
    documents.append(embed_text)
    ids.append(rule.check_id)
    metadatas.append({
        "check_id": rule.check_id,
        "scenario": rule.scenario,
        "title": rule.title,
        "code": rule.code,
        "section": rule.section,
        "severity": rule.severity,
        "violation_type": rule.violation_type,
        "applies_when_json": str(rule.applies_when),
        "field_dependencies_csv": ",".join(rule.field_dependencies),
    })

collection.add(documents=documents, metadatas=metadatas, ids=ids)

print(f"Indexed {collection.count()} rules into ChromaDB ✅")