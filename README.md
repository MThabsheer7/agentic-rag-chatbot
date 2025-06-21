# 🤖 Agentic RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot powered by an agentic architecture using LlamaIndex, OpenAI GPT-4o, and Streamlit. This system enables dynamic interaction with multiple PDFs (like earnings reports or research papers), where an LLM intelligently decides whether to query documents or generate answers directly.

## ✨ Key Features

- **Agent-based Orchestration**: Uses `FunctionCallingAgentWorker` and `AgentRunner` to dynamically manage document tools and query resolution.
- **Multi-Document Handling**: Upload and chat with multiple PDFs through a modular Streamlit interface.
- **Tool Indexing with LlamaIndex**: Each document is transformed into vector-based and summarization tools using `VectorStoreIndex` and `SummaryIndex`.
- **Smart Query Routing**: The agent retrieves the right tool (vector or summary) depending on the user query context.
- **Document Caching & Frontend**: Interactive document upload and chat interface using Streamlit with persistent document storage.

## 📂 Project Structure

```
agentic-rag-chatbot/
├── Scripts/
│   ├── app.py                  # Main backend logic (agent construction, doc processing)
│   ├── frontend.py             # Streamlit-based UI
│   ├── utils.py                # Config reader
│   └── cache/                  # Uploaded documents (PDFs)
├── LICENSE
├── .gitignore
```

## 🚀 How to Run

### 1. Clone & Setup Environment

```bash
git clone https://github.com/MThabsheer7/agentic-rag-chatbot.git
cd agentic-rag-chatbot
python -m venv venv
source venv/bin/activate   # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

> Note: Set your OpenAI API key in the YAML file referenced in `utils.py`.

### 2. Run the App

```bash
cd Scripts
streamlit run frontend.py
```

Upload multiple PDF documents through the sidebar, assign them names, and then interact via the chat interface.

## 📦 Dependencies

- `llama-index` (LlamaIndex)
- `streamlit`
- `openai`
- `PyYAML`
- `loguru`

Install via:

```bash
pip install -r requirements.txt
```

## 📁 Config Example (config.yaml)

```yaml
api:
  openai: sk-xxxxxxxxxxxxxxxxxxxx
```

## 📸 Screenshots

*(Add screenshots of UI or chat examples if needed)*

## 🧠 Use Case

This system was built to support document-intensive domains like financial reporting, where users can upload multiple earnings reports or company filings and ask complex, cross-document questions using a single conversational agent.
