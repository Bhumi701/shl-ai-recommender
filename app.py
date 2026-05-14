from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import json

app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Step 1: Load catalog (fallback JSON for local testing)
# Replace this with real scraping or API later
catalog = [
    {"name": "OPQ32r", "url": "https://www.shl.com/opq32r", "description": "Personality assessment", "test_type": "P"},
    {"name": "Java Developer Test", "url": "https://www.shl.com/java-test", "description": "Technical skill test", "test_type": "K"},
    {"name": "Numerical Reasoning Test", "url": "https://www.shl.com/numerical", "description": "Numerical ability assessment", "test_type": "A"}
]

# Step 2: Build vector index safely
texts = [item["description"] for item in catalog if item["description"]]
embeddings = model.encode(texts)

if len(embeddings) == 0:
    raise ValueError("Catalog is empty. Please check scraping or JSON fallback.")

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

def search_catalog(query, k=10):
    q_emb = model.encode([query])
    D, I = index.search(np.array(q_emb), k)
    return [catalog[i] for i in I[0]]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/chat")
def chat_get(query: str = "assessment"):
    """GET endpoint for testing /chat endpoint from browser"""
    user_msg = query
    
    # Clarify vague queries
    if "assessment" in user_msg.lower() and len(user_msg.split()) < 4:
        return {
            "reply": "Could you clarify role, seniority, or skill area?",
            "recommendations": [],
            "end_of_conversation": False
        }

    # Search catalog
    results = search_catalog(user_msg, k=5)
    recs = [{"name": r["name"], "url": r["url"], "test_type": r["test_type"]} for r in results]

    return {
        "reply": f"Here are {len(recs)} assessments that match your query.",
        "recommendations": recs,
        "end_of_conversation": False
    }

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    messages = data.get("messages", [])
    user_msg = messages[-1]["content"] if messages else ""

    # Clarify vague queries
    if "assessment" in user_msg.lower() and len(user_msg.split()) < 4:
        return {
            "reply": "Could you clarify role, seniority, or skill area?",
            "recommendations": [],
            "end_of_conversation": False
        }

    # Search catalog
    results = search_catalog(user_msg, k=5)
    recs = [{"name": r["name"], "url": r["url"], "test_type": r["test_type"]} for r in results]

    return {
        "reply": f"Here are {len(recs)} assessments that match your query.",
        "recommendations": recs,
        "end_of_conversation": False
    }
