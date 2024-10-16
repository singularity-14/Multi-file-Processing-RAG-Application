import streamlit as st
from rag_application import *

st.title("Multi-file Processing RAG Application")

# Initialize chat history and processed data in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

# File uploader in sidebar
uploaded_files = st.sidebar.file_uploader(
    "Choose files and Upload PDF, Excel, PowerPoint, or CSV files for processing",
    type=["pdf", "xlsx", "xls", "pptx", "csv"],
    accept_multiple_files=True
)

if uploaded_files:
    if len(uploaded_files) > 3:
        st.sidebar.error("You can only upload a maximum of 3 files.")
    else:
        st.sidebar.success(f"{len(uploaded_files)} files uploaded successfully!")
        
        # Indicate processing status in the sidebar
        status_placeholder = st.sidebar.empty()
        status_placeholder.text("Processing files...")

        # Process the files only if they haven't been processed yet
        if st.session_state.vector_db is None:
            documents = file_processing(uploaded_files)
            st.session_state.vector_db = text_chunking_uploading(documents) 
            status_placeholder.success("File processing complete!")
        else:
            status_placeholder.success("Files already processed!")
else:
    st.session_state.vector_db = None

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    try:
        # Display user message in the chat message container
        st.chat_message("user").markdown(prompt)
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            try:
                # Check if the vector database is available
                if st.session_state.vector_db is None:
                    response = "No files have been processed yet. Please upload and process files first."
                else:
                    # Response from the chain function using the stored vector database
                    response = chain(prompt, st.session_state.vector_db)
            except Exception as e:
                response = f"An error occurred while generating the response: {str(e)}"

            # Display the response
            st.markdown(response)
            
            # Add the response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
