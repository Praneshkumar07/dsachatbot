import streamlit as st
from google import genai

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="DSA Chatbot", page_icon="🧠")
st.title("🧠 DSA Doubt Solver")
st.caption("Ask anything about Data Structures & Algorithms")

# ── Load knowledge base ───────────────────────────────────────────────────────
@st.cache_data
def load_kb():
    with open("Dsa chatbot.txt", "r") as f:
        return f.read()

kb = load_kb()

# ── System prompt (your original logic) ──────────────────────────────────────
SYSTEM_PROMPT = f"""you are a dsa teacher your job is to clear doubts on dsa, you should clarify doubts with as simple as possible to understand
{kb}"""

# ── Gemini client ─────────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    return genai.Client(api_key="AIzaSyDymw04y6EiYYzCD3KaXnQ9rVtt-Sh7trc")   # <-- paste your API key here

client = get_client()

# ── Chat session (one per Streamlit session) ──────────────────────────────────
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-2.5-flash",
        config={"system_instruction": SYSTEM_PROMPT},
    )
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Display history ───────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── User input ────────────────────────────────────────────────────────────────
if user_input := st.chat_input("Ask a DSA question..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get response (your original logic)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat.send_message(user_input)
            reply = response.text
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})