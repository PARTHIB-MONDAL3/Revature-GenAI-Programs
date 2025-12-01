import streamlit as st
from ollama import Client

# -------------------------------------------------
# 1. Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Local Ollama Chatbot",
    page_icon="💬",
)

st.title("💬 Local AI Chatbot (Ollama + Streamlit)")
st.write("Runs fully offline, powered by **Ollama models** on your machine.")


# -------------------------------------------------
# 2. Load Ollama Client (cached)
# -------------------------------------------------
@st.cache_resource
def load_ollama():
    return Client(host="http://localhost:11434")

ollama_client = load_ollama()


# -------------------------------------------------
# 3. Build prompt from conversation history
# -------------------------------------------------
def build_prompt(history, user_message):
    lines = []
    for msg in history:
        role = "User" if msg["role"] == "user" else "Bot"
        lines.append(f"{role}: {msg['text']}")
    lines.append(f"User: {user_message}")
    lines.append("Bot:")
    return "\n".join(lines)


# -------------------------------------------------
# 4. Generate reply using Ollama
# -------------------------------------------------
def generate_reply(history, user_message, temperature):
    prompt = build_prompt(history, user_message)

    response = ollama_client.chat(
        model="llama3",       # You can change to mistral, phi3, llama2, gemma, etc.
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": temperature},
    )

    return response["message"]["content"].strip()


# -------------------------------------------------
# 5. Session State (chat history)
# -------------------------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "bot", "text": "Hey, I’m your local Ollama-powered assistant. Ask me anything."}
    ]

if "temperature" not in st.session_state:
    st.session_state["temperature"] = 0.7


# -------------------------------------------------
# 6. Sidebar Settings
# -------------------------------------------------
st.sidebar.header("⚙️ Model Settings")

temperature = st.sidebar.slider(
    "Temperature (higher = more creative)",
    0.1, 1.5, st.session_state["temperature"], 0.1
)
st.session_state["temperature"] = temperature

if st.sidebar.button("🧹 Clear Chat History"):
    st.session_state["messages"] = [
        {"role": "bot", "text": "Chat reset. Let's start fresh!"}
    ]
    st.experimental_rerun()


# -------------------------------------------------
# 7. Display chat history
# -------------------------------------------------
st.subheader("Conversation")

for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['text']}")
    else:
        st.markdown(f"**Bot:** {msg['text']}")


# -------------------------------------------------
# 8. User Input
# -------------------------------------------------
with st.form("chat_form", clear_on_submit=True):
    user_text = st.text_input("Type your message")
    send = st.form_submit_button("Send")

if send and user_text.strip():
    st.session_state["messages"].append({"role": "user", "text": user_text})

    with st.spinner("Thinking..."):
        reply = generate_reply(
            st.session_state["messages"],
            user_text,
            st.session_state["temperature"]
        )

    st.session_state["messages"].append({"role": "bot", "text": reply})

    st.experimental_rerun()
