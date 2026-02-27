# Naive RAG — Dark Psychology Q&A

 **Live Demo:** [https://native-rag-jrlzjnerndkg4rbugoe57q.streamlit.app](https://native-rag-jrlzjnerndkg4rbugoe57q.streamlit.app/)

A modular RAG pipeline that reads a Dark Psychology PDF and answers questions using ChromaDB + Groq LLaMA 3.3 70B.

## Setup

```bash
pip install chromadb groq langchain-community pypdf langchain-text-splitters python-dotenv streamlit
```

Create a `.env` file in the root:
```
GROQ_API_KEY=your_key_here
```

## File Structure

```
vector-db/
├── app.py            # Streamlit UI
├── main.py           # CLI version
├── extraction.py     # PDF loading & chunking
├── ingestion.py      # ChromaDB vector store
└── generation.py     # LLM response (ROSE framework)
```

## Run

```bash
# Web UI
streamlit run vector-db/app.py

# Terminal
python vector-db/main.py
```

## Testing

1. Run the app — should print `Successfully ingested X document chunks.`
2. Ask *"What is the main topic of this paper?"* — checks if retrieval works
3. Ask *"Explain Dark Triad traits."* — checks if ROSE framework is followed
4. Ask *"What is the recipe for chocolate cake?"* — should say it doesn't have the answer

## Push to GitHub

```bash
git init
git add .
git commit -m "Modular RAG with ROSE framework"
git branch -M main
git remote add origin https://github.com/muhaddasgujjar/Naive-Rag.git
git push -u origin main
```
