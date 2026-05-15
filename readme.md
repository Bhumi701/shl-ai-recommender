
# 🧠 SHL Conversational Assessment Recommender

## 📋 Overview
This project implements a **FastAPI-based conversational agent** that recommends SHL assessments based on user queries.  

It was developed as part of the **SHL Research Intern (AI) take-home assignment**, showcasing skills in agent design, context engineering, and retrieval-based recommendation.

---

## ⚙️ Features
- Conversational Agent that clarifies vague queries, refines context, and recommends relevant SHL assessments.  
- **TF‑IDF + Cosine Similarity** for lightweight semantic retrieval.  
- **CORS-enabled API** for easy integration with web clients.  
- Schema-compliant endpoints (`/health`, `/chat`) matching SHL’s evaluation format.  

---

## 🧩 Tech Stack

| Component            | Description |
|----------------------|-------------|
| **FastAPI**          | Lightweight Python web framework for building APIs |
| **scikit-learn**     | TF‑IDF vectorizer and cosine similarity |
| **NumPy**            | Numerical operations for similarity ranking |
| **CORS Middleware**  | Enables cross-origin requests for testing and deployment |

---

## 🚀 API Endpoints

### ✅ Health Check
- **GET /health**  
- Returns service readiness.  
- Example:  
  ```json
  {"status": "ok"}
  ```  
- Live URL: [https://shl-ai-recommender-0j68.onrender.com/health](https://shl-ai-recommender-0j68.onrender.com/health)

---

### 💬 Conversational Endpoint
- **GET /chat**  
  - Quick browser testing with query parameter.  
  - Example:  
    ```
    https://shl-ai-recommender-0j68.onrender.com/chat?query=mid-level java developer assessment
    ```

- **POST /chat**  
  - Main conversational endpoint used by SHL’s evaluator.  
  - Example request:  
    ```json
    {
      "messages": [
        {"role": "user", "content": "I need an assessment for a mid-level Java developer"}
      ]
    }
    ```  
  - Example response:  
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

- Live URL: [https://shl-ai-recommender-0j68.onrender.com/chat](https://shl-ai-recommender-0j68.onrender.com/chat)

---

## 🧠 Agent Behavior
- **Clarify vague queries** → asks for role, seniority level, or skill area.  
- **Recommend assessments** → returns 1–10 items with names and URLs.  
- **Refine context** → updates shortlist when constraints change.  
- **Stay in scope** → only discusses SHL assessments.  

---

## 🧪 Local Setup
```bash
# Clone the repository
git clone https://github.com/<your-username>/shl-ai-recommender.git
cd shl-ai-recommender

# Install dependencies
pip install -r requirements.txt

# Run the app locally
uvicorn app:app --reload
```

Test endpoints locally:  
- [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)  
- [http://127.0.0.1:8000/chat](http://127.0.0.1:8000/chat)  

---

## 🌐 Deployment (Render)
- **Build command:**  
  ```bash
  pip install -r requirements.txt
  ```
- **Start command:**  
  ```bash
  uvicorn app:app --host 0.0.0.0 --port 10000
  ```
- **Base URL (Live):**  
  [https://shl-ai-recommender-0j68.onrender.com](https://shl-ai-recommender-0j68.onrender.com)

---

## 🧾 Notes
- The catalog currently uses a **static JSON fallback** for local testing.  
- Replace with **real scraping or SHL’s product catalog API** for production.  
- Ensure **schema compliance** for automated evaluation.  

---
