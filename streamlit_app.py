import streamlit as st
import openai
import os

# Set OpenAI API Key (recommended: use Streamlit secrets or .env for security)
openai.api_key = st.secrets.get("OPENAI_API_KEY", "")

# Streamlit app config
st.set_page_config(page_title="Simple Chatbot", page_icon="🤖")
st.title("🤖 Chatbot using OpenAI API")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Display past messages
for msg in st.session_state.messages[1:]:  # skip the system message
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
if prompt := st.chat_input("Ask me anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant reply
    with st.spinner("Thinking..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",  # or gpt-3.5-turbo
                messages=st.session_state.messages,
                temperature=0.7,
            )
            reply = response.choices[0].message["content"]
        except Exception as e:
            reply = f"Error: {e}"

    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
