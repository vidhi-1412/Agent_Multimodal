import streamlit as st
import time

st.set_page_config(
    page_title="ManufactureIQ",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force white background — override ALL Streamlit dark theme elements
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&family=Fraunces:wght@500;700&display=swap');

/* ROOT OVERRIDE — force white everywhere */
:root {
    --background-color: #f7faf7 !important;
    --secondary-background-color: #ffffff !important;
    --text-color: #1a2e1a !important;
    --primary-color: #2d7a2d !important;
}

html, body { background-color: #f7faf7 !important; }

.stApp {
    background-color: #f7faf7 !important;
    font-family: 'DM Sans', sans-serif !important;
    color: #1a2e1a !important;
}

/* Kill dark mode completely */
[data-testid="stAppViewContainer"] { background-color: #f7faf7 !important; }
[data-testid="stHeader"] { background-color: #ffffff !important; border-bottom: 1px solid #d5e8d5 !important; }
[data-testid="stToolbar"] { background-color: #ffffff !important; }
[data-testid="block-container"] { background-color: transparent !important; }

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 2px solid #d5e8d5 !important;
}
[data-testid="stSidebar"] * { color: #1a2e1a !important; }
[data-testid="stSidebar"] .stSelectbox > div > div {
    background-color: #f0f7f0 !important;
    border: 1.5px solid #b8d8b8 !important;
    color: #1a2e1a !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] .stTextInput > div > div > input {
    background-color: #f0f7f0 !important;
    border: 1.5px solid #b8d8b8 !important;
    color: #1a2e1a !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] .stButton > button {
    background-color: #fff0f0 !important;
    border: 1.5px solid #e8a0a0 !important;
    color: #c05050 !important;
    border-radius: 8px !important;
    width: 100% !important;
    font-size: 13px !important;
}

/* MAIN text colors */
h1, h2, h3, h4, p, span, div, label {
    color: #1a2e1a !important;
}

/* CHAT INPUT */
[data-testid="stChatInput"] {
    background-color: #ffffff !important;
}
[data-testid="stChatInput"] > div {
    background-color: #ffffff !important;
    border: 2px solid #b8d8b8 !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 12px rgba(45,122,45,0.08) !important;
}
[data-testid="stChatInput"] textarea {
    background-color: #ffffff !important;
    color: #1a2e1a !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stChatInput"] button {
    background-color: #2d7a2d !important;
    border-radius: 8px !important;
}

/* CHAT MESSAGES — force dark text on all children */
[data-testid="stChatMessage"] {
    background-color: #ffffff !important;
    border: 1px solid #d5e8d5 !important;
    border-radius: 14px !important;
    padding: 14px !important;
    margin-bottom: 12px !important;
    color: #1a2e1a !important;
}
[data-testid="stChatMessage"] *,
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] div,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] strong,
[data-testid="stChatMessage"] em,
[data-testid="stChatMessage"] code,
[data-testid="stChatMessage"] .stMarkdown,
[data-testid="stChatMessage"] .stMarkdown * {
    color: #1a2e1a !important;
    font-family: 'DM Sans', sans-serif !important;
    line-height: 1.7 !important;
}

/* Also target the stText and stMarkdownContainer */
.stChatMessage .stMarkdownContainer p,
.stChatMessage .stMarkdownContainer span,
.stChatMessage [class*="markdown"] * {
    color: #1a2e1a !important;
}

/* User message — light green bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, #eaf6ea, #f0faf0) !important;
    border-color: #a8d5a8 !important;
}

/* Spinner */
[data-testid="stSpinner"] > div { color: #2d7a2d !important; }

/* HIDE default streamlit stuff */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
.stDeployButton { display: none; }

/* SCROLLBAR */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #f0f7f0; }
::-webkit-scrollbar-thumb { background: #b8d8b8; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ---- Lazy imports to avoid circular issues ----
from main import run
from memory.vector_store import get_all_history, get_stats, clear_memory, search_similar

# ---- SESSION STATE ----
if "messages" not in st.session_state:
    st.session_state.messages = []

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    # Logo
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding:8px 0 20px 0;border-bottom:1.5px solid #d5e8d5;margin-bottom:20px;">
        <div style="width:36px;height:36px;background:linear-gradient(135deg,#2d7a2d,#4aad4a);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px;box-shadow:0 2px 8px rgba(45,122,45,0.25);">🏭</div>
        <div>
            <div style="font-family:'Fraunces',serif;font-size:18px;font-weight:700;color:#1a2e1a;line-height:1.1;">Manufacture<span style="color:#2d7a2d;">IQ</span></div>
            <div style="font-size:10px;color:#6b8f6b;letter-spacing:0.5px;">Agentic AI System</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p style="font-size:11px;font-weight:600;letter-spacing:1.2px;color:#6b8f6b;text-transform:uppercase;margin-bottom:10px;">⚙️ Configuration</p>', unsafe_allow_html=True)
    industry = st.selectbox("Industry", ["Aluminum", "Steel", "Electronics", "Plastics", "Textile"])
    location = st.text_input("Location", "India")

    # Memory Stats
    st.markdown('<p style="font-size:11px;font-weight:600;letter-spacing:1.2px;color:#6b8f6b;text-transform:uppercase;margin:20px 0 10px 0;">🧠 ChromaDB Memory</p>', unsafe_allow_html=True)
    stats = get_stats()
    st.markdown(f"""
    <div style="background:#f0f7f0;border:1px solid #c5dfc5;border-radius:10px;padding:12px 14px;">
        <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
            <span style="font-size:12px;color:#5a7a5a;">Queries Stored</span>
            <span style="font-size:14px;font-weight:700;color:#2d7a2d;">{stats['queries_stored']}</span>
        </div>
        <div style="display:flex;justify-content:space-between;">
            <span style="font-size:12px;color:#5a7a5a;">Total Entries</span>
            <span style="font-size:14px;font-weight:700;color:#2d7a2d;">{stats['total_entries']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Past queries
    st.markdown('<p style="font-size:11px;font-weight:600;letter-spacing:1.2px;color:#6b8f6b;text-transform:uppercase;margin:20px 0 10px 0;">📋 Past Queries</p>', unsafe_allow_html=True)
    history = get_all_history(limit=5)
    if history:
        for h in history:
            ts = h['timestamp'][:10] if h.get('timestamp') else ''
            q = h['query'][:48] + ("..." if len(h['query']) > 48 else "")
            st.markdown(f"""
            <div style="background:#f7fcf7;border:1px solid #d5e8d5;border-left:3px solid #4aad4a;border-radius:8px;padding:9px 12px;margin-bottom:7px;">
                <div style="font-size:12px;font-weight:500;color:#1a2e1a;margin-bottom:2px;">{q}</div>
                <div style="font-size:10px;color:#8aac8a;">{ts}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<p style="font-size:12px;color:#8aac8a;">No history yet.</p>', unsafe_allow_html=True)

    st.markdown('<p style="font-size:11px;font-weight:600;letter-spacing:1.2px;color:#6b8f6b;text-transform:uppercase;margin:20px 0 10px 0;">🗑 Actions</p>', unsafe_allow_html=True)
    if st.button("Clear ChromaDB Memory"):
        if clear_memory():
            st.success("Memory cleared!")
            time.sleep(1)
            st.rerun()

# ============================================================
# MAIN AREA
# ============================================================
st.markdown("""
<div style="padding: 28px 20px 10px 20px;">
    <h1 style="font-family:'Fraunces',serif;font-size:26px;font-weight:700;color:#1a2e1a;margin-bottom:4px;">
        🌿 Manufacturing Assistant
    </h1>
    <p style="font-size:14px;color:#5a7a5a;margin-bottom:0;">
        Ask me to find suppliers, compare pricing, or generate reports — powered by ChromaDB memory.
    </p>
    <hr style="border:none;border-top:1.5px solid #d5e8d5;margin:16px 0 20px 0;">
</div>
""", unsafe_allow_html=True)

# Welcome screen when no messages
if not st.session_state.messages:
    col1, col2 = st.columns(2)
    suggestions = [
        f"🔍 Find top 3 {industry} suppliers in {location}",
        "📊 Compare Steel supplier pricing",
        "📋 Generate Electronics supplier report",
        "⏱ Best lead time suppliers in India",
    ]
    for i, s in enumerate(suggestions):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown(f"""
            <div style="background:#ffffff;border:1.5px solid #d5e8d5;border-radius:12px;padding:14px 16px;
                        margin-bottom:10px;cursor:pointer;transition:all 0.2s;">
                <span style="font-size:13px;font-weight:500;color:#2d4a2d;">{s}</span>
            </div>
            """, unsafe_allow_html=True)

# Display chat history using native Streamlit chat (proper colors)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🤖"):
        # Memory badge for assistant
        if msg["role"] == "assistant" and msg.get("from_memory"):
            st.markdown("""
            <div style="display:inline-flex;align-items:center;gap:5px;background:#edf7ed;
                        border:1px solid #c5dfc5;border-radius:20px;padding:3px 10px;
                        font-size:11px;color:#2d7a2d;font-weight:500;margin-bottom:8px;">
                🧠 Related to a past query in memory
            </div>
            """, unsafe_allow_html=True)
        st.markdown(msg["content"])
        st.caption(msg.get("time", ""))

# Chat input
user_input = st.chat_input("Ask about suppliers, pricing, or generate a report…")

if user_input:
    ts = time.strftime("%I:%M %p")

    # Check ChromaDB for similar past queries
    similar = search_similar(user_input, n_results=2)
    from_memory = bool(similar and similar[0]["similarity"] > 0.75)

    st.session_state.messages.append({"role": "user", "content": user_input, "time": ts})

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🤖 Agents thinking…"):
            response = run(query=user_input, industry=industry, location=location)

    resp_ts = time.strftime("%I:%M %p")
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "time": resp_ts,
        "from_memory": from_memory
    })
    st.rerun()