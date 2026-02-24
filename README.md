# 🛡️ Privacy-First Local RAG Agent (Full-Stack)

## 📌 Overview
An offline, privacy-first AI Customer Support Agent built with Retrieval-Augmented Generation (RAG). This full-stack microservice runs entirely on local hardware, ensuring zero data leakage to third-party cloud APIs like OpenAI or Google. 

By utilizing local vector embeddings and an open-source Meta LLM, this system ingests internal company documents and serves highly accurate, context-aware answers through a REST API and a clean, interactive chat interface.

## 🚀 Tech Stack
* **LLM Engine:** Ollama (Llama 3.2)
* **Backend API:** FastAPI / Uvicorn
* **Frontend UI:** Streamlit
* **Orchestration:** LangChain
* **Vector Database:** ChromaDB
* **Embeddings:** Hugging Face (`all-MiniLM-L6-v2`)

## 💡 Key Features
* **100% Offline & Private:** All data chunking, vectorization, and text generation happen locally. Sensitive company data never leaves the network.
* **Decoupled Architecture:** Built with a headless FastAPI backend and a separate Streamlit frontend to demonstrate modern microservice design.
* **Zero API Costs:** Bypasses cloud rate limits and subscription fees by utilizing local open-source models.
* **Hallucination Prevention:** Grounds the AI's answers strictly in the provided local `faq.txt` data using RAG.



## 🛠️ Local Setup & Installation

### 1. Prerequisites
* Python 3.9+
* [Ollama](https://ollama.com/) installed on your machine.

### 2. Download the Local LLM
Open your terminal and download the Llama 3.2 model via Ollama:
```bash
ollama run llama3.2

```

*(Type `/bye` to exit once it finishes downloading).*

### 3. Clone & Install Dependencies

Clone this repository to your local machine, navigate into the folder, and install the required Python libraries:

```bash
pip install fastapi uvicorn pydantic langchain langchain-chroma langchain-huggingface langchain-ollama sentence-transformers tf-keras streamlit requests

```

---

## 🚀 Running the Application

Because this is a full-stack application, you need to run the backend and the frontend simultaneously in **two separate terminal windows**.

### Terminal 1: Start the AI Backend (FastAPI)

This boots up the vector database and the local LLM engine.

```bash
python -m uvicorn api:app --reload

```

* The API will be live at: `http://127.0.0.1:8000`
* Interactive API documentation (Swagger UI) is available at: `http://127.0.0.1:8000/docs`

### Terminal 2: Start the Chat Interface (Streamlit)

Once the backend is running, open a second terminal in the same folder and launch the user interface.

```bash
python -m streamlit run frontend.py

```

* The chat UI will automatically open in your browser at: `http://localhost:8501`

---

## 📡 Example API Usage (For Developers)

If you want to query the backend directly without the UI, you can send a POST request to the `/ask` endpoint.

**cURL Request:**

```bash
curl -X 'POST' \
  '[http://127.0.0.1:8000/ask](http://127.0.0.1:8000/ask)' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "question": "What is the return policy for opened items?"
}'

