import os
import streamlit as st
from pathlib import Path
from app import MultiDocAgent

# Cache folder for saving uploaded documents
CACHE_FOLDER = "cache"
os.makedirs(CACHE_FOLDER, exist_ok=True)
multi_doc_agent = MultiDocAgent()

# Initialize session state for agent if not already set
if "global_agent" not in st.session_state:
    st.session_state["global_agent"] = None  # Initially None, to be updated after processing


# Function to save uploaded files
def save_uploaded_file(uploaded_file, document_name):
    file_path = Path(CACHE_FOLDER) / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return str(file_path)

# Function to simulate backend indexing and processing
def process_documents(doc_name_mapping):
    st.info("Processing documents...")
    # Simulate backend processing (replace this with actual backend code)
    for name, path in doc_name_mapping.items():
        st.write(f"Indexing document: {name} at {path}")
    agent = multi_doc_agent.process_documents(doc_name_mapping)
    # Store the agent in session state
    st.session_state["global_agent"] = agent
    st.session_state["documents_processed"] = True
    st.success("Documents have been successfully indexed and processed.")

# Streamlit UI
st.title("Agentic RAG Chatbot - Document Uploader and Chat")

st.sidebar.header("Upload Documents")
uploaded_files = st.sidebar.file_uploader(
    "Upload one or more documents (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

doc_name_mapping = {}  # Dictionary to store document names and file paths

# Step 1: Document Upload and Processing
if uploaded_files:
    for uploaded_file in uploaded_files:
        st.sidebar.write(f"Processing file: {uploaded_file.name}")
        document_name = st.sidebar.text_input(
            f"Enter a name for '{uploaded_file.name}'",
            key=uploaded_file.name
        )
        if document_name:
            file_path = save_uploaded_file(uploaded_file, document_name)
            doc_name_mapping[document_name] = file_path
            st.sidebar.success(f"Saved '{uploaded_file.name}' as '{document_name}'.")

    if st.sidebar.button("Start Processing"):
        if doc_name_mapping:
            process_documents(doc_name_mapping)
        else:
            st.sidebar.error("Please upload documents before processing.")

# Step 2: Chat Interface (Enabled after processing)
if "documents_processed" in st.session_state and st.session_state["documents_processed"]:
    st.write("## Chat Interface")
    st.info("Start asking questions based on the uploaded documents.")

    # User's input for questions
    query = st.text_input("Enter your question:", "")

    if st.button("Submit Question"):
        if query:
            if st.session_state["global_agent"]:
                answer = st.session_state["global_agent"].query(query)
                st.success(f"{str(answer)}")
            else:
                st.error("Error: Document processing failed. Please re-upload and process again.")
        else:
            st.error("Please enter a question.")
else:
    st.info("Upload and process documents to enable the chat interface.")
