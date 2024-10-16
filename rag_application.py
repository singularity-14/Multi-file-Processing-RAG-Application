import os
import fitz  # PyMuPDF for PDF processing
import tempfile
import streamlit as st
from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_community.document_loaders import UnstructuredPowerPointLoader


# Loading the Environmental Variables
load_dotenv()
os.environ["GOOGLE_API_KEY"]=os.getenv("GOOGLE_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_ENDPOINT"]=os.getenv("LANGCHAIN_ENDPOINT")
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")

def file_processing(uploaded_files):
    """
    Processes a list of uploaded files (PDF, XLSX, PPT, CSV) and extracts content.

    Args:
        uploaded_files (list): List of uploaded files.

    Returns:
        list: List of Document objects containing text and metadata for each file type.
    """
    processed_files = []
    
    for file in uploaded_files:
        file_name = file.name
        file_extension = file_name.split(".")[-1].lower()

        # Process PDF files
        if file_extension == "pdf":
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(file.read())
                    tmp_file_path = tmp_file.name
                    
                    doc = fitz.open(tmp_file_path)
                    for page_num in range(len(doc)):
                        page = doc.load_page(page_num)
                        text = page.get_text()
                        document = Document(page_content=text, metadata={"source": file_name, "page_number": page_num + 1})
                        processed_files.append(document)
            except Exception as e:
                st.sidebar.error(f"Error processing PDF file {file_name}: {e}")

        # Process Excel files
        elif file_extension in ["xlsx", "xls"]:
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp_file:
                    tmp_file.write(file.read())
                    tmp_file_path = tmp_file.name
                
                xlsx_loader = UnstructuredExcelLoader(tmp_file_path, mode="elements")
                xlsx_docs = xlsx_loader.load()
                processed_files.extend(xlsx_docs)
            except Exception as e:
                st.sidebar.error(f"Error processing Excel file {file_name}: {e}")

        # Process PowerPoint files
        elif file_extension == "pptx":
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as tmp_file:
                    tmp_file.write(file.read())
                    tmp_file_path = tmp_file.name
                    
                pptx_loader = UnstructuredPowerPointLoader(tmp_file_path)
                pptx_data = pptx_loader.load()
                processed_files.extend(pptx_data)
            except Exception as e:
                st.sidebar.error(f"Error processing PowerPoint file {file_name}: {e}")

        # Process CSV files
        elif file_extension == "csv":
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
                    tmp_file.write(file.read())
                    tmp_file_path = tmp_file.name
                    
                csv_loader = CSVLoader(tmp_file_path)
                csv_data = csv_loader.load()
                processed_files.extend(csv_data)
            except Exception as e:
                st.sidebar.error(f"Error processing CSV file {file_name}: {e}")

        else:
            st.sidebar.warning(f"Unsupported file type: {file_extension}")
            
    return processed_files

# Text Chunking, Adding Documents with thier embeddings in FAISS Vecotr Store and Saving it
def text_chunking_uploading(pdf_text):
    """
    Chunks text from uploaded PDFs and uploads it to a vector database.

    Args:
        pdf_text (list): List of Document objects containing text and metadata.

    Returns:
        FAISS or None: The vector database instance if successful, None otherwise.
    """
    if not pdf_text:
        return None
    
    try:
        # Initialize the text splitter with defined chunk size and overlap
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
        
        # Split the provided documents into smaller chunks
        text_documents = text_splitter.split_documents(pdf_text)
        
        # Create embeddings for the document chunks and store them in a FAISS vector database
        vector_db = FAISS.from_documents(text_documents, HuggingFaceBgeEmbeddings())
        
        # Save the FAISS database locally
        vector_db.save_local("Vector_Store/vector_store_of_recently_uploaded_pdfs")
        
        return vector_db
    
    except Exception as e:
        print(f"An error occurred while processing and uploading the text: {e}")
        return None

# Loading the gemini-1.5-flash Model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.5,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Prompt Template
template = """
You are a good chatbot developed by XYZ company.

Instructions:
1. Your job is to answer the question based on the provided context; don't go out of context to answer the question.
2. If Someone appreciate you then respond with Polite Asnwer.
2. If the answer is not present in the context, respond with "I don't know the answer."

context:
{context}

question:
{question}

Answer:
"""

# Retriver Chain to Generate Answer
def chain(question, vector_db):
    """
    Processes a question by retrieving relevant information from the vector database
    and generating an answer through a LangChain RunnablePassthrough chain.

    Args:
        question (str): The question to be answered.
        vector_db (FAISS): The vector database used for retrieval.

    Returns:
        str: The answer generated by the chain, or an error message if an exception occurs.
    """
    try:
        # Set up retriever from the vector database
        retriever = vector_db.as_retriever()
        
        # Generate prompt template
        prompt = ChatPromptTemplate.from_template(template)
        
        # Create the chain using the retriever, prompt, and LLM
        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        # Invoke the chain to generate the answer
        answer = chain.invoke(question)
        
        return answer
    
    except Exception as e:
        return f"An error occurred during processing: {str(e)}"

