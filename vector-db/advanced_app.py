import streamlit as st
import os, sys

sys.path.insert(0, os.path.dirname(__file__))
from extraction import extract_and_chunk
from ingestion import VectorStore
from generation import Generator

# --- Config ---
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

PDF_PATH = os.path.join(os.path.dirname(__file__), "..", "dark pyscology.pdf")

st.set_page_config(page_title="Dark Psychology — Ask Me Anything", page_icon="📖", layout="wide")

# --- CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Outfit', sans-serif; }
    .stApp { background-color: #111827; }
    .main .block-container { color: #F3F4F6; }
    header[data-testid="stHeader"] { background: #111827; }
    h1,h2,h3,h4,h5,h6 { color: #F3F4F6 !important; }
    p,li,span,div,label { color: #F3F4F6; }

    .hero {
        background: linear-gradient(135deg, #1F2937 0%, #1a1f3a 50%, #1F2937 100%);
        padding: 2.4rem 2rem; border-radius: 20px; margin-bottom: 1.8rem;
        text-align: center; position: relative; overflow: hidden;
        border: 1px solid rgba(99,102,241,0.25);
        box-shadow: 0 0 40px rgba(99,102,241,0.08);
    }
    .hero::before {
        content: ''; position: absolute; top: -40%; right: -20%;
        width: 350px; height: 350px; border-radius: 50%;
        background: rgba(99,102,241,0.06); pointer-events: none;
    }
    .hero h1 {
        font-size: 2.1rem; font-weight: 700; margin-bottom: 0.2rem;
        background: linear-gradient(90deg, #a5b4fc, #818cf8, #6366F1);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .hero p { font-size: 0.95rem; color: #9CA3AF !important; margin: 0; }
    .chips { display: flex; gap: 0.6rem; flex-wrap: wrap; justify-content: center; margin-top: 1rem; }
    .chip {
        background: #374151; border: 1px solid rgba(99,102,241,0.4);
        border-radius: 30px; padding: 0.35rem 1rem;
        font-size: 0.78rem; font-weight: 500; color: #a5b4fc !important;
        transition: background 0.2s; cursor: default;
    }
    .chip:hover { background: #4B5563; }

    .stChatMessage { border-radius: 16px !important; background: #1F2937 !important; }
    .ctx-card {
        background: #1F2937; border: 1px solid #374151;
        border-radius: 12px; padding: 0.9rem 1.1rem; margin-bottom: 0.6rem;
        font-size: 0.84rem; color: #9CA3AF !important; line-height: 1.55;
    }
    .ctx-page {
        display: inline-block; background: #374151;
        color: #a5b4fc !important; border: 1px solid rgba(99,102,241,0.3);
        padding: 0.1rem 0.55rem; border-radius: 8px;
        font-size: 0.7rem; font-weight: 600; margin-bottom: 0.4rem;
    }
    section[data-testid="stSidebar"] { background: #1F2937 !important; }
    section[data-testid="stSidebar"] * { color: #9CA3AF !important; }
    section[data-testid="stSidebar"] strong, section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 { color: #F3F4F6 !important; }
    .stChatInput { background: #1F2937; }
    textarea { background: #1F2937 !important; color: #F3F4F6 !important; border-color: #374151 !important; }
    .streamlit-expanderHeader { color: #a5b4fc !important; }
    .stButton button {
        background: #374151 !important; color: #F3F4F6 !important;
        border: 1px solid rgba(99,102,241,0.3) !important; transition: background 0.2s;
    }
    .stButton button:hover { background: #4B5563 !important; }
    .stSpinner > div { color: #9CA3AF !important; }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="hero">
    <h1>📖 Dark Psychology — Ask Me Anything</h1>
    <p>Ask any question about the book and I'll explain it in simple words</p>
    <div class="chips">
        <span class="chip">📄 Based on your PDF</span>
        <span class="chip">💬 Plain-language answers</span>
        <span class="chip">🔄 Suggests better questions</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Pipeline ---
@st.cache_resource(show_spinner=False)
def load_pipeline():
    docs = extract_and_chunk(PDF_PATH)
    db = VectorStore()
    db.add_documents(docs)
    return db, len(docs)

with st.spinner("📄 Reading your book..."):
    db, chunk_count = load_pipeline()

gen = Generator(GROQ_API_KEY)

# --- Chat ---
st.markdown("### 💬 Chat")
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("sources"):
            with st.expander("📚 Where I found this"):
                for text, _, meta in msg["sources"]:
                    pg = meta.get("page_number", "?")
                    st.markdown(f'<span class="ctx-page">📄 Page {pg}</span>', unsafe_allow_html=True)
                    st.markdown(f'<div class="ctx-card">{text[:500]}</div>', unsafe_allow_html=True)

if user_query := st.chat_input("Ask me anything about the book..."):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Looking through the book..."):
            result = db.query_with_threshold(user_query, threshold=0.8)
        with st.spinner("Writing your answer..."):
            answer = gen.get_response(result["context"], user_query)
        st.markdown(answer)
        if result["sources"]:
            with st.expander("📚 Where I found this"):
                for text, _, meta in result["sources"]:
                    pg = meta.get("page_number", "?")
                    st.markdown(f'<span class="ctx-page">📄 Page {pg}</span>', unsafe_allow_html=True)
                    st.markdown(f'<div class="ctx-card">{text[:500]}</div>', unsafe_allow_html=True)

    st.session_state.messages.append({
        "role": "assistant", "content": answer,
        "sources": result["sources"] if result["is_relevant"] else [],
    })

# --- Sidebar ---
with st.sidebar:
    st.markdown("## 📖 About")
    st.markdown("This app reads a **Dark Psychology** PDF and answers your questions in simple, everyday language.")
    st.markdown("---")
    st.markdown(f"**Book:** dark pyscology.pdf")
    st.markdown(f"**Sections:** {chunk_count}")
    st.markdown("**AI:** LLaMA 3.3")
    st.markdown("---")
    st.markdown("### 💡 Try Asking")
    st.markdown("- What is dark psychology?\n- How do people manipulate others?\n- What is gaslighting?\n- How can I protect myself?\n- What is the dark triad?")
    st.markdown("---")
    if st.button("🗑️ Start Over"):
        st.session_state.messages = []
        st.rerun()
