# 📄 Multi-File Processing RAG Application

> A Retrieval-Augmented Generation (RAG) chatbot that lets users upload documents (PDF, Excel, PowerPoint, CSV) and ask natural language questions — powered by Google Gemini 1.5, LangChain, and FAISS vector search.

---

## 📌 Project Overview

This application enables **conversational Q&A over your own documents**. Users upload files, the app intelligently chunks and embeds the content into a FAISS vector store, and then answers questions using Google's Gemini 1.5 model — all through a clean Streamlit chat interface.

Built with production-readiness in mind: containerized via Docker and monitored via LangSmith.

---

## ✨ Key Features

| Feature | Description |
|--------|-------------|
| 📂 Multi-format support | Ingests PDF, XLSX, PPTX, and CSV files |
| 🔍 Semantic search | FAISS vector store for fast, relevant document retrieval |
| 🤖 Conversational AI | Google Gemini 1.5 powers context-aware responses |
| ✂️ Smart chunking | Text splitting optimized for accurate embedding |
| 📊 Pipeline monitoring | LangSmith integration for logging and observability |
| 🐳 Dockerized | One-command deployment via Docker |

---

## 🚀 Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python 3.9+ |
| LLM | Google Gemini 1.5 (via Google Generative AI) |
| RAG Framework | LangChain |
| Vector Database | FAISS |
| Frontend | Streamlit |
| Monitoring | LangSmith |
| Containerization | Docker |

---

## 🏗️ Architecture

```
User uploads file (PDF / XLSX / PPTX / CSV)
        ↓
Text Extraction & Chunking
        ↓
Embedding Generation (Google Generative AI Embeddings)
        ↓
FAISS Vector Store (stored in-memory)
        ↓
User asks a question
        ↓
Semantic Retrieval → Gemini 1.5 → Conversational Response
        ↓
LangSmith logs interaction for monitoring
```

---

## ⚙️ Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/multi-file-rag-app.git
cd multi-file-rag-app
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```
> Requires Python 3.9 or higher.

### 3. Configure environment variables

Create a `.env` file in the root directory:
```bash
GOOGLE_API_KEY=<your-google-api-key>
LANGCHAIN_API_KEY=<your-langchain-api-key>
LANGCHAIN_ENDPOINT=<your-langchain-endpoint>
LANGCHAIN_PROJECT=<your-project-name>
LANGSMITH_API_KEY=<your-langsmith-api-key>
```

### 4. Run the app
```bash
streamlit run app.py
```
Visit `http://localhost:8501` in your browser.

---

## 🐳 Docker Deployment

### Build the image
```bash
docker build -t multi-file-rag-app .
```

### Run the container
```bash
docker run -p 8501:8501 multi-file-rag-app
```

The app will be live at `http://localhost:8501`.

<details>
<summary>View Dockerfile</summary>

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```
</details>

---

## 📡 LangSmith Monitoring

All key pipeline events are automatically logged to LangSmith, including:
- File upload and text extraction
- Vector store updates
- Model queries and responses

Ensure your `LANGSMITH_API_KEY` is set in `.env` to enable observability.

---

## 💡 Key Learnings & Takeaways

- Designed and implemented a full **end-to-end RAG pipeline** from document ingestion to response generation
- Explored **chunking strategies** and their impact on retrieval quality and embedding efficiency
- Integrated **LLM observability** tooling (LangSmith) for production-grade monitoring
- Containerized an ML application with Docker for **reproducible, portable deployment**

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

*An exploration of RAG architecture, LLM integration, and production ML deployment patterns.*
