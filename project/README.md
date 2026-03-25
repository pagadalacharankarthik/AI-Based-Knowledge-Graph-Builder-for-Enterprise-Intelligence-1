# 🧠 AI Knowledge Graph Builder & RAG Dashboard
Built by **Charan Karthik**

An advanced, end-to-end mission-ready AI system that transforms raw email data into a searchable, visual, and intelligent knowledge engine using Hybrid RAG and Graph Analytics.

---

## 🚀 Project Overview
This project unifies four critical milestones into a cohesive, production-ready application:
1.  **Milestone 1**: Data Ingestion (Cleaning, enrichment, and normalization).
2.  **Milestone 2**: Knowledge Graph construction using **Neo4j**.
3.  **Milestone 3**: Hybrid RAG pipeline using **FAISS** and **Groq LLM**.
4.  **Milestone 4**: Final Integrated Dashboard & UI.

---

## 🧩 Technical Deep Dive

### 1. Hybrid RAG (Retrieval-Augmented Generation)
The system uses a unique hybrid retrieval strategy:
-   **Vector Search**: Finds semantically similar emails based on the query.
-   **Graph Context**: For each retrieved email, the system extracts key entities (PERSON, ORG) and queries Neo4j to find their immediate relationships (e.g., who else they are related to).
-   **Context Fusion**: Both the raw email text and the graph relationship triplets are fed into the LLM as high-density context.

### 2. Vector Database & Embeddings
-   **Model**: `all-MiniLM-L6-v2` (Sentence-Transformers).
-   **Storage**: **FAISS** (Facebook AI Similarity Search).
-   **Process**: Emails are cleaned, concatenated with their entity metadata, and encoded into 384-dimensional vectors for fast L2-distance similarity search.

### 3. Neo4j Knowledge Graph
-   **Nodes**: `PERSON`, `ORG`, `GPE`, `DATE`.
-   **Relationships**: `RELATED_TO`.
-   **Logic**: Uses a robust triplet extraction pipeline that canonicalizes entity names (e.g., merging "Ken Lay" and "Kenneth Lay") to ensure graph density and accuracy.

---

## 📂 Project Structure
```
project/
├── Milestone 4/            # Final Integrated Application
│   ├── frontend/
│   │   └── app.py          # Dashboard (Streamlit UI)
│   └── backend/
│       ├── rag.py          # RAG (FAISS + LLM) Logic
│       ├── graph.py        # Knowledge Graph (Neo4j) logic
│       ├── initialize_db.py # One-time Database Initialization
│       └── data/
│           └── cleaned_enron_emails.csv # Real Enron Dataset
├── requirements.txt        # Combined Dependencies
└── README.md               # You are here
```

---

## 🛠️ Setup & SOP (Standard Operating Procedure)

### Standard Operating Procedure (SOP)
1.  **Environment Setup**: Ensure Python 3.9+ is active and all API keys (Groq, Neo4j) are ready.
2.  **Dependency Handling**: Install all packages from the root `requirements.txt`.
3.  **Data Generation**: Run the Milestone 1 scripts to produce the `cleaned_enron_emails.csv`.
4.  **Graph Initialization**: Run `initialize_db.py` to wipe/populate the Neo4j instance.
5.  **Application Launch**: Start Streamlit through the `frontend/app.py` entry point.

---

## 🌐 How to Deploy to Streamlit Cloud (Live Link Guide)

Follow these steps to make your project live:

1.  **Prepare GitHub**:
    - Push your entire project folder to a public GitHub repository.
    - Ensure `requirements.txt` is in the root directory.
2.  **Connect to Streamlit Cloud**:
    - Log in to [Streamlit Cloud](https://share.streamlit.io/).
    - Click **"New app"**.
    - Select your Repository, Branch, and for **Main file path**, enter: `Milestone 4/frontend/app.py`.
3.  **Configure Secrets (CRITICAL)**:
    - Click **"Advanced settings"** -> **"Secrets"**.
    - Paste your credentials in TOML format:
      ```toml
      NEO4J_URI = "neo4j+s://your-db-id.databases.neo4j.io"
      NEO4J_USER = "neo4j"
      NEO4J_PASSWORD = "your-password"
      LLM_API_KEY = "your-groq-api-key"
      ```
4.  **Deploy**:
    - Click **"Deploy"**. Streamlit will provision a server, install dependencies, and give you a live URL (e.g., `https://your-app-name.streamlit.app`).

---

## 🔍 Example Queries
- *"Who is discussing energy trading?"*
- *"What are the most frequent companies mentioned?"*
- *"Who is involved in California power market discussions?"*

---
© 2026 AI Knowledge Graph Builder | Build by **Charan Karthik**
