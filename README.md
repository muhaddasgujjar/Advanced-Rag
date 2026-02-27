# 📖 Advanced RAG — Dark Psychology

An **Advanced Retrieval-Augmented Generation** system that reads a Dark Psychology PDF and answers questions in simple, everyday language.

Built with **ChromaDB**, **Groq (LLaMA 3.3)**, and **Streamlit**.

![Workflow](Advanced%20rag%20workflow.png)

---

## ✨ Features

| Feature | Description |
|---|---|
| **PDF Extraction** | PyPDFLoader with page-number metadata on every chunk |
| **Smart Retrieval** | ChromaDB with 0.8 similarity threshold — silent filtering |
| **LLM Generation** | Groq LLaMA 3.3 70B with structured, educational responses |
| **Fallback Handling** | Off-topic queries get a short friendly message + suggested questions |
| **Dark Mode UI** | Clean, professional dark theme with indigo accents |

---

## 🏗️ Architecture

```
User Question
    │
    ▼
┌─────────────────────┐
│   extraction.py     │  ← PyPDFLoader + chunking + page metadata
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│   ingestion.py      │  ← ChromaDB + similarity threshold (0.8)
└─────────┬───────────┘
          ▼
     Score ≥ 0.8?
    /           \
  YES            NO
   │              │
   ▼              ▼
Context        Empty context
   │              │
   ▼              ▼
┌─────────────────────┐
│   generation.py     │  ← Groq LLaMA 3.3 (handles both cases)
└─────────┬───────────┘
          ▼
   Answer to User
```

---

## 📁 Project Structure

```
Advanced Rag/
├── vector-db/
│   ├── extraction.py      # PDF loading + chunking with page metadata
│   ├── ingestion.py       # ChromaDB vector store + threshold filtering
│   ├── generation.py      # Groq LLaMA 3.3 response generation
│   └── advanced_app.py    # Streamlit dark-mode chat interface
├── dark pyscology.pdf     # Source PDF
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/muhaddasgujjar/Advanced-Rag.git
cd Advanced-Rag
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your API key

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run the app

```bash
cd vector-db
streamlit run advanced_app.py
```

---

## 🛠️ Tech Stack

- **LLM:** Groq API — LLaMA 3.3 70B Versatile
- **Vector DB:** ChromaDB (in-memory)
- **PDF Loader:** LangChain PyPDFLoader
- **Text Splitting:** RecursiveCharacterTextSplitter (1600 chars, 200 overlap)
- **Frontend:** Streamlit with custom dark-mode CSS
- **Language:** Python

---

## 📝 How It Works

1. **Extraction** — The PDF is loaded page-by-page. Each page is split into chunks of 1600 characters with 200-character overlap. Every chunk carries its source page number as metadata.

2. **Ingestion** — Chunks are embedded and stored in ChromaDB. When a user asks a question, the top 5 chunks are retrieved and scored. Only chunks scoring ≥ 0.8 similarity pass through.

3. **Generation** — The passing context (or empty string if nothing passed) is sent to LLaMA 3.3. If context exists, it gives a structured educational answer. If empty, it naturally says it couldn't find that topic and suggests related questions.

---

## 👤 Author

**Muhaddas Gujjar**

- GitHub: [@muhaddasgujjar](https://github.com/muhaddasgujjar)