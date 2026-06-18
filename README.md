# ChatGPT Helper for Rockwell Products

## Demo

<video src="Demo.mp4" controls width="100%"></video>

## About

An interactive chat assistant that converts Rockwell device help manuals and support articles (placed in the `Data/` folder) into vector embeddings stored as `.pkl` files. When a user asks a question in the Gradio-based chat UI, relevant context is retrieved from the vector database via semantic search and fed to OpenAI's language model to generate a precise, grounded answer.

The application is designed specifically to assist engineers and technicians working with Rockwell Automation products such as the PowerFlex 525, 755, and 755T drives — enabling fast, natural-language access to technical documentation without manual searching.

---

## File Structure

```
ChatGPT-Helper-for-Rockwell-Products/
│
├── main.py                      # Entry point — launches the Gradio chat UI
├── CreateChunks.py              # Ingests PDFs from Data/, creates vector embeddings, saves .pkl
├── QueryData.py                 # Loads the vector store and runs conversational retrieval
├── requirements.txt             # Python dependencies
├── ExtractedTextFromPDF.txt     # Intermediate text file generated during PDF ingestion
├── Powerflex755T.pkl            # Serialized FAISS vector store (generated after ingestion)
│
├── Data/                        # Place Rockwell device manuals (PDF) here
│   ├── Powerflex 525.pdf
│   ├── Powerflex 755.pdf
│   ├── Powerflex 755T Features.pdf
│   ├── Powerflex 755T.pdf
│   └── Powerflex40.pdf
│
└── myenv/                       # Python virtual environment (not committed to source control)
```

---

## How It Works

1. **Ingestion** — `CreateChunks.py` reads a PDF from `Data/`, extracts text via `textract`, splits it into token-sized chunks using LangChain's `RecursiveCharacterTextSplitter`, generates OpenAI embeddings, and saves the resulting FAISS vector store as a `.pkl` file.
2. **Retrieval** — `QueryData.py` loads the `.pkl` vector store and uses LangChain's `ConversationalRetrievalChain` with `gpt-3.5-turbo` to answer user questions, maintaining chat history across turns.
3. **UI** — `main.py` wraps everything in a Gradio `Blocks` chat interface served locally.

---

## Build & Run

### Prerequisites

- Python 3.9+
- An [OpenAI API key](https://platform.openai.com/account/api-keys)

### 1. Create and activate a virtual environment

```console
python -m venv myenv
myenv\Scripts\activate        # Windows
# source myenv/bin/activate   # macOS/Linux
```

### 2. Install dependencies

```console
pip install -r requirements.txt
```

### 3. (First time) Ingest a device manual

Add or verify the PDF path in `CreateChunks.py`, then uncomment line 28 in `main.py`:

```python
# CreateChunks.Create_Vector_Database()   # <-- uncomment this
```

### 4. Run the web app

```console
python main.py
```

You will be prompted to paste your OpenAI API key. After that, the Gradio chat UI will be available at `http://127.0.0.1:7860`.

> **Note:** After the vector database (`.pkl`) has been generated once, you can re-comment line 28 in `main.py` to skip re-ingestion on subsequent runs.
