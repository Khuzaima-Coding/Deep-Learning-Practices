# Sirf Streamlit UI (ChatGPT jaisa)

import streamlit as st
from langchain_helper import get_models, create_chain, ask

st.set_page_config(page_title="Simple ChatGPT", page_icon="💬")

# --- Sidebar: API key, model aur history ---
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Groq API Key", type="password")

    model = None
    if api_key:
        try:
            # Sirf wahi models dikhayein jo is key pe available hain
            model = st.selectbox("Model", get_models(api_key))
        except Exception as e:
            st.error(f"Key ya connection ka masla: {e}")

    if st.button("🗑️ New Chat"):
        # Sirf chat aur memory saaf karein, API key rehne dein
        st.session_state.pop("chain", None)
        st.session_state.pop("model", None)
        st.session_state.messages = []
        st.rerun()

    st.header("🕘 History")
    for m in st.session_state.get("messages", []):
        if m["role"] == "user":
            st.write("• " + m["content"][:40])

st.title("💬 Simple ChatGPT")

# Key aur model dono zaroori hain
if not model:
    st.info("Pehle sidebar mein Groq API key daalein.")
    st.stop()

# Chain ek hi dafa banayein (memory bachi rahe), model badle to nayi banayein
if st.session_state.get("model") != model:
    st.session_state.model = model
    st.session_state.chain = create_chain(api_key, model)
    st.session_state.messages = []

# Purani chat screen pe dikhayein
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# Naya sawal lein
question = st.chat_input("Kuch poochein...")
if question:
    # User ka message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    # AI ka jawab
    with st.chat_message("assistant"):
        with st.spinner("Soch raha hoon..."):
            try:
                answer = ask(st.session_state.chain, question)
            except Exception as e:
                answer = f"❌ Error: {e}"
        st.write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
st.balloons()