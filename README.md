## Multi-file Processing RAG Application

This application processes uploaded files such as PDFs, Excel, PowerPoint, or CSV files, chunks the text, and stores it in a FAISS vector database for question-answering using LangChain and Google Generative AI.

### Features:
- File processing for multiple formats: PDF, XLSX, PPTX, CSV
- Embeddings and vector storage using FAISS
- Question-answering based on uploaded files
- Conversational interaction with a chatbot model (Google Generative AI)
- Chunking and text splitting for efficient embedding
- Integration with LangSmith for monitoring and logging the AI pipeline

### Dependencies:
To install the dependencies, make sure you have Python 3.9 or higher. Use the following command to install the required packages:

```bash
pip install -r requirements.txt
```

### Usage:

1. **Environment Variables:**
   Create a `.env` file with the following variables:

   ```bash
   GOOGLE_API_KEY=<your-google-api-key>
   LANGCHAIN_API_KEY=<your-langchain-api-key>
   LANGCHAIN_ENDPOINT=<your-langchain-endpoint>
   LANGCHAIN_PROJECT=<your-project-name>
   LANGSMITH_API_KEY=<your-langsmith-api-key>
   ```

2. **File Upload:**
   Upload PDF, Excel, PowerPoint, or CSV files using the file uploader in the sidebar. The files are then processed, chunked, and stored in a FAISS vector store.

3. **Chat Interface:**
   Ask questions in the chat interface. The system will use the stored vector database to retrieve the most relevant documents and generate a response using a conversational model (Google's Gemini 1.5).

4. **LangSmith Monitoring:**
   LangSmith is used to monitor the application’s performance and log interactions.

   To enable LangSmith monitoring, ensure you have an API key and that it is set up in your `.env` file. The application will log and monitor all major interactions, including file processing, vector database updates, and model responses.

5. **Run the Application:**

   To run the app locally, use:

   ```bash
   streamlit run app.py
   ```

### Docker Setup:

1. **Dockerfile**:
   The provided Dockerfile helps you containerize the application.

   ```Dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt .

   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8501

   CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build the Docker image:**

   ```bash
   docker build -t multi-file-processing-app .
   ```

3. **Run the Docker container:**

   ```bash
   docker run -p 8501:8501 multi-file-processing-app
   ```

---

### Updated `app.py` with LangSmith integration:

---

```python
from langsmith import LangSmithTracer

# Initialize LangSmith monitoring
tracer = LangSmithTracer()

# Setting up LangSmith tracer in LangChain
import langchain
langchain.trace_with(tracer)

# Continue with your existing app logic
# All major events, such as file uploads, vector database updates, and model responses, will be logged and monitored via LangSmith.

# File Processing, Chatbot logic as described earlier
```

---

### Notes:
- **LangSmith API Key:** Ensure you have a valid LangSmith API key. Add it to your `.env` file to enable LangSmith monitoring.
- **LangSmith Dashboard:** You can view all logs and metrics related to your app’s performance in the LangSmith dashboard.
