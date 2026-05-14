
## 🧠 SHL Conversational Assessment Recommender

### 📋 Overview
This project implements a **FastAPI-based conversational agent** that recommends SHL assessments based on user queries.  
It is designed for the **SHL Research Intern (AI)** take-home assignment, demonstrating skills in agent design, context engineering, and retrieval-based recommendation.

---

### ⚙️ Features
- **Conversational Agent** that clarifies vague queries, refines context, and recommends relevant SHL assessments.  
- **Vector Search (FAISS)** for semantic retrieval using SentenceTransformer embeddings.  
- **CORS-enabled API** for easy integration with web clients.  
- **Schema-compliant endpoints** (`/health`, `/chat`) matching SHL’s evaluation format.

---

### 🧩 Tech Stack
| Component | Description |
|------------|-------------|
| **FastAPI** | Lightweight Python web framework for building APIs |
| **SentenceTransformers** | Embedding model (`all-MiniLM-L6-v2`) for semantic similarity |
| **FAISS** | Efficient vector search for recommendation retrieval |
| **NumPy** | Numerical operations for embeddings |
| **CORS Middleware** | Enables cross-origin requests for testing and deployment |

---

### 🚀 API Endpoints

#### **GET /health**
Returns service readiness.
```json
{"status": "ok"}
```

#### **GET /chat**
Quick browser testing endpoint.
Example:
```
http://127.0.0.1:8000/chat?query=mid-level java developer assessment
```
Response:
```json
{
  "reply": "Here are 3 assessments that match your query.",
  "recommendations": [
    {"name": "Java Developer Test", "url": "https://www.shl.com/java-test", "test_type": "K"},
    {"name": "OPQ32r", "url": "https://www.shl.com/opq32r", "test_type": "P"},
    {"name": "Numerical Reasoning Test", "url": "https://www.shl.com/numerical", "test_type": "A"}
  ],
  "end_of_conversation": false
}
```

#### **POST /chat**
Main conversational endpoint used by SHL’s evaluator.
Example body:
```json
{
  "messages": [
    {"role": "user", "content": "I need an assessment for a mid-level Java developer"}
  ]
}
```

---

### 🧠 Agent Behavior
- **Clarify vague queries** → asks for role, seniority, or skill area.  
- **Recommend assessments** → returns 1–10 items with names and URLs.  
- **Refine context** → updates shortlist when constraints change.  
- **Stay in scope** → only discusses SHL assessments.  

---

### 🧪 Local Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/shl-ai-recommender.git
   cd shl-ai-recommender
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   uvicorn app:app --reload
   ```
4. Test endpoints:
   - `http://127.0.0.1:8000/health`
   - `http://127.0.0.1:8000/chat`

---

### 🌐 Deployment (Render)
- **Build command:** `pip install -r requirements.txt`  
- **Start command:** `uvicorn app:app --host 0.0.0.0 --port 10000`  
- Public endpoint example:  
  ```
  https://shl-recommender.onrender.com
  ```

🧾 Notes
The catalog currently uses a static JSON fallback for local testing.

Replace it with real scraping or SHL’s product catalog API for production.

Ensure schema compliance for automated evaluation.