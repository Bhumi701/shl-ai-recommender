from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


catalog = [
    {"name": "OPQ32r",                 "url": "https://www.shl.com/opq32r",    "description": "Personality assessment for workplace behaviour",  "test_type": "P"},
    {"name": "Java Developer Test",    "url": "https://www.shl.com/java-test", "description": "Technical skill test for Java developers",          "test_type": "K"},
    {"name": "Numerical Reasoning Test","url": "https://www.shl.com/numerical","description": "Numerical ability and data interpretation assessment","test_type": "A"},
]


texts = [item["description"] for item in catalog]

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(texts)   # sparse matrix, very light


def search_catalog(query: str, k: int = 10):
    """Return top-k catalog items ranked by TF-IDF cosine similarity."""
    q_vec = vectorizer.transform([query])
    sims  = cosine_similarity(q_vec, tfidf_matrix).flatten()
    top_k = np.argsort(sims)[-k:][::-1]
    return [catalog[i] for i in top_k if sims[i] > 0]   # skip zero-score items


def _is_vague(msg: str) -> bool:
    return "assessment" in msg.lower() and len(msg.split()) < 4


def _build_response(user_msg: str):
    if _is_vague(user_msg):
        return {
            "reply": "Could you clarify the role, seniority level, or skill area you need an assessment for?",
            "recommendations": [],
            "end_of_conversation": False,
        }

    results = search_catalog(user_msg, k=5)
    recs    = [{"name": r["name"], "url": r["url"], "test_type": r["test_type"]} for r in results]

    reply = (
        f"Here are {len(recs)} assessments that match your query."
        if recs
        else "No matching assessments found. Try describing the role or skill you need."
    )
    return {"reply": reply, "recommendations": recs, "end_of_conversation": False}



@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/chat")
def chat_get(query: str = "assessment"):
    return _build_response(query)


@app.post("/chat")
async def chat_post(request: Request):
    data     = await request.json()
    messages = data.get("messages", [])
    user_msg = messages[-1]["content"] if messages else ""
    return _build_response(user_msg)